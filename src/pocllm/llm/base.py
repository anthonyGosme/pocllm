"""Abstraction fournisseur (§8).

Le cadrage demande « une abstraction fine permettant d'en changer, notamment
pour donner des modèles différents aux deux agents A2A ». Fine, donc : une
méthode, un objet de réponse, et surtout les compteurs de cache exposés — sans
eux le jalon 9 ne peut rien mesurer.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    cache_creation_input_tokens: int = 0
    cache_read_input_tokens: int = 0

    @property
    def cache_hit_ratio(self) -> float:
        billed = self.input_tokens + self.cache_read_input_tokens
        return self.cache_read_input_tokens / billed if billed else 0.0


@dataclass
class LLMResponse:
    text: str
    usage: Usage = field(default_factory=Usage)
    model: str = ""
    stop_reason: str | None = None
    latency_s: float = 0.0
    thinking: str = ""


class Provider(Protocol):
    name: str
    model: str

    def generate(self, system, messages, max_tokens: int = 16000,
                 cache_system: bool = False, effort: str | None = None) -> LLMResponse:
        ...
