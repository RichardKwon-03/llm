from __future__ import annotations

from typing import Any, Dict, Optional

from app.rag.types import Document
from app.rag.chunkers.base import Chunker
from app.rag.embedders.base import Embedder
from app.rag.vectorstores.base import VectorStore


class IngestionService:
    def __init__(self, chunker: Chunker, embedder: Embedder, vectorstore: VectorStore):
        self._chunker = chunker
        self._embedder = embedder
        self._vs = vectorstore

    def ingest_text(self, *, source_id: str, text: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        doc = Document(id=source_id, text=text, metadata=metadata or {})
        chunks = self._chunker.chunk(doc)
        vectors = self._embedder.embed_chunks(chunks)
        self._vs.upsert(source_id=source_id, chunks=chunks, vectors=vectors)
        return len(chunks)