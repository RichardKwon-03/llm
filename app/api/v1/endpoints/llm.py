from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.core.sse import sse_stream
from app.schemas.llm import ChatRequest, ChatResponse
from app.core.container import get_llm_service
from app.services.llm_service import LLMService

router = APIRouter(prefix="/llm")


@router.post("/chat", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    svc: LLMService = Depends(get_llm_service),
) -> ChatResponse:
    reply, used_tag, used_version = svc.chat(
        prompt=req.prompt,
        tag=req.tag,
        version=req.version,
        system=req.system,
        vars=req.vars,
    )

    return ChatResponse(
        reply=reply,
        provider=svc.provider_name(),
        tag=used_tag,
        version=used_version,
    )


@router.post("/chat/stream")
def chat_stream(
    req: ChatRequest,
    svc: LLMService = Depends(get_llm_service),
):
    tokens, used_tag, used_version = svc.stream_tokens(
        prompt=req.prompt,
        tag=req.tag,
        version=req.version,
        system=req.system,
        vars=req.vars,
    )

    return StreamingResponse(
        sse_stream(tokens),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )