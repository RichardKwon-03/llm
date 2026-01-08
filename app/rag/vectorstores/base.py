from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.rag.types import Chunk, ScoredChunk


class VectorStore(ABC):
    @abstractmethod
    def upsert_chunks(
        self,
        *,
        chunks: List[Chunk],
        vectors: List[List[float]],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def similarity_search(
        self,
        *,
        query_vector: List[float],
        top_k: int,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ) -> List[ScoredChunk]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_document_id(self, *, document_id: str) -> int:
        raise NotImplementedError