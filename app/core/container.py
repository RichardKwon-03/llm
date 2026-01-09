from typing import Iterator

from sqlalchemy.orm import Session

from app.cache.prompt_cache import PromptCache
from app.core.config import settings
from app.db.session import SessionLocal
from app.providers.groq_provider import GroqProvider
from app.rag.chunkers.simple_chunker import SimpleChunker
from app.rag.embedders.dummy_embedder import DummyEmbedder
from app.services.ingestion_service import IngestionService
from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService
from app.rag.vectorstores.memory_vectorstore import MemoryVectorStore

_cache = PromptCache()

_memory_vs = MemoryVectorStore()

def get_llm_service() -> Iterator[LLMService]:
    db = SessionLocal()
    try:
        prompt_service = PromptService(db=db, cache=_cache)
        provider = GroqProvider(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL)
        yield LLMService(provider=provider, prompt_service=prompt_service)
    finally:
        db.close()

def get_prompt_service() -> Iterator[PromptService]:
    db: Session = SessionLocal()
    try:
        yield PromptService(db=db, cache=_cache)
    finally:
        db.close()

def get_ingestion_service() -> IngestionService:
    return IngestionService(
        chunker=SimpleChunker(),
        embedder=DummyEmbedder(dim=8),
        vectorstore=_memory_vs,
    )