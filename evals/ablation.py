"""Tableau d'ablation — le livrable numéro un du POC (§9).

Chaque ligne coupe un étage et rejoue le même jeu d'éval. Le delta chiffré est
ce qui doit figurer au README ; les hypothèses pré-enregistrées dans le champ
`hypothese_ablation` de chaque question disent ce qu'on attendait, et l'écart
entre attendu et mesuré est le contenu intéressant.
"""
from __future__ import annotations
import json, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = str(ROOT / ".venv" / "bin" / "python")
RESULTS = ROOT / "evals" / "results"

# (nom, [overrides]) — l'ordre suit la progression des jalons 2 -> 3
CONFIGS = [
    ("sparse_seul",        ["retrieval.dense.enabled=false", "retrieval.rerank.enabled=false"]),
    ("dense_seul",         ["retrieval.sparse.enabled=false", "retrieval.rerank.enabled=false"]),
    ("hybride_sans_fusion",["retrieval.fusion.enabled=false", "retrieval.rerank.enabled=false"]),
    ("hybride_rrf60",      ["retrieval.rerank.enabled=false"]),
    ("hybride_rrf10",      ["retrieval.fusion.k=10", "retrieval.rerank.enabled=false"]),
    ("hybride_rrf30",      ["retrieval.fusion.k=30", "retrieval.rerank.enabled=false"]),
    ("hybride_rrf120",     ["retrieval.fusion.k=120", "retrieval.rerank.enabled=false"]),
    ("sparse_sans_codes",  ["retrieval.dense.enabled=false", "retrieval.rerank.enabled=false",
                            "retrieval.sparse.protect_codes=false"]),
    # chiffre le coût d'un modèle d'embedding symétrique (paraphrase) là où la
    # tâche est asymétrique (question -> passage). C'est l'erreur corrigée, gardée
    # comme mesure plutôt qu'effacée.
    ("dense_symetrique",   ["retrieval.sparse.enabled=false", "retrieval.rerank.enabled=false",
                            "retrieval.dense.profile=symmetric"]),
    # la branche faible dilue-t-elle la forte ? poids 2/1 en faveur du sparse.
    ("hybride_rrf60_pondere", ["retrieval.rerank.enabled=false",
                               "retrieval.fusion.w_sparse=2.0"]),
    ("hybride_rrf60_rerank", []),
    # Les similarités e5 s'écrasent (toutes entre 0,81 et 0,88 sur ce corpus) :
    # 0,03 d'écart sépare le rang 1 du rang 4 000. Couper à top_k=50 jette des
    # chunks d'or situés aux rangs 54, 61, 115. La profondeur de candidats est
    # donc un paramètre de premier plan ici, pas un détail d'implémentation.
    ("dense_topk200",      ["retrieval.sparse.enabled=false", "retrieval.rerank.enabled=false",
                            "retrieval.dense.top_k=200"]),
    ("dense_topk500",      ["retrieval.sparse.enabled=false", "retrieval.rerank.enabled=false",
                            "retrieval.dense.top_k=500"]),
    ("hybride_topk200",    ["retrieval.rerank.enabled=false", "retrieval.dense.top_k=200",
                            "retrieval.sparse.top_k=200"]),
    ("hybride_topk200_rerank50", ["retrieval.dense.top_k=200", "retrieval.sparse.top_k=200",
                                  "retrieval.rerank.top_n.fast=50"]),
]


def run(name, overrides):
    t = time.perf_counter()
    p = subprocess.run([PY, str(ROOT / "evals" / "run_eval.py"), "--name", name, "--set", *overrides],
                       capture_output=True, text=True, cwd=ROOT)
    if p.returncode != 0:
        print(f"  ECHEC {name}\n{p.stderr[-900:]}")
        return None
    d = json.loads((RESULTS / f"{name}.json").read_text(encoding="utf-8"))
    d["duree_s"] = round(time.perf_counter() - t, 1)
    return d


def table(runs):
    cols = ["recall@1", "recall@5", "recall@10", "recall@20", "MRR", "nDCG@10"]
    types = sorted({t for r in runs for t in r["metriques"]["par_type"]})
    L = ["# Tableau d'ablation", "",
         f"{len(runs[0]['par_question'])} questions · corpus 23 615 chunks (canon 21 600 / maison 2 015)", "",
         "| configuration | " + " | ".join(cols) + " | latence/q |",
         "|---|" + "---|" * (len(cols) + 1)]
    base = None
    for r in runs:
        m = r["metriques"]
        row = " | ".join(f"{m[c]:.3f}" for c in cols)
        L.append(f"| `{r['run']}` | {row} | {r['latence_par_question_s']:.2f} s |")
        if r["run"] == "sparse_seul":
            base = m
    L += ["", "## recall@10 par type de question", "",
          "| configuration | " + " | ".join(types) + " |",
          "|---|" + "---|" * len(types)]
    for r in runs:
        pt = r["metriques"]["par_type"]
        L.append(f"| `{r['run']}` | " + " | ".join(
            f"{pt[t]['recall@10']:.2f}" if t in pt else "—" for t in types) + " |")
    return "\n".join(L) + "\n"


def main():
    only = sys.argv[1:] or None
    runs = []
    for name, ov in CONFIGS:
        if only and name not in only:
            continue
        print(f"» {name} …", flush=True)
        d = run(name, ov)
        if d:
            m = d["metriques"]
            print(f"   recall@10={m['recall@10']:.3f}  MRR={m['MRR']:.3f}  ({d['duree_s']}s)", flush=True)
            runs.append(d)
    if runs:
        out = RESULTS / "ablation.md"
        out.write_text(table(runs), encoding="utf-8")
        print(f"\n-> {out}")


if __name__ == "__main__":
    main()
