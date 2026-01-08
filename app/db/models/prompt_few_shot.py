from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class PromptFewShot(Base):
    __tablename__ = "prompt_few_shots"

    id = Column(Integer, primary_key=True)
    definition_id = Column(Integer, ForeignKey("prompt_definitions.id", ondelete="CASCADE"), nullable=False)

    shot_type = Column(String(10), nullable=False, default="good")  # good | bad
    label = Column(String(20), nullable=True)

    input_text = Column(Text, nullable=False)
    output_text = Column(Text, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    definition = relationship("PromptDefinition", back_populates="few_shots")