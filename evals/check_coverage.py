"""Vérifie que chaque question du jeu d'éval a bien ses sources dans l'index.

Sans ce contrôle, une question dont la source manque se lit comme un échec du
retrieval alors que c'est un défaut d'ingestion. C'est exactement le piège dans
lequel sont tombées q005, q007 et q008.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fold(s: str) -> str:
    s = unicodedata.normalize("NFKD", s.lower())
    return re.sub(r"\W+", " ", "".join(c for c in s if not unicodedata.combining(c)))


def load(name):
    p = ROOT / "data" / "chunks" / f"{name}.jsonl"
    return [json.loads(l) for l in p.open(encoding="utf-8")] if p.exists() else []


def main():
    chunks = load("maison") + load("canon")
    if not chunks:
        print("aucun chunk indexé"); return 1
    blob = [(fold(c.get("header", "") + " " + c.get("source", "") + " " +
                  " ".join(map(str, c.get("section_path", []))) + " " + c["text"]), c)
            for c in chunks]

    rows = [json.loads(l) for l in (ROOT / "evals" / "eval_v0_echantillon.jsonl").open(encoding="utf-8")]
    print(f"{len(chunks)} chunks indexés | {len(rows)} questions\n")
    ko = []
    for q in rows:
        miss = []
        for src in q["expected_sources"]:
            work = fold(src["work"])
            # mots discriminants du titre/auteur (>3 lettres)
            keys = [w for w in work.split() if len(w) > 3][:4]
            if not keys:
                continue
            hits = sum(1 for b, _ in blob if all(k in b for k in keys[:2]))
            if hits == 0:
                hits = sum(1 for b, _ in blob if keys[0] in b)
            (miss.append((src["work"], hits)) if hits == 0 else None)
        flag = "OK " if not miss else "MANQUE"
        print(f"  {flag} {q['id']} [{q['type'][:18]:18s}] {q['question'][:56]}")
        for w, h in miss:
            print(f"        -> source absente de l'index : {w}")
        if miss:
            ko.append(q["id"])
    print(f"\n{len(rows)-len(ko)}/{len(rows)} questions couvertes")
    if ko:
        print("à traiter :", ", ".join(ko))
    return 0


if __name__ == "__main__":
    sys.exit(main())
