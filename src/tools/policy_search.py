# src/tools/policy_search.py

from __future__ import annotations

from src.llm.openai_client import OpenAIClient
from src.rag.policy_index import build_policy_store

# Build once (in-memory). For MVP this is fine.
# Later with Qdrant you persist and reuse across runs.
_POLICY_PATH = "data/policies/banking_intake_policy.md"

_client = OpenAIClient()
_store = build_policy_store(_POLICY_PATH, _client)


def policy_search(query: str, top_k: int = 5) -> str:
    """
    Returns top-k relevant policy chunks as a single string.
    Your agent can inject this into the prompt as grounded context.
    """
    q_vec = _client.embed([query])[0]
    results = _store.search(q_vec, top_k=top_k)

    if not results:
        return "No relevant policy context found."

    blocks = []
    for chunk, score in results:
        blocks.append(f"[source={chunk.source} chunk={chunk.chunk_id} score={score:.3f}]\n{chunk.text}")

    return "\n\n---\n\n".join(blocks)