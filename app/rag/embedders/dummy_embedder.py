# app/rag/embedders/dummy_embedder.py
from __future__ import annotations

from typing import List
from app.rag.types import Chunk, Vector
from app.rag.embedders.base import Embedder


class DummyEmbedder(Embedder):
    def __init__(self, dim: int = 8):
        self._dim = dim

    def embed_chunks(self, chunks: List[Chunk]) -> List[Vector]:
        out: List[Vector] = []
        for c in chunks:
            s = c.text
            total = sum(ord(ch) for ch in s)
            v = []
            for i in range(self._dim):
                v.append(((total + i * 31) % 1000) / 1000.0)
            out.append(v)
        return out