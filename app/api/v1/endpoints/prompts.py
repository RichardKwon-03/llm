from fastapi import APIRouter, Depends

from app.core.container import get_prompt_service
from app.services.prompt_service import PromptService
from app.schemas.prompt import (
    PromptDefinitionUpsertRequest,
    PromptDefinitionResponse,
    FewShotUpsertRequest,
    FewShotResponse,
)

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.post("", response_model=PromptDefinitionResponse)
def upsert_prompt_definition(
    req: PromptDefinitionUpsertRequest,
    service: PromptService = Depends(get_prompt_service),
):
    defn = service.upsert_definition(
        tag=req.tag,
        version=req.version,
        persona=req.persona,
        system_guardrails=req.system_guardrails,
        output_guideline=req.output_guideline,
        llm_config=req.llm_config,
        output_schema_json=req.output_schema_json,
        is_active=req.is_active,
    )

    return PromptDefinitionResponse(
        tag=defn.tag,
        version=defn.version,
        is_active=defn.is_active,
    )


@router.get("/{tag}/{version}", response_model=PromptDefinitionResponse)
def get_prompt_definition(
    tag: str,
    version: int,
    service: PromptService = Depends(get_prompt_service),
):
    defn, _ = service.resolve(tag=tag, version=version)

    return PromptDefinitionResponse(
        tag=defn.tag,
        version=defn.version,
        is_active=defn.is_active,
    )

@router.get(
    "/{tag}/{version}/few-shots",
    response_model=list[FewShotResponse],
)
def list_few_shots(
    tag: str,
    version: int,
    service: PromptService = Depends(get_prompt_service),
):
    defn, shots = service.resolve(tag=tag, version=version)

    return [
        FewShotResponse(
            id=s.id,
            input_text=s.input_text,
            output_text=s.output_text,
            label=s.label,
            sort_order=s.sort_order,
            is_active=s.is_active,
        )
        for s in shots
    ]


@router.post(
    "/{tag}/{version}/few-shots",
    response_model=FewShotResponse,
)
def upsert_few_shot(
    tag: str,
    version: int,
    req: FewShotUpsertRequest,
    service: PromptService = Depends(get_prompt_service),
):
    obj = service.upsert_few_shot(
        id=req.id,
        definition_id=req.definition_id,
        input_text=req.input_text,
        output_text=req.output_text,
        label=req.label,
        sort_order=req.sort_order,
        is_active=req.is_active,
        tag=tag,
        version=version,
    )

    return FewShotResponse(
        id=obj.id,
        input_text=obj.input_text,
        output_text=obj.output_text,
        label=obj.label,
        sort_order=obj.sort_order,
        is_active=obj.is_active,
    )


@router.delete(
    "/{tag}/{version}/few-shots/{few_shot_id}",
    response_model=FewShotResponse,
)
def deactivate_few_shot(
    tag: str,
    version: int,
    few_shot_id: int,
    service: PromptService = Depends(get_prompt_service),
):
    obj = service.deactivate_few_shot(
        id=few_shot_id,
        tag=tag,
        version=version,
    )

    return FewShotResponse(
        id=obj.id,
        input_text=obj.input_text,
        output_text=obj.output_text,
        label=obj.label,
        sort_order=obj.sort_order,
        is_active=obj.is_active,
    )