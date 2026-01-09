from __future__ import annotations

from typing import Dict, List, Tuple
from app.rag.types import Chunk, Vector
from app.rag.vectorstores.base import VectorStore


class MemoryVectorStore(VectorStore):
    def __init__(self):
        self._data: Dict[str, List[Tuple[Chunk, Vector]]] = {}

    def upsert(self, *, source_id: str, chunks: List[Chunk], vectors: List[Vector]) -> None:
        if len(chunks) != len(vectors):
            raise ValueError("chunks and vectors length mismatch")
        self._data[source_id] = list(zip(chunks, vectors))