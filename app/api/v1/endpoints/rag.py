from __future__ import annotations

from fastapi import APIRouter, Depends

from app.schemas.rag import RagIngestRequest, RagIngestResponse, RagSearchRequest, RagSearchResponse, RagMatch
from app.rag.services.ingestion_service import IngestionService
from app.rag.services.rag_service import RagService
from app.core.container import get_ingestion_service, get_rag_service


router = APIRouter(prefix="/rag")


@router.post("/ingest", response_model=RagIngestResponse)
def ingest(
    req: RagIngestRequest,
    svc: IngestionService = Depends(get_ingestion_service),
):
    r = svc.ingest(source=req.source)
    return RagIngestResponse(document_id=r.document_id, chunk_count=r.chunk_count)


@router.post("/search", response_model=RagSearchResponse)
def search(
    req: RagSearchRequest,
    svc: RagService = Depends(get_rag_service),
):
    r = svc.search(query=req.query, top_k=req.top_k, filters=req.filters, score_threshold=req.score_threshold)
    return RagSearchResponse(
        query=r.query,
        matches=[
            RagMatch(
                chunk_id=m.chunk.id,
                document_id=m.chunk.document_id,
                score=m.score,
                text=m.chunk.text,
                metadata=m.chunk.metadata,
            )
            for m in r.matches
        ],
    )