from dataclasses import dataclass

from ragpdf.generation.llm import get_llm
from ragpdf.generation.prompts import build_messages
from ragpdf.retrieval.retriever import Retriever


@dataclass
class RAGAnswer:
    question: str
    answer: str
    hits: list          # the retrieved chunks
    model: str


class RAGChain:
    def __init__(self, retriever: Retriever | None = None) -> None:
        self.retriever = retriever or Retriever()
        self.llm = get_llm()

    def ask(self, question: str, top_k: int = 5) -> RAGAnswer:
        hits = self.retriever.retrieve(question, top_k=top_k)
        messages = build_messages(question, hits)
        answer = self.llm.chat(messages, temperature=0.0)
        return RAGAnswer(
            question=question,
            answer=answer,
            hits=hits,
            model=getattr(self.llm, "model", "unknown"),
        )

    def stream(self, question: str, top_k: int = 5):
        """Stream the answer token by token."""
        hits = self.retriever.retrieve(question, top_k=top_k)
        messages = build_messages(question, hits)
        return hits, self.llm.stream(messages, temperature=0.0)