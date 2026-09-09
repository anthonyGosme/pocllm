"""Retrieval hybride : dense + sparse + fusion RRF + reranking.

Chaque étage se coupe indépendamment par la config — c'est l'objectif numéro un
du POC (§6) et la condition pour produire un tableau d'ablation complet.
Rien n'est caché derrière un framework : la fusion et le RRF sont écrits ici.
"""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
INDEX = ROOT / "data" / "index"


@dataclass
class Stage:
    name: str
    kept: int
    detail: str = ""


@dataclass
class Result:
    chunk_id: str
    score: float
    rank_dense: int | None = None
    rank_sparse: int | None = None
    rank_fused: int | None = None
    rerank_score: float | None = None


@dataclass
class Trace:
    """Trace d'exécution : quel étage a produit quoi. Sans elle, une ablation
    donne des nombres sans explication."""
    stages: list[Stage] = field(default_factory=list)

    def add(self, name, kept, detail=""):
        self.stages.append(Stage(name, kept, detail))

    def __str__(self):
        return " -> ".join(f"{s.name}({s.kept}){(' ' + s.detail) if s.detail else ''}"
                           for s in self.stages)


def rrf(rankings: list[list[str]], k: int = 60,
        weights: list[float] | None = None) -> dict[str, float]:
    """Reciprocal Rank Fusion.

    `k` amortit le poids des premiers rangs : petit k = confiance aux têtes de
    liste, grand k = plus de place à la diversité. Paramètre exposé et testé (§6).

    `weights` : le RRF canonique pondère les branches à égalité, ce qui fait
    qu'une branche faible DILUE une branche forte au lieu de la compléter —
    observé sur ce corpus, où l'hybride tombait sous le sparse seul. Les poids
    permettent de mesurer ce phénomène plutôt que de le subir. Défaut 1.0
    partout, donc identique au RRF canonique."""
    w = weights or [1.0] * len(rankings)
    out: dict[str, float] = {}
    for ranking, wi in zip(rankings, w):
        for rank, cid in enumerate(ranking, start=1):
            out[cid] = out.get(cid, 0.0) + wi / (k + rank)
    return out


class HybridRetriever:
    def __init__(self, chunks, sparse=None, dense=None, ids=None):
        self.chunks = {c["chunk_id"]: c for c in chunks}
        self.sparse = sparse
        self.dense = dense                       # matrice (N, d) normalisée
        self.ids = ids or []
        self._emb = None

    def _embed_query(self, q, model):
        from pocllm.index.dense import prefixes, register
        if self._emb is None:
            from fastembed import TextEmbedding
            register(model)
            self._emb = TextEmbedding(model)
        q_prefix, _ = prefixes(model)
        v = np.asarray(next(iter(self._emb.embed([q_prefix + q]))), dtype=np.float32)
        return v / (np.linalg.norm(v) + 1e-9)

    def search(self, query: str, cfg: dict) -> tuple[list[Result], Trace]:
        r = cfg["retrieval"]
        tr = Trace()
        dense_rank: list[str] = []
        sparse_rank: list[str] = []

        if r["dense"]["enabled"] and self.dense is not None:
            model = r["dense"]["models"][r["dense"]["profile"]]
            qv = self._embed_query(query, model)
            sims = self.dense @ qv
            k = min(r["dense"]["top_k"], len(sims))
            top = np.argpartition(-sims, k - 1)[:k]
            top = top[np.argsort(-sims[top])]
            dense_rank = [self.ids[i] for i in top]
            tr.add("dense", len(dense_rank), f"top={sims[top[0]]:.3f}")

        if r["sparse"]["enabled"] and self.sparse is not None:
            hits = self.sparse.search(query, k=r["sparse"]["top_k"])
            sparse_rank = [cid for cid, _ in hits]
            tr.add("sparse", len(sparse_rank), f"top={hits[0][1]:.2f}" if hits else "")

        legs = [x for x in (dense_rank, sparse_rank) if x]
        if not legs:
            return [], tr
        if len(legs) == 1:
            order = legs[0]
            tr.add("fusion", len(order), "un seul étage actif, non fusionné")
        elif r["fusion"]["enabled"]:
            wd, ws = r["fusion"].get("w_dense", 1.0), r["fusion"].get("w_sparse", 1.0)
            w = [wd if leg is dense_rank else ws for leg in legs]
            scores = rrf(legs, k=r["fusion"]["k"], weights=w)
            order = sorted(scores, key=lambda c: -scores[c])
            tr.add("rrf", len(order), f"k={r['fusion']['k']} w={wd}/{ws}")
        else:
            seen, order = set(), []
            for cid in [c for pair in zip(*legs) for c in pair]:   # entrelacement
                if cid not in seen:
                    seen.add(cid); order.append(cid)
            tr.add("interleave", len(order), "fusion désactivée")

        di = {c: i + 1 for i, c in enumerate(dense_rank)}
        si = {c: i + 1 for i, c in enumerate(sparse_rank)}
        res = [Result(c, 1.0 / (i + 1), di.get(c), si.get(c), i + 1)
               for i, c in enumerate(order)]

        if r["rerank"]["enabled"]:
            prof = r["rerank"]["profile"]
            n = r["rerank"]["top_n"][prof] if isinstance(r["rerank"]["top_n"], dict) else r["rerank"]["top_n"]
            cand = res[:n]
            from pocllm.retrieve.rerank import score_pairs
            docs = [(self.chunks[c.chunk_id].get("header", "") + "\n" +
                     self.chunks[c.chunk_id]["text"]) for c in cand]
            sc = score_pairs(query, docs, r["rerank"]["models"][prof])
            for c, s in zip(cand, sc):
                c.rerank_score = float(s)
            cand.sort(key=lambda c: -c.rerank_score)
            res = cand + res[n:]
            tr.add("rerank", len(cand), f"{prof}, top_n={n}")

        keep = r["rerank"].get("keep", 10)
        return res[:keep], tr


def load(collection: str, profile="fast", k1=1.5, b=0.75, protect_codes=True):
    from pocllm.index.sparse import SparseIndex, load_chunks
    chunks = load_chunks(collection)
    idx = SparseIndex(k1=k1, b=b, protect_codes=protect_codes).build(chunks)
    npy = INDEX / f"{collection}.{profile}.npy"
    ids_p = INDEX / f"{collection}.{profile}.ids.json"
    M = np.load(npy) if npy.exists() else None
    ids = json.loads(ids_p.read_text()) if ids_p.exists() else []
    return HybridRetriever(chunks, sparse=idx, dense=M, ids=ids)
