from typing import Protocol

import ollama

from ragpdf.config import settings


class LLMProvider(Protocol):
    def chat(self, messages: list[dict], temperature: float = 0.0) -> str: ...


class OllamaProvider:
    def __init__(self, model: str | None = None, host: str | None = None) -> None:
        self.model = model or settings.ollama_model
        self.client = ollama.Client(host=host or settings.ollama_host)

    def chat(self, messages: list[dict], temperature: float = 0.0) -> str:
        response = self.client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": temperature},
        )
        return response["message"]["content"]

    def stream(self, messages: list[dict], temperature: float = 0.0):
        """Yield response tokens as they arrive."""
        for chunk in self.client.chat(
            model=self.model,
            messages=messages,
            options={"temperature": temperature},
            stream=True,
        ):
            yield chunk["message"]["content"]


def get_llm() -> LLMProvider:
    """Factory — returns the configured LLM provider."""
    # In Act 2, we read a LLM_PROVIDER env var and return Ollama or OpenAI
    return OllamaProvider()