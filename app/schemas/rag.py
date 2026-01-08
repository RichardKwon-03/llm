from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class RagIngestRequest(BaseModel):
    source: str = Field(min_length=1)


class RagIngestResponse(BaseModel):
    document_id: str
    chunk_count: int


class RagSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = 5
    score_threshold: Optional[float] = None
    filters: Optional[Dict[str, Any]] = None


class RagMatch(BaseModel):
    chunk_id: str
    document_id: str
    score: float
    text: str
    metadata: Dict[str, Any]


class RagSearchResponse(BaseModel):
    query: str
    matches: List[RagMatch]