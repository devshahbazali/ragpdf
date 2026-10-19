SYSTEM_PROMPT = """You are a helpful assistant that answers questions strictly based on the provided context.

Rules:
- Only use information from the context below to answer.
- If the context does not contain the answer, reply exactly: "I don't have enough information in the provided documents to answer that."
- Do not make up facts, numbers, or names.
- When you use information, cite the source in the form [file.pdf, p.N].
- Be concise but complete.
"""


def build_context(hits) -> str:
    """Format retrieved chunks into a numbered context block."""
    lines = []
    for i, hit in enumerate(hits, start=1):
        header = f"[{i}] source: {hit.source}, page: {hit.page}"
        lines.append(header)
        lines.append(hit.text)
        lines.append("")  # blank line between chunks
    return "\n".join(lines)


def build_messages(question: str, hits) -> list[dict]:
    """Build the chat messages for the LLM."""
    context = build_context(hits)
    user_content = f"""Context:{context} Question: {question}
                    Answer using only the context above. Include citations like [file.pdf, p.N]."""

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_content},
    ]