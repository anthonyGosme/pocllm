from pathlib import Path

from pocllm.llm.base import LLMResponse, Provider, Usage

_ROOT = Path(__file__).resolve().parents[3]


def load_dotenv(path: Path | None = None) -> int:
    """Charge .env dans l'environnement sans écraser ce qui y est déjà.

    Écrit à la main plutôt qu'en dépendance : le fichier tient en dix lignes et
    une dépendance de plus pour lire des `clé=valeur` ne se justifie pas.
    Les valeurs déjà présentes gagnent, pour qu'un export ponctuel prime.
    """
    import os
    f = path or (_ROOT / ".env")
    if not f.exists():
        return 0
    n = 0
    for ligne in f.read_text(encoding="utf-8").splitlines():
        ligne = ligne.strip()
        if not ligne or ligne.startswith("#") or "=" not in ligne:
            continue
        cle, _, val = ligne.partition("=")
        cle, val = cle.strip(), val.strip().strip("\'\"")
        if cle and val and cle not in os.environ:
            os.environ[cle] = val
            n += 1
    return n


def make_provider(cfg: dict):
    """Fabrique un fournisseur depuis la section `generation` de la config."""
    load_dotenv()
    p = cfg.get("provider", "anthropic")
    if p == "anthropic":
        from pocllm.llm.anthropic_provider import AnthropicProvider
        return AnthropicProvider(model=cfg.get("model", "claude-opus-5"),
                                 thinking=cfg.get("thinking", True),
                                 cache_ttl=cfg.get("cache_ttl", "1h"))
    if p == "ollama":
        from pocllm.llm.ollama_provider import OllamaProvider
        return OllamaProvider(model=cfg.get("model", "llama3.1:8b"))
    raise ValueError(f"fournisseur inconnu : {p}")


__all__ = ["make_provider", "load_dotenv", "LLMResponse", "Provider", "Usage"]
