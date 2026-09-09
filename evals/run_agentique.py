"""Jalon 4 — boucle agentique sur le jeu d'éval.

Critère de sortie du cadrage : « résolution multi-hop fonctionnelle ». Les six
questions multi-hop l'éprouvent ; les six pièges éprouvent en plus le refus, que
le baseline du jalon 1 réussit 5/5 avec le contexte complet. L'écart entre les
deux est la mesure intéressante : l'agent doit d'abord RÉCUPÉRER le passage que
le baseline avait déjà sous les yeux.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import yaml                                                       # noqa: E402
import anthropic                                                  # noqa: E402
from pocllm.llm import load_dotenv                                # noqa: E402
from pocllm.agent.boucle import Boucle                            # noqa: E402

EVAL = ROOT / "evals" / "eval_v0_echantillon.jsonl"
RESULTS = ROOT / "evals" / "results"


def verdict(t: str) -> str:
    bas = t.lower()
    i = bas.rfind("verdict:")
    if i == -1:
        return "indetermine"
    return "refuser" if "refuser" in bas[i:i + 40] else "repondre"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="agentique")
    ap.add_argument("--types", nargs="*", default=["multi_hop", "piege_attribution"])
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("-v", "--verbeux", action="store_true")
    a = ap.parse_args()

    load_dotenv()
    cfg = yaml.safe_load((ROOT / "config" / "default.yaml").read_text(encoding="utf-8"))
    cl = anthropic.Anthropic(api_key=os.environ["POCLLM_ANTHROPIC_API_KEY"], timeout=600.0)
    b = Boucle(cl, modele=cfg["generation"]["model"], budget=cfg["guardrails"]["budget"],
               effort=cfg["generation"].get("effort"), verbeux=a.verbeux)

    qs = [json.loads(l) for l in EVAL.open(encoding="utf-8")]
    if a.types:
        qs = [q for q in qs if q["type"] in a.types]
    if a.limit:
        qs = qs[:a.limit]
    print(f"{len(qs)} questions · modèle {b.modele} · budget "
          f"{b.max_etapes} étapes / {b.max_outils} outils / {b.max_tokens_total} tokens\n",
          flush=True)

    lignes, t0 = [], time.perf_counter()
    for i, q in enumerate(qs, 1):
        print(f"[{i:2d}/{len(qs)}] {q['id']} {q['type'][:17]:17s}", flush=True)
        r = b.executer(q["question"])
        v = verdict(r.reponse)
        attendu = q.get("expected_behavior", "repondre")
        lignes.append({"id": q["id"], "type": q["type"], "verdict": v, "attendu": attendu,
                       "correct": v == attendu, "tours": r.tours, "arret": r.arret,
                       "outils": r.outils_utilises, "n_outils": len(r.etapes),
                       "cout_usd": round(r.cout_usd, 5), "duree_s": round(r.duree_s, 1),
                       "reponse": r.reponse,
                       "etapes": [{"outil": e.outil, "args": e.args, "resume": e.resume}
                                  for e in r.etapes]})
        print(f"          {r.tours} tours · {len(r.etapes)} appels · {'/'.join(r.outils_utilises) or '—'}"
              f" · verdict={v} (attendu {attendu}) · {r.cout_usd:.4f} $ · {r.duree_s:.0f}s",
              flush=True)

    dt = time.perf_counter() - t0
    pieges = [l for l in lignes if l["attendu"] == "refuser"]
    mh = [l for l in lignes if l["type"] == "multi_hop"]
    out = {"run": a.name, "modele": b.modele, "n_questions": len(lignes),
           "duree_s": round(dt, 1), "cout_total_usd": round(sum(l["cout_usd"] for l in lignes), 4),
           "refus_correct": round(sum(l["correct"] for l in pieges) / len(pieges), 3) if pieges else None,
           "faux_refus": sum(1 for l in lignes if l["attendu"] == "repondre" and l["verdict"] == "refuser"),
           "multi_hop_deux_outils": sum(1 for l in mh if l["n_outils"] >= 2),
           "multi_hop_n": len(mh),
           "outils_moyen": round(sum(l["n_outils"] for l in lignes) / max(len(lignes), 1), 2),
           "arrets_budget": sum(1 for l in lignes if l["arret"].startswith("budget")),
           "par_question": lignes}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{a.name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    print(f"\nrefus correct sur les pièges : {out['refus_correct']} ({len(pieges)} questions)")
    print(f"faux refus : {out['faux_refus']}")
    print(f"multi-hop ayant appelé >= 2 outils : {out['multi_hop_deux_outils']}/{out['multi_hop_n']}")
    print(f"appels d'outils par question : {out['outils_moyen']} · arrêts sur budget : {out['arrets_budget']}")
    print(f"coût total {out['cout_total_usd']} $ · {dt/60:.1f} min")
    print(f"-> {RESULTS / (a.name + '.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
