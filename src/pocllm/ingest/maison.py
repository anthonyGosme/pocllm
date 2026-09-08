"""Ingestion du corpus maison (Ontodynamique).

Deux sorties, volontairement séparées :

  data/docs/<doc_id>.txt      texte normalisé, STABLE — c'est l'espace d'ancrage
  data/chunks/maison.jsonl    chunks, jetables et regénérables

La vérité terrain du jeu d'éval pointe vers (doc_id, span) dans le premier,
jamais vers un identifiant de chunk. C'est ce qui permet de comparer deux
stratégies de découpage (§5) sans réannoter les questions.
"""
from __future__ import annotations
import json, re, sys, unicodedata
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "corpus" / "maison"
DOCS = ROOT / "data" / "docs"
CHUNKS = ROOT / "data" / "chunks"

CHARS_PER_TOKEN = 4.2

# Codes formels du système : R-XVII, XVII-bis, I-β₂, NT-V, LXXVII, Φ-...
CODE_RE = re.compile(
    r"(?:\b(?:R|NT|Φ)-[IVXLC]{1,7}(?:-bis|-ter|[ab])?\b"
    r"|\b[IVXLC]{2,7}(?:-bis|-ter|[ab])?\b"
    r"|\bI-[αβγδν](?:[₀-₉0-9])?\b)"
)
DECL_RE = re.compile(
    r"^(?:noncomputable\s+)?(?:private\s+|protected\s+)?"
    r"(theorem|lemma|def|structure|abbrev|instance|example|inductive|class|axiom)\s+"
    r"([A-Za-z0-9_'\.]+)",
    re.M,
)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    span: tuple[int, int]
    text: str
    header: str          # en-tête contextuel préfixé avant embedding (§5)
    collection: str
    source: str
    version: str         # manuscrit | resume | executive | article | supplement | lean
    lang: str
    kind: str
    section_path: list[str]
    codes: list[str]
    decl_name: str | None


def normalize(raw: str) -> str:
    """Normalisation MINIMALE : on préserve ∎ ◇ ≈ ₁₂₃ αβγδ τ Φ.

    Les effacer casserait q015, qui teste précisément la survie des marqueurs
    de force à travers le pipeline.
    """
    t = unicodedata.normalize("NFC", raw.replace("\r\n", "\n").replace("\r", "\n"))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n{4,}", "\n\n\n", t).strip()


def codes_in(text: str) -> list[str]:
    out, seen = [], set()
    for m in CODE_RE.findall(text):
        if m not in seen:
            seen.add(m); out.append(m)
    return out


def _split_long(text: str, base: int, budget: int, overlap: int):
    """Découpe une section trop longue en respectant les frontières de paragraphe."""
    if len(text) <= budget:
        yield base, text; return
    start = 0
    while start < len(text):
        end = min(start + budget, len(text))
        if end < len(text):
            cut = text.rfind("\n\n", start + budget // 2, end)
            if cut == -1:
                cut = text.rfind(" ", start + budget // 2, end)
            if cut != -1:
                end = cut
        piece = text[start:end]
        if piece.strip():
            yield base + start, piece
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)


def chunk_prose(doc_id, text, meta, budget, overlap):
    """Découpage structurel piloté par les titres markdown, chemin conservé."""
    heads = [(m.start(), len(m.group(1)), m.group(2).strip())
             for m in re.finditer(r"^(#{1,6}) +(.+)$", text, re.M)]
    bounds = [h[0] for h in heads] + [len(text)]
    path: dict[int, str] = {}
    out = []
    if not heads:                       # document sans titre
        heads, bounds = [(0, 1, meta["source"])], [0, len(text)]
    for i, (pos, lvl, title) in enumerate(heads):
        path = {k: v for k, v in path.items() if k < lvl}
        path[lvl] = title
        section = text[pos:bounds[i + 1]]
        sec_path = [path[k] for k in sorted(path)]
        for off, piece in _split_long(section, pos, budget, overlap):
            out.append((off, piece, sec_path, None))
    return out


def chunk_lean(doc_id, text, meta, budget, overlap):
    """Une déclaration = un chunk. Le préambule (namespace/variable/open) est
    répété en chevauchement, sinon la déclaration est illisible hors contexte."""
    decls = list(DECL_RE.finditer(text))
    if not decls:
        return [(0, text, [meta["source"]], None)]
    preamble = text[: decls[0].start()].strip()
    head = "\n".join(l for l in preamble.splitlines()
                     if l.startswith(("import", "open", "namespace", "variable", "universe")))[:600]
    out = []
    for i, m in enumerate(decls):
        start = m.start()
        # remonter sur le docstring /-- ... -/ ou les commentaires -- qui précèdent
        pre = text[: start].rstrip()
        j = pre.rfind("/--")
        if j != -1 and pre.endswith("-/") and start - j < 1500:
            start = j
        else:
            lines = pre.splitlines()
            k = len(lines)
            while k > 0 and lines[k - 1].lstrip().startswith("--"):
                k -= 1
            if k < len(lines):
                start = len(pre) - sum(len(l) + 1 for l in lines[k:])
        end = decls[i + 1].start() if i + 1 < len(decls) else len(text)
        body = text[start:end]
        for off, piece in _split_long(body, start, budget, overlap):
            out.append((off, piece, [meta["source"], m.group(2)], m.group(2)))
    for o in out:
        o and None
    return [(off, (head + "\n\n" + p) if head else p, sp, dn) for off, p, sp, dn in out]


def load_pdf(path: Path) -> str:
    from pypdf import PdfReader
    return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)


