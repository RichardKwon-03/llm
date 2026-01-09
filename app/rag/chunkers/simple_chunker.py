from __future__ import annotations

from typing import List
from app.rag.types import Document, Chunk
from app.rag.chunkers.base import Chunker


class SimpleChunker(Chunker):
    def chunk(self, doc: Document) -> List[Chunk]:
        parts = [p.strip() for p in doc.text.split("\n") if p.strip()]
        if not parts:
            parts = [doc.text.strip()]

        chunks: List[Chunk] = []
        for i, t in enumerate(parts):
            chunks.append(
                Chunk(
                    id=f"{doc.id}::chunk::{i}",
                    doc_id=doc.id,
                    text=t,
                    metadata=dict(doc.metadata),
                )
            )
        return chunks