"""Ancrage de la vérité terrain : sonde textuelle -> (doc_id, span).

Le §4 demandait d'annoter des `expected_doc_ids`. Deux défauts : les
identifiants de chunk changent à chaque rechunking (or le §5 impose de comparer
deux découpages), et annoter 60 à 100 questions x 2-4 sources à la main est le
genre de tâche qui ne se fait jamais.

Ici chaque source porte une `probe` : une phrase littérale et distinctive du
passage d'or. Ce script la localise dans data/docs/ et en DÉRIVE le span. La
sonde est écrite une fois, se vérifie toute seule, et survit à tout rechunking.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "data" / "docs"
EVAL = ROOT / "evals" / "eval_v0_echantillon.jsonl"


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def load_docs():
    out = {}
    for p in sorted(DOCS.glob("*.txt")):
        raw = p.read_text(encoding="utf-8")
        out[p.stem] = (raw, fold(raw))
    return out


def locate(probe: str, docs, restrict: str | None = None):
    """Retourne [(doc_id, start, end)] pour chaque occurrence de la sonde."""
    fp = fold(probe)
    if not fp:
        return []
    hits = []
    for doc_id, (raw, folded) in docs.items():
        if restrict and restrict not in doc_id:
            continue
        i = folded.find(fp)
        while i != -1:
            # ré-alignement approximatif sur le texte brut (le folding préserve l'ordre)
            ratio = len(raw) / max(len(folded), 1)
            s = max(0, int(i * ratio) - 40)
            e = min(len(raw), int((i + len(fp)) * ratio) + 40)
            hits.append((doc_id, s, e))
            i = folded.find(fp, i + 1)
            if len(hits) > 40:
                return hits
    return hits


def main(write=False):
    docs = load_docs()
    rows = [json.loads(l) for l in EVAL.open(encoding="utf-8")]
    print(f"{len(docs)} documents | {len(rows)} questions\n")
    n_ok = n_probe = n_miss = 0
    for q in rows:
        for src in q["expected_sources"]:
            probe = src.get("probe")
            if not probe:
                n_probe += 1
                print(f"  ..... {q['id']} sonde absente : {src['work'][:52]}")
                continue
            hits = locate(probe, docs, src.get("doc_hint"))
            if not hits and src.get("doc_hint"):
                hits = locate(probe, docs)      # repli : indice trop strict
            if not hits:
                n_miss += 1
                print(f"  ECHEC {q['id']} sonde introuvable : « {probe[:56]} »")
            else:
                n_ok += 1
                src["doc_id"], src["span"] = hits[0][0], [hits[0][1], hits[0][2]]
                src["n_occurrences"] = len(hits)
                if len(hits) > 6:
                    print(f"  LARGE {q['id']} sonde peu discriminante ({len(hits)} occ.) : « {probe[:44]} »")
    print(f"\nancrées {n_ok} | sondes à écrire {n_probe} | introuvables {n_miss}")
    if write and not n_miss:
        with EVAL.open("w", encoding="utf-8") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print("spans écrits dans le jeu d'éval")
    return 1 if n_miss else 0


if __name__ == "__main__":
    sys.exit(main(write="--write" in sys.argv))
