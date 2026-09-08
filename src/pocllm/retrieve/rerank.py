"""Cross-encoder avec cache disque des scores.

Mesuré sur cette machine : jina-v2-multilingual à 1,8 paire/s, soit 9,2 h pour
une ablation de 12 configurations à froid. Le cache ramène les passages
suivants à quelques minutes. Le §9 du cadrage jugeait le caching à faible ROI
parce qu'il pensait au trafic utilisateur ; le trafic répétitif de ce POC est
la boucle d'ablation elle-même.
"""
from __future__ import annotations
import hashlib, sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CACHE = ROOT / ".cache"
_models: dict[str, object] = {}
_db = None


def _conn():
    global _db
    if _db is None:
        CACHE.mkdir(parents=True, exist_ok=True)
        _db = sqlite3.connect(CACHE / "rerank.sqlite")
        _db.execute("CREATE TABLE IF NOT EXISTS s (k TEXT PRIMARY KEY, v REAL)")
        _db.commit()
    return _db


def score_pairs(query: str, docs: list[str], model_name: str) -> list[float]:
    db = _conn()
    keys = [hashlib.sha1(f"{model_name}\x00{query}\x00{d}".encode()).hexdigest() for d in docs]
    have: dict[str, float] = {}
    for i in range(0, len(keys), 900):
        b = keys[i:i + 900]
        for k, v in db.execute(f"SELECT k,v FROM s WHERE k IN ({','.join('?'*len(b))})", b):
            have[k] = v
    todo = [i for i, k in enumerate(keys) if k not in have]
    if todo:
        if model_name not in _models:
            from fastembed.rerank.cross_encoder import TextCrossEncoder
            _models[model_name] = TextCrossEncoder(model_name)
        sc = list(_models[model_name].rerank(query, [docs[i] for i in todo]))
        rows = []
        for i, s in zip(todo, sc):
            have[keys[i]] = float(s); rows.append((keys[i], float(s)))
        db.executemany("INSERT OR REPLACE INTO s VALUES (?,?)", rows)
        db.commit()
    return [have[k] for k in keys]


def cache_stats() -> int:
    return _conn().execute("SELECT COUNT(*) FROM s").fetchone()[0]
