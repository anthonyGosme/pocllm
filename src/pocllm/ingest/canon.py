"""Ingestion du canon philosophique français depuis Wikisource.

Phase 1 : liste d'œuvres vérifiées présentes, qui garantit que les sources
citées par le jeu d'éval sont dans l'index. Phase 2 (expansion par catégories)
ajoute le volume et les distracteurs.

Une sous-page = un document = une unité canonique (chapitre, partie, section).
L'ancrage de la vérité terrain se fait sur (doc_id, span) dans data/docs/.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from pocllm.ingest.common import CHARS_PER_TOKEN, normalize, split_long
from pocllm.ingest.wikisource import page_text, subpages, category_members, resolve

ROOT = Path(__file__).resolve().parents[3]
DOCS = ROOT / "data" / "docs"
CHUNKS = ROOT / "data" / "chunks"

# (œuvre Wikisource, auteur, titre court) — toutes vérifiées présentes
SEED: list[tuple[str, str, str]] = [
    ("Éthique (Appuhn, 1913)",                          "Spinoza",       "Éthique"),
    ("Critique de la raison pure (trad. Barni)",        "Kant",          "Critique de la raison pure"),
    ("Critique de la raison pratique (trad. Barni)",    "Kant",          "Critique de la raison pratique"),
    ("Fondements de la métaphysique des mœurs",         "Kant",          "Fondements de la métaphysique des mœurs"),
    ("La religion dans les limites de la raison (trad. Tremesaygues)", "Kant", "La religion dans les limites de la raison"),
    ("Méditations métaphysiques",                       "Descartes",     "Méditations métaphysiques"),
    ("Discours de la méthode",                          "Descartes",     "Discours de la méthode"),
    ("Du contrat social/Édition 1762",                  "Rousseau",      "Du contrat social"),
    ("Émile, ou De l’éducation",                        "Rousseau",      "Émile"),
    ("Discours sur l’origine et les fondements de l’inégalité parmi les hommes", "Rousseau", "Discours sur l'inégalité"),
    ("Pensées (Pascal)",                                "Pascal",        "Pensées"),
    ("Essai philosophique concernant l’entendement humain", "Locke",     "Essai sur l'entendement humain"),
    ("De la recherche de la vérité",                    "Malebranche",   "De la recherche de la vérité"),
    ("Monadologie",                                     "Leibniz",       "Monadologie"),
    ("Ainsi parlait Zarathoustra",                      "Nietzsche",     "Ainsi parlait Zarathoustra"),
    ("Par delà le bien et le mal",                      "Nietzsche",     "Par delà le bien et le mal"),
    ("La Généalogie de la morale",                      "Nietzsche",     "Généalogie de la morale"),
    ("De l’esprit des lois (éd. Nourse)",               "Montesquieu",   "De l'esprit des lois"),
    ("Le Monde comme volonté et comme représentation",  "Schopenhauer",  "Le Monde comme volonté et représentation"),
    ("Œuvres de Platon (trad. Cousin)",                 "Platon",        "Œuvres"),
    ("L’Évolution créatrice",                           "Bergson",       "L'Évolution créatrice"),
    ("Essais",                                          "Montaigne",     "Les Essais"),
    ("Essais philosophiques sur l’entendement humain",  "Hume",          "Essais sur l'entendement humain"),
]


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"_+", "_", re.sub(r"\W+", "_", s)).strip("_").lower()[:90]


def ingest(works, target_tokens=400, overlap_tokens=60, context_header=True, log=print, refetch=False):
    DOCS.mkdir(parents=True, exist_ok=True)
    CHUNKS.mkdir(parents=True, exist_ok=True)
    budget, overlap = int(target_tokens * CHARS_PER_TOKEN), int(overlap_tokens * CHARS_PER_TOKEN)
    rows, seen_docs, empty = [], set(), 0

    for work, author, short in works:
        work = resolve(work)
        pages = subpages(work) or [work]
        log(f"  {short:42s} {len(pages):4d} unités")
        for title in pages:
            doc_id = "canon_" + slug(title)
            if doc_id in seen_docs:
                continue
            cached = DOCS / f"{doc_id}.txt"
            # data/docs/ est la couche STABLE : on ne refetch jamais ce qu'on a déjà.
            # C'est ce qui rend le rechunking (§5) possible hors ligne, et ce qui
            # rend cette fonction idempotente.
            if cached.exists() and not refetch:
                text = cached.read_text(encoding="utf-8")
            else:
                text = normalize(page_text(title))
                if len(text) >= 200:
                    cached.write_text(text, encoding="utf-8")
            if len(text) < 200:
                empty += 1
                continue
            seen_docs.add(doc_id)

            unit = title[len(work):].strip("/") or "intégral"
            pages_seen = re.findall(r"\[\[p\.(\d+)\]\]", text)
            header = f"[{author} | {short} | {unit}]"
            for i, (off, piece) in enumerate(split_long(text, 0, budget, overlap)):
                body = piece.strip()
                if len(body) < 40:
                    continue
                loc = re.findall(r"\[\[p\.(\d+)\]\]", piece)
                rows.append({
                    "chunk_id": f"{doc_id}#c{i:04d}", "doc_id": doc_id,
                    "span": [off, off + len(piece)], "text": body,
                    "header": header if context_header else "",
                    "collection": "canon", "source": title, "work": short,
                    "author": author, "unit": unit, "lang": "fr", "kind": "canon",
                    "section_path": [author, short, unit],
                    "pages": loc, "page_range": [pages_seen[0], pages_seen[-1]] if pages_seen else None,
                })
    # Déduplication : Wikisource expose souvent l'œuvre entière ET ses chapitres,
    # donc le même texte est indexé plusieurs fois. On garde l'occurrence dont le
    # titre est le plus profond (unité la plus fine = meilleure citation).
    import hashlib
    best: dict[str, dict] = {}
    for r in rows:
        h = hashlib.sha1(re.sub(r"\s+", " ", r["text"]).strip().encode()).hexdigest()
        prev = best.get(h)
        if prev is None or r["source"].count("/") > prev["source"].count("/"):
            best[h] = r
    dropped = len(rows) - len(best)
    rows = [r for r in rows if best.get(
        hashlib.sha1(re.sub(r"\s+", " ", r["text"]).strip().encode()).hexdigest()) is r]
    log(f"  déduplication : {dropped} chunks redondants retirés")

    out = CHUNKS / "canon.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows, out, empty


if __name__ == "__main__":
    rows, out, empty = ingest(SEED)
    chars = sum(len(r["text"]) for r in rows)
    print(f"\n{len(rows)} chunks -> {out}")
    print(f"~{chars/CHARS_PER_TOKEN/1000:.0f} k tokens | {empty} pages vides ignorées")
