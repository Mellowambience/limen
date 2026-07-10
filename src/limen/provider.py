from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol


class Provider(Protocol):
    def generate(self, system: str, prompt: str) -> str:
        ...


@dataclass(slots=True)
class OllamaProvider:
    model: str = "qwen2.5:3b"
    base_url: str = "http://localhost:11434"
    timeout_seconds: int = 120

    def generate(self, system: str, prompt: str) -> str:
        endpoint = self.base_url.rstrip("/") + "/api/chat"
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
        }
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(
                request, timeout=self.timeout_seconds
            ) as response:
                data = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(
                "Could not reach local Ollama. Run `ollama serve` and pull the "
                f"configured model ({self.model}). Original error: {exc}"
            ) from exc
        message = data.get("message", {})
        content = str(message.get("content", "")).strip()
        if not content:
            raise RuntimeError("Ollama returned no message content.")
        return content
