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


def fold_mapped(raw: str) -> tuple[str, list[int]]:
    """Replie le texte EN CONSERVANT, pour chaque caractère replié, l'index du
    caractère brut dont il provient.

    Une règle de trois entre longueur repliée et longueur brute ne marche pas :
    le repliement supprime la ponctuation et écrase les espaces de façon non
    uniforme, si bien que la dérive atteint des centaines de caractères dans un
    long document. Mesuré avant correction : 42 spans faux sur 56."""
    out: list[str] = []
    idx: list[int] = []
    prev_space = True
    for i, ch in enumerate(raw):
        dec = unicodedata.normalize("NFKD", ch.lower())
        for c in (c for c in dec if not unicodedata.combining(c)):
            if not (c.isalnum() or c == "_"):
                c = " "
            if c == " ":
                if prev_space:
                    continue
                prev_space = True
            else:
                prev_space = False
            out.append(c)
            idx.append(i)
    while out and out[-1] == " ":
        out.pop(); idx.pop()
    return "".join(out), idx


def load_docs():
    out = {}
    for p in sorted(DOCS.glob("*.txt")):
        raw = p.read_text(encoding="utf-8")
        folded, idx = fold_mapped(raw)
        out[p.stem] = (raw, folded, idx)
    return out


def locate(probe: str, docs, restrict: str | None = None):
    """Retourne [(doc_id, start, end)] pour chaque occurrence de la sonde."""
    fp = fold(probe)
    if not fp:
        return []
    hits = []
    for doc_id, (raw, folded, idx) in docs.items():
        if restrict and restrict not in doc_id:
            continue
        i = folded.find(fp)
        while i != -1:
            # position EXACTE, lue dans la table d'index construite au repliement
            s = idx[i]
            e = idx[min(i + len(fp), len(idx)) - 1] + 1
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
