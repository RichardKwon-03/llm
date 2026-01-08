from __future__ import annotations

from sqlalchemy.orm import Session

from app.cache.prompt_cache import PromptCache
from app.db.repositories.prompt_definitions import (
    get_prompt_definition,
    upsert_prompt_definition,
)
from app.db.repositories.prompt_few_shot import (
    list_few_shots,
    upsert_prompt_few_shot,
    deactivate_prompt_few_shot,
)


class PromptService:
    def __init__(self, db: Session, cache: PromptCache):
        self._db = db
        self._cache = cache

    def resolve(
        self,
        *,
        tag: str,
        version: int,
    ):
        cached = self._cache.get(tag, version)
        if cached:
            return cached["definition"], cached["few_shots"]

        definition = get_prompt_definition(self._db, tag, version)
        if not definition:
            raise RuntimeError("Prompt definition not found")

        few_shots = list_few_shots(
            self._db,
            definition_id=definition.id,
            active_only=True,
        )

        payload = {
            "definition": {
                "id": definition.id,
                "tag": definition.tag,
                "version": definition.version,
                "persona": definition.persona,
                "system_guardrails": definition.system_guardrails,
                "output_guideline": definition.output_guideline,
                "output_schema_json": definition.output_schema_json,
                "llm_config": definition.llm_config,
                "is_active": definition.is_active,
            },
            "few_shots": [
                {
                    "id": s.id,
                    "definition_id": s.definition_id,
                    "input_text": s.input_text,
                    "output_text": s.output_text,
                    "label": s.label,
                    "sort_order": s.sort_order,
                    "is_active": s.is_active,
                }
                for s in few_shots
            ],
        }
        self._cache.set(tag, version, payload)

        return definition, few_shots

    def upsert_definition(
        self,
        *,
        tag: str,
        version: int,
        persona: str,
        system_guardrails: str | None,
        output_guideline: str | None,
        llm_config: dict,
        output_schema_json: dict | None,
        is_active: bool = True,
    ):
        obj = upsert_prompt_definition(
            self._db,
            tag=tag,
            version=version,
            persona=persona,
            system_guardrails=system_guardrails,
            output_guideline=output_guideline,
            llm_config=llm_config,
            output_schema_json=output_schema_json,
            is_active=is_active,
        )

        self._cache.delete(tag, version)

        return obj

    def list_few_shots(
        self,
        *,
        definition_id: str,
        active_only: bool = True,
    ):
        return list_few_shots(
            self._db,
            definition_id=definition_id,
            active_only=active_only,
        )

    def upsert_few_shot(
        self,
        *,
        id: int | None,
        definition_id: int,
        input_text: str,
        output_text: str,
        label: str | None,
        sort_order: int | None,
        is_active: bool,
        tag: str,
        version: int,
    ):
        obj = upsert_prompt_few_shot(
            self._db,
            id=id,
            definition_id=definition_id,
            input_text=input_text,
            output_text=output_text,
            label=label,
            sort_order=sort_order,
            is_active=is_active,
        )

        self._cache.delete(tag, version)

        return obj

    def deactivate_few_shot(
        self,
        *,
        id: int,
        tag: str,
        version: int,
    ):
        obj = deactivate_prompt_few_shot(self._db, id=id)

        self._cache.delete(tag, version)

        return obj