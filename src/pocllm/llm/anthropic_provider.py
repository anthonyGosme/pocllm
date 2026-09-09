"""Fournisseur Anthropic.

Deux détails qui coûtent cher si on les rate :

1. `ANTHROPIC_BASE_URL` est défini dans cet environnement et pointe vers le
   proxy de Claude Code, qui n'est pas une API généraliste. Un client construit
   sans argument le récupérerait silencieusement et échouerait de façon
   incompréhensible. On l'ignore sauf demande explicite.

2. Le prompt caching est un match de PRÉFIXE : tout octet modifié en amont
   invalide la suite. Le corpus va donc en tête du bloc système, la question
   variable en queue — c'est ce qui rend le baseline du jalon 1 (tout le
   système maison en contexte) économiquement tenable.
"""
from __future__ import annotations
import os, time

from pocllm.llm.base import LLMResponse, Usage

# Adaptatif sur Opus 5 / Sonnet 5 / Opus 4.x ; budget_tokens y est REJETÉ (400).
ADAPTIVE_THINKING = {"claude-opus-5", "claude-opus-4-8", "claude-opus-4-7",
                     "claude-sonnet-5", "claude-fable-5-1"}


class AnthropicProvider:
    name = "anthropic"

    def __init__(self, model="claude-opus-5", api_key=None, base_url=None,
                 thinking=True, timeout=600.0, cache_ttl="1h"):
        import anthropic
        key = api_key or os.environ.get("POCLLM_ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "Aucune clé API. Exporter POCLLM_ANTHROPIC_API_KEY (préféré, pour ne pas "
                "entrer en conflit avec l'environnement Claude Code) ou ANTHROPIC_API_KEY.")
        kw = {"api_key": key, "timeout": timeout}
        if base_url:                       # jamais hérité de l'environnement
            kw["base_url"] = base_url
        self.client = anthropic.Anthropic(**kw)
        self.model, self.thinking, self.cache_ttl = model, thinking, cache_ttl

    def generate(self, system, messages, max_tokens=16000, cache_system=False, effort=None,
                 contexte=""):
        # Le bloc système porte le point de cache : stable en tête, volatil en queue.
        if isinstance(system, str):
            system = [{"type": "text", "text": system}]
        if cache_system and system:
            system = [dict(b) for b in system]
            # TTL explicite. Par défaut le cache expire en 5 minutes ; or une passe
            # de 38 questions sur 152 k tokens de contexte dure bien davantage, et
            # le cache expirerait en cours de route — on repaierait alors le
            # contexte plein à chaque question, soit un facteur 5 à 10 sur la note.
            cc = {"type": "ephemeral"}
            if self.cache_ttl:
                cc["ttl"] = self.cache_ttl
            system[-1]["cache_control"] = cc

        kw = dict(model=self.model, max_tokens=max_tokens, system=system, messages=messages)
        if self.thinking and self.model in ADAPTIVE_THINKING:
            kw["thinking"] = {"type": "adaptive", "display": "summarized"}
        if effort:
            kw["output_config"] = {"effort": effort}

        t = time.perf_counter()
        # Streaming : max_tokens élevé + long contexte dépassent sinon le timeout HTTP.
        with self.client.messages.stream(**kw) as s:
            msg = s.get_final_message()
        dt = time.perf_counter() - t

        u = msg.usage
        usage = Usage(u.input_tokens, u.output_tokens,
                      getattr(u, "cache_creation_input_tokens", 0) or 0,
                      getattr(u, "cache_read_input_tokens", 0) or 0)
        from pocllm.llm.couts import enregistrer
        enregistrer(msg.model, usage, contexte)
        return LLMResponse(
            text="".join(b.text for b in msg.content if b.type == "text"),
            thinking="".join(getattr(b, "thinking", "") for b in msg.content if b.type == "thinking"),
            usage=usage, model=msg.model, stop_reason=msg.stop_reason, latency_s=dt)
