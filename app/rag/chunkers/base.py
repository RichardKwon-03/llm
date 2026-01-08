from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List
from app.rag.types import Document, Chunk


class Chunker(ABC):
    @abstractmethod
    def chunk(self, doc: Document) -> List[Chunk]:
        raise NotImplementedError