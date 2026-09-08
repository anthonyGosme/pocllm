"""Index dense (fastembed / ONNX Runtime, sans torch).

Sur cette machine (Intel x86_64, pas de GPU) PyTorch n'a plus de wheel depuis
la 2.2.2 : toute la pile passe donc par ONNX Runtime. Deux profils, parce que
réembedder 23 k chunks à chaque essai de découpage est le goulot d'étranglement
du jalon 3 (§5 impose de comparer au moins deux stratégies).

Les vecteurs sont mis en cache sur disque, clés par (modèle, hash du texte) :
un rechunking partiel ne réembedde que ce qui a bougé.
"""
from __future__ import annotations
import hashlib, json, sqlite3, sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
CHUNKS = ROOT / "data" / "chunks"
INDEX = ROOT / "data" / "index"
CACHE = ROOT / ".cache"

PROFILES = {
    "fast":    ("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2", 384),
    "quality": ("intfloat/multilingual-e5-large", 1024),
}


class EmbeddingCache:
    def __init__(self, path: Path, model: str, dim: int):
        CACHE.mkdir(parents=True, exist_ok=True)
        self.model, self.dim = model, dim
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS emb (k TEXT PRIMARY KEY, v BLOB)")
        self.db.commit()

    def key(self, text: str) -> str:
        return hashlib.sha1(f"{self.model}\x00{text}".encode()).hexdigest()

    def get_many(self, texts):
        keys = [self.key(t) for t in texts]
        found = {}
        for i in range(0, len(keys), 900):
            batch = keys[i:i + 900]
            q = ",".join("?" * len(batch))
            for k, v in self.db.execute(f"SELECT k,v FROM emb WHERE k IN ({q})", batch):
                found[k] = np.frombuffer(v, dtype=np.float32)
        return keys, found

    def put_many(self, keys, vecs):
        self.db.executemany("INSERT OR REPLACE INTO emb VALUES (?,?)",
                            [(k, v.astype(np.float32).tobytes()) for k, v in zip(keys, vecs)])
        self.db.commit()


def embed_chunks(chunks: list[dict], profile="fast", batch=64, log=print) -> np.ndarray:
    from fastembed import TextEmbedding
    model, dim = PROFILES[profile]
    texts = [(c.get("header", "") + "\n" + c["text"]).strip() for c in chunks]
    cache = EmbeddingCache(CACHE / "emb.sqlite", model, dim)
    keys, found = cache.get_many(texts)
    todo = [i for i, k in enumerate(keys) if k not in found]
    log(f"  {len(found)} vecteurs en cache, {len(todo)} à calculer")

    if todo:
        emb = TextEmbedding(model)
        done, new_keys, new_vecs = 0, [], []
        for i0 in range(0, len(todo), batch):
            idx = todo[i0:i0 + batch]
            vecs = list(emb.embed([texts[i] for i in idx]))
            for i, v in zip(idx, vecs):
                found[keys[i]] = np.asarray(v, dtype=np.float32)
                new_keys.append(keys[i]); new_vecs.append(found[keys[i]])
            done += len(idx)
            if len(new_keys) >= 512:
                cache.put_many(new_keys, new_vecs); new_keys, new_vecs = [], []
            if done % 2048 < batch:
                log(f"  {done}/{len(todo)} embeddés", flush=True)
        if new_keys:
            cache.put_many(new_keys, new_vecs)

    M = np.vstack([found[k] for k in keys])
    return M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-9)


def main(profile="fast"):
    INDEX.mkdir(parents=True, exist_ok=True)
    import time
    for name in ("maison", "canon"):
        p = CHUNKS / f"{name}.jsonl"
        if not p.exists():
            continue
        ch = [json.loads(l) for l in p.open(encoding="utf-8")]
        print(f"[{name}] {len(ch)} chunks", flush=True)
        t = time.perf_counter()
        M = embed_chunks(ch, profile, log=lambda m, **k: print(m, flush=True))
        dt = time.perf_counter() - t
        np.save(INDEX / f"{name}.{profile}.npy", M)
        (INDEX / f"{name}.{profile}.ids.json").write_text(
            json.dumps([c["chunk_id"] for c in ch]), encoding="utf-8")
        print(f"[{name}] {M.shape} en {dt/60:.1f} min ({len(ch)/max(dt,1e-9):.1f} chunks/s)", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "fast")
