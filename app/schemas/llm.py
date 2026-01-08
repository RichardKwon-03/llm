from __future__ import annotations

from enum import Enum
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class Role(str, Enum):
    system = "system"
    user = "user"
    assistant = "assistant"


class ChatMessage(BaseModel):
    role: Role
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)

    tag: Optional[str] = Field(default=None, description="prompt definition tag in DB")
    version: Optional[int] = Field(default=None, description="prompt definition version (default=1 if omitted)")

    system: Optional[str] = Field(default=None, description="override system prompt (optional)")
    vars: Optional[Dict[str, Any]] = Field(default=None, description="template variables")


class ChatResponse(BaseModel):
    reply: str
    provider: str
    tag: Optional[str] = None
    version: Optional[int] = None