"""Jalon 1 — baseline « tout le système maison dans le contexte ».

Le §3 exige ce baseline et demande de le CONSERVER : sur 152 k tokens, mettre le
corpus entier en contexte est une ligne de base forte, et toute la suite doit
s'y comparer. « S'il gagne sur un axe, le noter honnêtement — c'est un résultat,
pas un échec. »

Un avertissement de méthode, qui vaut d'être posé avant les chiffres. Le jeu
d'éval mesure le RETRIEVAL : recall@k sur des spans. Ce baseline n'a pas de
retrieval — tout est déjà là. Les deux ne sont donc PAS comparables sur recall@k,
et prétendre le contraire produirait un tableau flatteur et faux. Les axes
comparables sont : le taux de refus correct sur les questions pièges, le coût,
et la latence. La justesse des réponses libres demandera un juge, qui viendra
après.
"""
from __future__ import annotations
import argparse, json, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import yaml                                                     # noqa: E402
from pocllm.llm import make_provider                            # noqa: E402

EVAL = ROOT / "evals" / "eval_v0_echantillon.jsonl"
RESULTS = ROOT / "evals" / "results"
SOURCES = ("92.txt", "resume12.md", "executive4.md")

CONSIGNE = """Tu réponds à propos du système philosophique « Ontodynamique »,
dont le texte intégral t'est fourni ci-dessus.

Trois règles, dans cet ordre de priorité.

1. N'affirme que ce que le texte fourni soutient. Si la question repose sur une
   prémisse fausse — le texte dit le contraire, ou ne dit rien de tel — refuse et
   explique en quoi la prémisse est fausse. Ne complète jamais par ce qui te
   paraît plausible.
2. Vérifie la POLARITÉ avant d'attribuer une thèse. Le texte contient des
   formules du type « le système ne dit pas que X » : y lire une affirmation de X
   est l'erreur exacte que ces questions traquent.
3. Vérifie le MARQUEUR de force avant de t'appuyer sur un résultat : ∎ démontré,
   ◇ constructible mais non démontré, ≈ conditionnel. Un ◇ n'établit pas une
   nécessité.

Commence impérativement ta réponse par une seule ligne :
VERDICT: repondre
ou
VERDICT: refuser

puis, après un saut de ligne, ta réponse."""


def contexte() -> str:
    return "\n\n".join(
        f"===== {f} =====\n" + (ROOT / "corpus" / "maison" / f).read_text(encoding="utf-8")
        for f in SOURCES)


def verdict(texte: str) -> str:
    tete = texte.strip().splitlines()[0].lower() if texte.strip() else ""
    if "verdict:" in tete:
        return "refuser" if "refuser" in tete else "repondre"
    return "indetermine"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", default="baseline_contexte")
    ap.add_argument("--limit", type=int, default=0, help="ne traiter que les N premières questions")
    ap.add_argument("--types", nargs="*", default=None, help="filtrer sur des types de question")
    a = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "config" / "default.yaml").read_text(encoding="utf-8"))
    prov = make_provider(cfg["generation"])
    ctx = contexte()
    print(f"contexte : {len(ctx)/4.2/1000:.1f} k tokens · modèle {prov.model} · TTL {prov.cache_ttl}",
          flush=True)

    qs = [json.loads(l) for l in EVAL.open(encoding="utf-8")]
    if a.types:
        qs = [q for q in qs if q["type"] in a.types]
    if a.limit:
        qs = qs[:a.limit]

    # Le bloc système porte le point de cache : stable en tête, question en queue.
    systeme = [{"type": "text", "text": ctx}, {"type": "text", "text": CONSIGNE}]

    lignes, t0 = [], time.perf_counter()
    for i, q in enumerate(qs, 1):
        r = prov.generate(systeme, [{"role": "user", "content": q["question"]}],
                          max_tokens=cfg["generation"]["max_tokens"],
                          cache_system=True, effort=cfg["generation"].get("effort"))
        v = verdict(r.text)
        attendu = q.get("expected_behavior", "repondre")
        lignes.append({
            "id": q["id"], "type": q["type"], "verdict": v, "attendu": attendu,
            "correct": v == attendu, "reponse": r.text, "latence_s": round(r.latency_s, 2),
            "usage": {"entree": r.usage.input_tokens, "sortie": r.usage.output_tokens,
                      "cache_ecrit": r.usage.cache_creation_input_tokens,
                      "cache_lu": r.usage.cache_read_input_tokens,
                      "taux_cache": round(r.usage.cache_hit_ratio, 3)},
        })
        print(f"  [{i:2d}/{len(qs)}] {q['id']} {q['type'][:17]:17s} "
              f"verdict={v:11s} attendu={attendu:9s} "
              f"cache_lu={r.usage.cache_read_input_tokens:7d} {r.latency_s:5.1f}s", flush=True)

    dt = time.perf_counter() - t0
    pieges = [l for l in lignes if l["attendu"] == "refuser"]
    out = {
        "run": a.name, "modele": prov.model, "contexte_tokens": int(len(ctx) / 4.2),
        "n_questions": len(lignes), "duree_s": round(dt, 1),
        "refus_correct": round(sum(l["correct"] for l in pieges) / len(pieges), 3) if pieges else None,
        "faux_refus": sum(1 for l in lignes if l["attendu"] == "repondre" and l["verdict"] == "refuser"),
        "tokens_cache_lus": sum(l["usage"]["cache_lu"] for l in lignes),
        "tokens_entree_pleins": sum(l["usage"]["entree"] for l in lignes),
        "latence_p50": sorted(l["latence_s"] for l in lignes)[len(lignes) // 2] if lignes else None,
        "par_question": lignes,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / f"{a.name}.json").write_text(json.dumps(out, ensure_ascii=False, indent=2),
                                            encoding="utf-8")
    print(f"\nrefus correct sur les pièges : {out['refus_correct']}  ({len(pieges)} questions)")
    print(f"faux refus : {out['faux_refus']}")
    print(f"cache : {out['tokens_cache_lus']/1e6:.2f} M tokens lus contre "
          f"{out['tokens_entree_pleins']/1e6:.2f} M facturés plein tarif")
    print(f"latence p50 : {out['latence_p50']} s · total {dt/60:.1f} min")
    print(f"-> {RESULTS / (a.name + '.json')}")


if __name__ == "__main__":
    main()
