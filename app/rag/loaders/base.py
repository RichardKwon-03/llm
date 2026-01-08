from __future__ import annotations

from abc import ABC, abstractmethod
from app.rag.types import Document


class DocumentLoader(ABC):
    @abstractmethod
    def load(self, *, source: str) -> Document:
        """
        source 예:
        - 파일 경로
        - URL
        - DB key
        - raw text id 등
        """
        raise NotImplementedError