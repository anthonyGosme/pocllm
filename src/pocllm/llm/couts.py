"""Comptabilité des coûts d'API, mesurée et non estimée.

Le §4 demande « coût par requête » parmi les métriques d'exploitation. Ce module
existe surtout parce que mes estimations à la main se sont trompées deux fois :
d'abord d'un facteur 1,8 sur le comptage de tokens, puis d'environ 40 % sur la
facture réelle. Un compteur branché sur les `usage` renvoyés par l'API ne se
trompe pas.

Tarifs en dollars par million de tokens (juin 2026).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
JOURNAL = ROOT / "data" / "couts.jsonl"

# (entrée, sortie). Multiplicateurs de cache, vérifiés dans la documentation :
#   écriture TTL 5 min -> x1,25   |   écriture TTL 1 h -> x2,00   |   lecture -> x0,10
# Je les avais tous pris à 1,25, ce qui sous-estimait la facture de 60 % sur les
# écritures — première cause de l'écart entre mes devis et le relevé réel.
TARIFS = {
    "claude-opus-5":   (5.00, 25.00),
    "claude-opus-4-8": (5.00, 25.00),
    "claude-sonnet-5": (2.00, 10.00),
    "claude-haiku-4-5": (1.00, 5.00),
    "claude-fable-5-1": (10.00, 50.00),
}


MULT_ECRITURE = {"5m": 1.25, "1h": 2.00}


def cout(modele: str, entree: int, sortie: int, cache_ecrit: int = 0, cache_lu: int = 0,
         ttl: str = "1h") -> float:
    pin, pout = TARIFS.get(modele, (2.00, 10.00))
    me = MULT_ECRITURE.get(ttl, 1.25)
    return (entree * pin + cache_ecrit * pin * me + cache_lu * pin * 0.10
            + sortie * pout) / 1e6


def enregistrer(modele: str, usage, contexte: str = "") -> float:
    """Journalise un appel. La somme du journal est la dépense réelle du POC."""
    c = cout(modele, usage.input_tokens, usage.output_tokens,
             usage.cache_creation_input_tokens, usage.cache_read_input_tokens)
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    with JOURNAL.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"modele": modele, "contexte": contexte, "cout_usd": round(c, 6),
                            "entree": usage.input_tokens, "sortie": usage.output_tokens,
                            "cache_ecrit": usage.cache_creation_input_tokens,
                            "cache_lu": usage.cache_read_input_tokens}, ensure_ascii=False) + "\n")
    return c


def total() -> dict:
    if not JOURNAL.exists():
        return {"appels": 0, "cout_usd": 0.0}
    lignes = [json.loads(l) for l in JOURNAL.open(encoding="utf-8")]
    par_ctx: dict[str, float] = {}
    for l in lignes:
        par_ctx[l.get("contexte", "")] = par_ctx.get(l.get("contexte", ""), 0.0) + l["cout_usd"]
    return {"appels": len(lignes), "cout_usd": round(sum(l["cout_usd"] for l in lignes), 4),
            "par_contexte": {k: round(v, 4) for k, v in sorted(par_ctx.items(), key=lambda kv: -kv[1])}}
