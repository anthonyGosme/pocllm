"""Index BM25 (bm25s) avec tokenisation protégeant les codes formels.

Le tokenizer par défaut découpe sur tout non-alphanumérique. Sur ce corpus il
transformerait `XVII-bis` en `xvii` + `bis`, `R-XVII` en `r` + `xvii`, et
`surplus_iff_intermediate` en trois mots. Ce sont précisément les tokens à
IDF maximale, ceux sur lesquels repose l'avantage du sparse (q011, q013) :
les casser reviendrait à mesurer un BM25 amputé de ce qui le rend utile ici.
"""
from __future__ import annotations
import json, re
from pathlib import Path

import bm25s, Stemmer

ROOT = Path(__file__).resolve().parents[3]
CHUNKS = ROOT / "data" / "chunks"
INDEX = ROOT / "data" / "index"

# Motifs préservés tels quels, avant tout découpage.
PROTECTED = re.compile(
    r"(?:\b(?:R|NT|Φ)-[IVXLC]{1,7}(?:-bis|-ter|[ab])?\b"      # R-XVII, NT-V
    r"|\b[IVXLC]{2,7}-(?:bis|ter)\b"                           # XVII-bis
    r"|\bI-[αβγδν][₀-₉0-9]?\b"                                 # I-β₂
    r"|\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b"                      # surplus_iff_intermediate
    r"|\[\[p\.\d+\]\])"                                        # ancre de pagination
)
_stemmer = Stemmer.Stemmer("french")


def tokenize_naive(text: str) -> list[str]:
    """Tokenisation ordinaire, sans protection des codes. Sert uniquement à
    mesurer ce que coûte de ne pas les protéger (ablation du tokenizer)."""
    return _plain(text)


def tokenize(text: str) -> list[str]:
    out, last = [], 0
    for m in PROTECTED.finditer(text):
        out += _plain(text[last:m.start()])
        out.append(m.group(0).lower().replace("[[p.", "p").rstrip("]"))
        last = m.end()
    out += _plain(text[last:])
    return out


def _plain(s: str) -> list[str]:
    words = [w for w in re.split(r"[^0-9A-Za-zÀ-ÿ]+", s.lower()) if len(w) > 1]
    return _stemmer.stemWords(words)


class SparseIndex:
    def __init__(self, k1=1.5, b=0.75, protect_codes=True):
        self.k1, self.b = k1, b
        self.tok = tokenize if protect_codes else tokenize_naive
        self.retriever = None
        self.ids: list[str] = []

    def build(self, chunks: list[dict]):
        self.ids = [c["chunk_id"] for c in chunks]
        corpus = [self.tok((c.get("header", "") + " " + c["text"])) for c in chunks]
        self.retriever = bm25s.BM25(k1=self.k1, b=self.b)
        self.retriever.index(corpus)
        return self

    def search(self, query: str, k=50):
        q = self.tok(query)
        res, scores = self.retriever.retrieve([q], k=min(k, len(self.ids)))
        return [(self.ids[i], float(s)) for i, s in zip(res[0], scores[0])]


def load_chunks(*names) -> list[dict]:
    out = []
    for n in names:
        p = CHUNKS / f"{n}.jsonl"
        if p.exists():
            out += [json.loads(l) for l in p.open(encoding="utf-8")]
    return out


if __name__ == "__main__":
    print("=== contrôle de tokenisation ===")
    for s in ["Que dit XVII-bis face à XLVII ?",
              "le théorème surplus_iff_intermediate et R-XVII",
              "I-β₂ pose la non-autarcie",
              "voir [[p.429]] des Fondements",
              "la clôture opérationnelle des clôtures"]:
        print(f"  {s:52s} -> {tokenize(s)}")
