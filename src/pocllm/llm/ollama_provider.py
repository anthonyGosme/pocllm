"""Fournisseur Ollama (local).

Sert surtout au jalon 10 : le §A2A exige deux agents « dans des process
distincts », de préférence sur des modèles différents. Un agent sur API et un
agent local satisfont la contrainte sans doubler le budget.

Avertissement mesuré : sur ce CPU Intel sans GPU, un 7B quantifié tourne à
4-7 tok/s, soit 1 à 2 minutes par réponse. Inutilisable pour évaluer 100
questions, acceptable pour une démonstration d'échange asynchrone.
"""
from __future__ import annotations
import json, subprocess, time

from pocllm.llm.base import LLMResponse, Usage


class OllamaProvider:
    name = "ollama"

    def __init__(self, model="llama3.1:8b", host="http://localhost:11434", timeout=900):
        self.model, self.host, self.timeout = model, host, timeout

    def generate(self, system, messages, max_tokens=16000, cache_system=False, effort=None):
        if not isinstance(system, str):
            system = "\n\n".join(b["text"] for b in system)
        payload = {"model": self.model, "stream": False,
                   "messages": [{"role": "system", "content": system}] + [
                       {"role": m["role"],
                        "content": m["content"] if isinstance(m["content"], str)
                        else "".join(c.get("text", "") for c in m["content"])}
                       for m in messages],
                   "options": {"num_predict": max_tokens}}
        t = time.perf_counter()
        p = subprocess.run(["curl", "-sS", "-m", str(self.timeout),
                            f"{self.host}/api/chat", "-d", json.dumps(payload)],
                           capture_output=True, text=True)
        dt = time.perf_counter() - t
        d = json.loads(p.stdout or "{}")
        return LLMResponse(
            text=d.get("message", {}).get("content", ""),
            usage=Usage(d.get("prompt_eval_count", 0), d.get("eval_count", 0)),
            model=self.model, stop_reason=d.get("done_reason"), latency_s=dt)
