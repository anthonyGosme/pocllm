"""Harnais d'évaluation du retrieval + tableau d'ablation.

Un chunk compte comme touché si son (doc_id, span) CHEVAUCHE le span d'or.
C'est ce qui rend la mesure indépendante du découpage : changer de stratégie de
chunking ne change pas la vérité terrain (§5).

Métriques instrumentées dès le départ comme l'exige le §4 : recall@k, MRR,
nDCG@10, plus la ventilation par type de question — c'est elle qui doit montrer
que le sparse gagne sur les néologismes et le dense sur les conceptuelles.
"""
from __future__ import annotations
import argparse, copy, json, math, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import yaml                                                    # noqa: E402
from pocllm.retrieve.hybrid import load                        # noqa: E402

EVAL = ROOT / "evals" / "eval_v0_echantillon.jsonl"
RESULTS = ROOT / "evals" / "results"


def overlaps(a, b) -> bool:
    return a and b and a[0] < b[1] and b[0] < a[1]


def gold_hits(chunk: dict, sources: list[dict]) -> set[int]:
    """Indices des sources d'or que ce chunk couvre."""
    out = set()
    for i, s in enumerate(sources):
        if s.get("doc_id") == chunk["doc_id"] and overlaps(chunk["span"], s.get("span")):
            out.add(i)
    return out


def ndcg(gains: list[float], ideal: int, k=10) -> float:
    dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains[:k]))
    idl = sum(1.0 / math.log2(i + 2) for i in range(min(ideal, k)))
    return dcg / idl if idl else 0.0


def evaluate(cfg, questions, retrievers, ks=(1, 5, 10, 20), router=None):
    per_q = []
    for q in questions:
        qcfg, motif = router.route(q["question"], cfg) if router else (cfg, "")
        cols = ["maison", "canon"] if q["corpus"] == "mixte" else [q["corpus"]]
        merged, traces = [], []
        for c in cols:
            r = retrievers.get(c)
            if r is None:
                continue
            res, tr = r.search(q["question"], qcfg)
            merged += [(x, r.chunks[x.chunk_id]) for x in res]
            traces.append(f"{c}:{tr}")
        merged.sort(key=lambda t: -(t[0].rerank_score if t[0].rerank_score is not None else t[0].score))

        srcs = q["expected_sources"]
        covered, gains, first = set(), [], None
        for rank, (res, ch) in enumerate(merged, start=1):
            h = gold_hits(ch, srcs)
            new = h - covered
            gains.append(1.0 if new else 0.0)
            if new and first is None:
                first = rank
            covered |= h
        per_q.append({
            "id": q["id"], "type": q["type"],
            "recall": {f"@{k}": len({i for r_, c_ in merged[:k] for i in gold_hits(c_, srcs)}) / max(len(srcs), 1)
                       for k in ks},
            "rr": 1.0 / first if first else 0.0,
            "ndcg@10": ndcg(gains, len(srcs)),
            "n_retrieved": len(merged), "trace": " | ".join(traces),
            "route": motif,
        })
    return per_q


def aggregate(per_q, ks=(1, 5, 10, 20)):
    n = max(len(per_q), 1)
    agg = {f"recall@{k}": sum(p["recall"][f"@{k}"] for p in per_q) / n for k in ks}
    agg["MRR"] = sum(p["rr"] for p in per_q) / n
    agg["nDCG@10"] = sum(p["ndcg@10"] for p in per_q) / n
    by = {}
    for p in per_q:
        by.setdefault(p["type"], []).append(p)
    agg["par_type"] = {t: {"n": len(v),
                           "recall@10": sum(x["recall"]["@10"] for x in v) / len(v),
                           "MRR": sum(x["rr"] for x in v) / len(v)}
                       for t, v in sorted(by.items())}
    return agg


def apply_overrides(cfg, overrides):
    cfg = copy.deepcopy(cfg)
    for o in overrides:
        path, _, val = o.partition("=")
        node = cfg
        keys = path.split(".")
        for k in keys[:-1]:
            node = node[k]
        cur = node[keys[-1]]
        node[keys[-1]] = (val.lower() == "true") if isinstance(cur, bool) else type(cur)(val) if cur is not None else val
    return cfg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "config" / "default.yaml"))
    ap.add_argument("--name", default=None)
    ap.add_argument("--set", nargs="*", default=[], help="ex: retrieval.sparse.enabled=false")
    a = ap.parse_args()

    cfg = apply_overrides(yaml.safe_load(open(a.config, encoding="utf-8")), a.set)
    # `keep` sert la génération, pas la mesure : le tronquer avant de calculer
    # recall@20 la sous-estimerait mécaniquement. On garde au moins max(ks).
    KS = (1, 5, 10, 20)
    cfg["retrieval"]["rerank"]["keep"] = max(cfg["retrieval"]["rerank"].get("keep", 10), max(KS))
    name = a.name or cfg["run_name"]
    questions = [json.loads(l) for l in EVAL.open(encoding="utf-8")]

    r = cfg["retrieval"]
    retrievers = {c: load(c, profile=r["dense"]["profile"],
                          k1=r["sparse"]["k1"], b=r["sparse"]["b"],
                          protect_codes=r["sparse"].get("protect_codes", True))
                  for c in ("maison", "canon")}
    router = None
    if r.get("routing", {}).get("enabled"):
        from pocllm.retrieve.routing import Router
        router = Router(max_canon_df=r["routing"]["max_canon_df"],
                        min_maison_df=r["routing"]["min_maison_df"],
                        protect_codes=r["sparse"].get("protect_codes", True),
                        disable_rerank=r["routing"].get("disable_rerank", False))
    t0 = time.perf_counter()
    per_q = evaluate(cfg, questions, retrievers, router=router)
    dt = time.perf_counter() - t0
    agg = aggregate(per_q)

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = {"run": name, "config": {"dense": r["dense"]["enabled"], "sparse": r["sparse"]["enabled"],
                                   "fusion": r["fusion"]["enabled"], "rrf_k": r["fusion"]["k"],
                                   "rerank": r["rerank"]["enabled"], "profile_dense": r["dense"]["profile"],
                                   "profile_rerank": r["rerank"]["profile"]},
           "n_questions": len(questions), "latence_totale_s": round(dt, 1),
           "latence_par_question_s": round(dt / max(len(questions), 1), 2),
           "metriques": agg, "par_question": per_q}
    (RESULTS / f"{name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\n=== {name} ===  dense={r['dense']['enabled']} sparse={r['sparse']['enabled']} "
          f"fusion={r['fusion']['enabled']} rerank={r['rerank']['enabled']}")
    for k in ("recall@1", "recall@5", "recall@10", "recall@20", "MRR", "nDCG@10"):
        print(f"  {k:12s} {agg[k]:.3f}")
    print(f"  {'latence/q':12s} {out['latence_par_question_s']:.2f} s")
    print("\n  par type :")
    for t, v in agg["par_type"].items():
        print(f"    {t:20s} n={v['n']:2d}  recall@10={v['recall@10']:.2f}  MRR={v['MRR']:.2f}")
    print(f"\n-> {RESULTS / (name + '.json')}")


if __name__ == "__main__":
    main()
