from sqlalchemy import Column, Integer, String, Boolean, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.base import Base


class PromptDefinition(Base):
    __tablename__ = "prompt_definitions"

    id = Column(Integer, primary_key=True)
    tag = Column(String(50), nullable=False)
    version = Column(Integer, nullable=False)

    description = Column(Text, nullable=True)

    persona = Column(Text, nullable=False)
    system_guardrails = Column(Text, nullable=True)
    output_guideline = Column(Text, nullable=True)

    output_schema_json = Column(JSONB, nullable=True)
    llm_config = Column(JSONB, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    few_shots = relationship(
        "PromptFewShot",
        back_populates="definition",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="PromptFewShot.sort_order",
    )

    __table_args__ = (
        UniqueConstraint("tag", "version", name="uq_prompt_tag_version"),
    )