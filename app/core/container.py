from typing import Iterator

from sqlalchemy.orm import Session

from app.cache.prompt_cache import PromptCache
from app.core.config import settings
from app.db.session import SessionLocal
from app.providers.groq_provider import GroqProvider
from app.services.llm_service import LLMService
from app.services.prompt_service import PromptService

_cache = PromptCache()

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