"""Helpers partagés par les ingesteurs."""
from __future__ import annotations
import re, unicodedata

CHARS_PER_TOKEN = 4.2


def normalize(raw: str) -> str:
    """Normalisation MINIMALE : préserve ∎ ◇ ≈ ₁₂₃ αβγδ τ Φ (cf. q015)."""
    t = unicodedata.normalize("NFC", raw.replace("\r\n", "\n").replace("\r", "\n"))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n{4,}", "\n\n\n", t).strip()


def split_long(text: str, base: int, budget: int, overlap: int):
    """Découpe en respectant les frontières de paragraphe, en gardant l'offset absolu."""
    if len(text) <= budget:
        yield base, text
        return
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
