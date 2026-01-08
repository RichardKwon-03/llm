from __future__ import annotations

from typing import Any, Dict, Optional

from app.rag.services.retrieval_service import RetrievalService


class RagService:
    """
    주제 무관 골격:
    - retrieve 까지만 책임 (LLM 합성/프롬프트는 상위 LLMService에서)
    """

    def __init__(self, retrieval: RetrievalService):
        self._retrieval = retrieval

    def search(
        self,
        *,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ):
        return self._retrieval.retrieve(
            query=query,
            top_k=top_k,
            filters=filters,
            score_threshold=score_threshold,
        )