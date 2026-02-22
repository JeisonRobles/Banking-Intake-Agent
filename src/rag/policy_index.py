# src/rag/policy_index.py

from __future__ import annotations

from pathlib import Path
from src.llm.openai_client import OpenAIClient
from src.rag.chunking import chunk_text
from src.rag.in_memory_store import InMemoryVectorStore, DocChunk


def build_policy_store(policy_path: str, client: OpenAIClient) -> InMemoryVectorStore:
    text = Path(policy_path).read_text(encoding="utf-8")
    chunks_text = chunk_text(text, max_chars=900, overlap=120)

    chunks = [
        DocChunk(text=ct, source=policy_path, chunk_id=i)
        for i, ct in enumerate(chunks_text)
    ]

    vectors = client.embed([c.text for c in chunks])

    store = InMemoryVectorStore()
    store.add(chunks, vectors)
    return store