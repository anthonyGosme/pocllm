"""Jalon 8 — taux d'attribution non ancrée.

Critère de sortie du cadrage. Le jeu d'éval porte déjà, sur chaque question
piège, un champ `must_not_attribute` : les affirmations que le système ne doit
jamais endosser. On les soumet au vérificateur, avec les passages que le
retrieval remonte réellement pour la question.

Le verdict attendu est CONTREDIT ou ABSENT — jamais SOUTENU. Un SOUTENU est une
attribution non ancrée qui serait passée.

On soumet aussi, en regard, les réponses attendues (`expected_answer`), qui
elles doivent être SOUTENUES : un vérificateur qui bloque tout serait inutile.
"""
from __future__ import annotations
import argparse, json, os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import yaml                                                        # noqa: E402
import anthropic                                                   # noqa: E402
from pocllm.llm import load_dotenv                                 # noqa: E402
from pocllm.mcp._commun import chercher, envelopper                # noqa: E402
from pocllm.guardrails.ancrage import verifier                     # noqa: E402

EVAL = ROOT / "evals" / "eval_v0_echantillon.jsonl"
RESULTS = ROOT / "evals" / "results"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="ancrage")
    ap.add_argument("-k", type=int, default=8)
    a = ap.parse_args()
    load_dotenv()
    cfg = yaml.safe_load((ROOT / "config" / "default.yaml").read_text(encoding="utf-8"))
    cl = anthropic.Anthropic(api_key=os.environ["POCLLM_ANTHROPIC_API_KEY"], timeout=600.0)
    modele = cfg["generation"]["model"]

    qs = [json.loads(l) for l in EVAL.open(encoding="utf-8")
          if json.loads(l).get("must_not_attribute")]
    print(f"{len(qs)} questions portant des attributions interdites · modèle {modele}\n", flush=True)

    lignes, t0, cout = [], time.perf_counter(), 0.0
    for i, q in enumerate(qs, 1):
        cols = ["maison", "canon"] if q["corpus"] == "mixte" else [q["corpus"]]
        passages = envelopper(sum((chercher(c, q["question"], k=a.k) for c in cols), []))
        interdites = q["must_not_attribute"]
        r = verifier(cl, modele, interdites, passages)
        cout += r.cout_usd
        fuites = [v for v in r.verifs if v.ancree]        # SOUTENU + citation vérifiée
        lignes.append({"id": q["id"], "type": q["type"], "n_interdites": len(interdites),
                       "fuites": len(fuites),
                       "verdicts": [{"aff": v.affirmation, "verdict": v.verdict,
                                     "cit_ok": v.citation_trouvee, "motif": v.motif}
                                    for v in r.verifs]})
        print(f"  [{i}/{len(qs)}] {q['id']} {q['type'][:17]:17s} "
              f"{len(interdites)} interdites · {r.resume()} · "
              f"{'** FUITE **' if fuites else 'bloquées'}", flush=True)

    dt = time.perf_counter() - t0
    tot = sum(l["n_interdites"] for l in lignes)
    fu = sum(l["fuites"] for l in lignes)
    out = {"run": a.name, "modele": modele, "n_questions": len(lignes),
           "attributions_interdites": tot, "attributions_non_ancrees_passees": fu,
           "taux_attribution_non_ancree": round(fu / tot, 4) if tot else 0.0,
           "cout_usd": round(cout, 4), "duree_s": round(dt, 1), "par_question": lignes}
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{a.name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    print(f"\nattributions interdites soumises : {tot}")
    print(f"passées malgré le vérificateur    : {fu}")
    print(f"TAUX D'ATTRIBUTION NON ANCRÉE     : {out['taux_attribution_non_ancree']:.1%}")
    print(f"coût {out['cout_usd']} $ · {dt/60:.1f} min")
    print(f"-> {RESULTS / (a.name + '.json')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
