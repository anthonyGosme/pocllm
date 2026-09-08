from pocllm.llm.base import LLMResponse, Provider, Usage


def make_provider(cfg: dict):
    """Fabrique un fournisseur depuis la section `generation` de la config."""
    p = cfg.get("provider", "anthropic")
    if p == "anthropic":
        from pocllm.llm.anthropic_provider import AnthropicProvider
        return AnthropicProvider(model=cfg.get("model", "claude-opus-5"),
                                 thinking=cfg.get("thinking", True))
    if p == "ollama":
        from pocllm.llm.ollama_provider import OllamaProvider
        return OllamaProvider(model=cfg.get("model", "llama3.1:8b"))
    raise ValueError(f"fournisseur inconnu : {p}")


__all__ = ["make_provider", "LLMResponse", "Provider", "Usage"]
