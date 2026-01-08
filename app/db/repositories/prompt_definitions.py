from __future__ import annotations

from sqlalchemy.orm import Session, selectinload, with_loader_criteria

from app.db.models.prompt_definition import PromptDefinition
from app.db.models.prompt_few_shot import PromptFewShot


def get_prompt_definition(db: Session, tag: str, version: int) -> PromptDefinition | None:
    return (
        db.query(PromptDefinition)
        .options(
            selectinload(PromptDefinition.few_shots),
            with_loader_criteria(
                PromptFewShot,
                PromptFewShot.is_active.is_(True),
                include_aliases=True,
            ),
        )
        .filter(
            PromptDefinition.tag == tag,
            PromptDefinition.version == version,
            PromptDefinition.is_active.is_(True),
        )
        .one_or_none()
    )


def upsert_prompt_definition(
    db: Session,
    *,
    tag: str,
    version: int,
    persona: str,
    system_guardrails: str | None = None,
    output_guideline: str | None = None,
    llm_config: dict,
    output_schema_json: dict | None = None,
    is_active: bool = True,
) -> PromptDefinition:
    obj = (
        db.query(PromptDefinition)
        .filter(PromptDefinition.tag == tag, PromptDefinition.version == version)
        .one_or_none()
    )

    if obj is None:
        obj = PromptDefinition(
            tag=tag,
            version=version,
            persona=persona,
            system_guardrails=system_guardrails,
            output_guideline=output_guideline,
            llm_config=llm_config,
            output_schema_json=output_schema_json,
            is_active=is_active,
        )
        db.add(obj)
    else:
        obj.persona = persona
        obj.system_guardrails = system_guardrails
        obj.output_guideline = output_guideline
        obj.llm_config = llm_config
        obj.output_schema_json = output_schema_json
        obj.is_active = is_active

    db.commit()
    db.refresh(obj)
    return obj