from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models.prompt_few_shot import PromptFewShot


def list_few_shots(
    db: Session,
    *,
    definition_id: int,
    active_only: bool = True,
) -> list[type[PromptFewShot]]:
    q = db.query(PromptFewShot).filter(PromptFewShot.definition_id == definition_id)
    if active_only:
        q = q.filter(PromptFewShot.is_active.is_(True))

    return (
        q.order_by(PromptFewShot.sort_order.asc(), PromptFewShot.id.asc())
        .all()
    )


def get_next_sort_order(db: Session, *, definition_id: int) -> int:
    max_order = (
        db.query(func.max(PromptFewShot.sort_order))
        .filter(PromptFewShot.definition_id == definition_id)
        .scalar()
    )
    return int(max_order or 0) + 1


def upsert_prompt_few_shot(
    db: Session,
    *,
    id: int | None = None,
    definition_id: int,
    input_text: str,
    output_text: str,
    label: str | None = None,
    sort_order: int | None = None,
    is_active: bool = True,
) -> PromptFewShot:
    obj: PromptFewShot | None = None

    if id is not None:
        obj = db.query(PromptFewShot).filter(PromptFewShot.id == id).one_or_none()

    if obj is None:
        if sort_order is None:
            sort_order = get_next_sort_order(db, definition_id=definition_id)

        obj = PromptFewShot(
            definition_id=definition_id,
            input_text=input_text,
            output_text=output_text,
            label=label,
            sort_order=sort_order,
            is_active=is_active,
        )
        db.add(obj)
    else:
        obj.definition_id = definition_id
        obj.input_text = input_text
        obj.output_text = output_text
        obj.label = label
        if sort_order is not None:
            obj.sort_order = sort_order
        obj.is_active = is_active

    db.commit()
    db.refresh(obj)
    return obj


def deactivate_prompt_few_shot(db: Session, *, id: int) -> type[PromptFewShot]:
    obj = db.query(PromptFewShot).filter(PromptFewShot.id == id).one_or_none()
    if obj is None:
        raise RuntimeError("PromptFewShot not found")

    obj.is_active = False
    db.commit()
    db.refresh(obj)
    return obj