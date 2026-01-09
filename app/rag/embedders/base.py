from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from app.rag.types import Chunk, Vector


class Embedder(ABC):
    @abstractmethod
    def embed_chunks(self, chunks: List[Chunk]) -> List[Vector]:
        raise NotImplementedError