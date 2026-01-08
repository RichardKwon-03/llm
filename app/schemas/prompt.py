from __future__ import annotations

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field

class PromptDefinitionUpsertRequest(BaseModel):
    tag: str = Field(..., description="프롬프트 식별자")
    version: int = Field(..., description="프롬프트 버전")

    persona: str = Field(..., description="모델 역할 정의")
    system_guardrails: Optional[str] = Field(None, description="금지 규칙 / 안전 가이드")
    output_guideline: Optional[str] = Field(None, description="출력 형식/톤 가이드")

    llm_config: Dict[str, Any] = Field(
        ...,
        description="LLM 설정값 (model, temperature, max_tokens 등)",
    )
    output_schema_json: Optional[Dict[str, Any]] = Field(
        None,
        description="Strict JSON output schema",
    )

    is_active: bool = True


class PromptDefinitionResponse(BaseModel):
    tag: str
    version: int
    is_active: bool

class FewShotUpsertRequest(BaseModel):
    id: Optional[int] = Field(
        None,
        description="있으면 update, 없으면 insert",
    )

    definition_id: int = Field(..., description="PromptDefinition.id")
    input_text: str = Field(..., description="User 예시 입력")
    output_text: str = Field(..., description="Assistant 예시 출력")

    label: Optional[str] = Field(
        None,
        description="style_fix / format_fix 등 라벨",
    )
    sort_order: Optional[int] = Field(
        None,
        description="None이면 자동으로 맨 뒤에 추가",
    )
    is_active: bool = True

class FewShotResponse(BaseModel):
    id: int
    input_text: str
    output_text: str
    label: Optional[str]
    sort_order: int
    is_active: bool