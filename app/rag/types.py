from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


Metadata = Dict[str, Any]


@dataclass(frozen=True)
class Document:
    id: str
    text: str
    metadata: Metadata


@dataclass(frozen=True)
class Chunk:
    id: str
    document_id: str
    text: str
    metadata: Metadata


@dataclass(frozen=True)
class ScoredChunk:
    chunk: Chunk
    score: float


@dataclass(frozen=True)
class IngestResult:
    document_id: str
    chunk_count: int


@dataclass(frozen=True)
class RetrieveResult:
    query: str
    matches: List[ScoredChunk]
    used_top_k: int
    score_threshold: Optional[float]