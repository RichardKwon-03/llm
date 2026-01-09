from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from app.rag.types import Chunk, Vector


class VectorStore(ABC):
    @abstractmethod
    def upsert(self, *, source_id: str, chunks: List[Chunk], vectors: List[Vector]) -> None:
        raise NotImplementedError