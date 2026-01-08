from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from app.rag.types import RetrieveResult


class Retriever(ABC):
    @abstractmethod
    def retrieve(
        self,
        *,
        query: str,
        top_k: int,
        filters: Optional[Dict[str, Any]] = None,
        score_threshold: Optional[float] = None,
    ) -> RetrieveResult:
        raise NotImplementedError