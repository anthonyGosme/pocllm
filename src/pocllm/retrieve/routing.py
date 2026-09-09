"""Routage de requête par rareté documentaire.

L'ablation du jalon 3 a montré que la meilleure configuration globale
(`hybride_topk200_rerank50`, recall@10 = 0,500) tombe de 1,00 à 0,25 sur les
questions à néologismes, là où le sparse seul était parfait. L'hybride ne réunit
pas les forces des deux étages : il les moyenne, et le dense dilue un signal
lexical sans défaut.

D'où ce routeur. Le signal est la **fréquence documentaire dans le canon** : un
terme que le canon n'emploie presque pas est du vocabulaire maison, et le dense
ne sait pas le représenter. La requête part alors au sparse seul.

Le seuil et l'activation sont dans la config : c'est une ligne d'ablation de
plus, pas une heuristique enfouie.
"""
from __future__ import annotations
import copy, json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / ".cache"


def document_frequencies(collection: str, protect_codes: bool = True) -> Counter:
    """DF par terme, mise en cache : recompter 21 600 chunks coûte ~15 s."""
    CACHE.mkdir(parents=True, exist_ok=True)
    p = CACHE / f"df_{collection}_{'prot' if protect_codes else 'naif'}.json"
    if p.exists():
        return Counter(json.loads(p.read_text(encoding="utf-8")))
    from pocllm.index.sparse import load_chunks, tokenize, tokenize_naive
    tok = tokenize if protect_codes else tokenize_naive
    df: Counter = Counter()
    for c in load_chunks(collection):
        df.update(set(tok(c.get("header", "") + " " + c["text"])))
    p.write_text(json.dumps(df), encoding="utf-8")
    return df


class Router:
    def __init__(self, max_canon_df=5, min_maison_df=2, protect_codes=True,
                 disable_rerank=False):
        self.max_canon_df = max_canon_df
        self.min_maison_df = min_maison_df
        self.disable_rerank = disable_rerank
        self.canon = document_frequencies("canon", protect_codes)
        self.maison = document_frequencies("maison", protect_codes)
        self.protect_codes = protect_codes

    def idiosyncratic_terms(self, query: str) -> list[str]:
        from pocllm.index.sparse import tokenize, tokenize_naive
        tok = tokenize if self.protect_codes else tokenize_naive
        return [t for t in set(tok(query))
                if self.canon.get(t, 0) <= self.max_canon_df
                and self.maison.get(t, 0) >= self.min_maison_df]

    def route(self, query: str, cfg: dict) -> tuple[dict, str]:
        """Retourne (config effective, motif). La config n'est copiée que si le
        routage change quelque chose — sinon on renvoie l'objet d'origine."""
        terms = self.idiosyncratic_terms(query)
        if not terms:
            return cfg, "hybride"
        out = copy.deepcopy(cfg)
        out["retrieval"]["dense"]["enabled"] = False
        # Couper le dense ne suffit pas : le cross-encoder réordonne ensuite un
        # classement lexical qui était déjà bon. Mesuré — router sans couper le
        # reranker laissait les néologismes à 0,25 au lieu de 1,00.
        if self.disable_rerank:
            out["retrieval"]["rerank"]["enabled"] = False
        return out, "sparse (termes hors canon : " + ", ".join(sorted(terms)[:4]) + ")"
