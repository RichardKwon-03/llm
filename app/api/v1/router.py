from fastapi import APIRouter
from app.api.v1.endpoints import health, llm, prompts

router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(llm.router, tags=["llm"])
router.include_router(prompts.router, tags=["prompts"])