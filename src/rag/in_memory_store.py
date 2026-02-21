# src/rag/in_memory_store.py

from __future__ import annotations

from dataclasses import dataclass
import numpy as np

@dataclass
class DocChunk:
    text: str
    source: str
    chunk_id: int


class InMemoryVectorStore:
    def __init__(self) -> None:
        self.chunks: list[DocChunk] = []
        self.embeddings: np.ndarray | None = None  # shape: (n, dim)

    def add(self, chunks: list[DocChunk], vectors: list[list[float]]) -> None:
        vecs = np.array(vectors, dtype=np.float32)
        if self.embeddings is None:
            self.embeddings = vecs
        else:
            self.embeddings = np.vstack([self.embeddings, vecs])

        self.chunks.extend(chunks)

    def search(self, query_vec: list[float], top_k: int = 5) -> list[tuple[DocChunk, float]]:
        if self.embeddings is None or len(self.chunks) == 0:
            return []

        q = np.array(query_vec, dtype=np.float32)
        q = q / (np.linalg.norm(q) + 1e-12)

        M = self.embeddings
        M_norm = M / (np.linalg.norm(M, axis=1, keepdims=True) + 1e-12)

        sims = M_norm @ q  # cosine similarity
        idx = np.argsort(-sims)[:top_k]

        return [(self.chunks[i], float(sims[i])) for i in idx]