from __future__ import annotations

from typing import Any, Dict, Optional
from app.rag.embedders.base import Embedder
from app.rag.vectorstores.base import VectorStore
from app.rag.types import RetrieveResult, ScoredChunk


class RetrievalService:
    def __init__(self, embedder: Embedder, store: VectorStore):
        self._embedder = embedder
        self._store = store

    def retrieve(
        self,
        *,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ) -> RetrieveResult:
        qv = self._embedder.embed_query(query)
        matches: list[ScoredChunk] = self._store.similarity_search(
            query_vector=qv,
            top_k=top_k,
            filters=filters,
            score_threshold=score_threshold,
        )
        return RetrieveResult(query=query, matches=matches, used_top_k=top_k, score_threshold=score_threshold)