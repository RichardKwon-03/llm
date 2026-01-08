from __future__ import annotations

from app.rag.loaders.base import DocumentLoader
from app.rag.chunkers.base import Chunker
from app.rag.embedders.base import Embedder
from app.rag.vectorstores.base import VectorStore
from app.rag.types import IngestResult


class IngestionService:
    def __init__(self, loader: DocumentLoader, chunker: Chunker, embedder: Embedder, store: VectorStore):
        self._loader = loader
        self._chunker = chunker
        self._embedder = embedder
        self._store = store

    def ingest(self, *, source: str) -> IngestResult:
        doc = self._loader.load(source=source)
        chunks = self._chunker.chunk(doc)
        vectors = self._embedder.embed_texts([c.text for c in chunks])
        self._store.upsert_chunks(chunks=chunks, vectors=vectors)
        return IngestResult(document_id=doc.id, chunk_count=len(chunks))