# source -> (doc_id, version, lang, kind)
PLAN = {
    "92.txt":          ("maison_manuscrit",  "manuscrit", "fr", "prose"),
    "resume12.md":     ("maison_resume",     "resume",    "fr", "prose"),
    "executive4.md":   ("maison_executive",  "executive", "fr", "prose"),
    "axiome_1_en_2_tentative (5).pdf": ("maison_article_en",    "article",    "en", "prose"),
    "axiome_1_en_2_tentative (4).pdf": ("maison_supplement_en", "supplement", "en", "prose"),
}


def main(target_tokens=400, overlap_tokens=60, context_header=True):
    DOCS.mkdir(parents=True, exist_ok=True)
    CHUNKS.mkdir(parents=True, exist_ok=True)
    budget = int(target_tokens * CHARS_PER_TOKEN)
    overlap = int(overlap_tokens * CHARS_PER_TOKEN)

    tasks = []
    for name, (doc_id, version, lang, kind) in PLAN.items():
        p = RAW / name
        if not p.exists():
            print(f"  MANQUANT {name}", file=sys.stderr); continue
        tasks.append((p, doc_id, version, lang, kind))
    for p in sorted(RAW.glob("*.lean")):
        tasks.append((p, "maison_lean_" + re.sub(r"\W+", "_", p.stem).lower(), "lean", "en", "lean"))

    rows, stats = [], {}
    for p, doc_id, version, lang, kind in tasks:
        raw = load_pdf(p) if p.suffix == ".pdf" else p.read_text(encoding="utf-8", errors="replace")
        text = normalize(raw)
        (DOCS / f"{doc_id}.txt").write_text(text, encoding="utf-8")
        meta = {"source": p.name}
        pieces = (chunk_lean if kind == "lean" else chunk_prose)(doc_id, text, meta, budget, overlap)
        n = 0
        for idx, (off, piece, sec_path, decl) in enumerate(pieces):
            body = piece.strip()
            if len(body) < 40:
                continue
            header = f"[Ontodynamique | {p.name} | {' > '.join(sec_path[:3])}]"
            rows.append(Chunk(
                chunk_id=f"{doc_id}#c{idx:04d}", doc_id=doc_id,
                span=(off, off + len(piece)), text=body,
                header=header if context_header else "",
                collection="maison", source=p.name, version=version, lang=lang,
                kind=kind, section_path=sec_path, codes=codes_in(body), decl_name=decl,
            ).__dict__)
            n += 1
        stats[p.name] = n

    out = CHUNKS / "maison.jsonl"
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows, stats, out


if __name__ == "__main__":
    rows, stats, out = main()
    tot_chars = sum(len(r["text"]) for r in rows)
    print(f"{len(rows)} chunks -> {out}")
    print(f"~{tot_chars/CHARS_PER_TOKEN/1000:.0f} k tokens indexés, "
          f"moyenne {tot_chars/max(len(rows),1)/CHARS_PER_TOKEN:.0f} tokens/chunk")
    print("\npar source (top 12) :")
    for k, v in sorted(stats.items(), key=lambda kv: -kv[1])[:12]:
        print(f"  {k[:44]:44s} {v:5d}")
