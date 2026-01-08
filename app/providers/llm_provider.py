from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Iterator, List, Literal, TypedDict

Role = Literal["system", "user", "assistant"]

class Message(TypedDict):
    role: Role
    content: str

class LLMProvider(ABC):
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def chat(self, prompt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream(self, prompt: str) -> Iterator[str]:
        raise NotImplementedError

    @abstractmethod
    def chat_messages(self, messages: List[Message]) -> str:
        raise NotImplementedError

    @abstractmethod
    def stream_messages(self, messages: List[Message]) -> Iterator[str]:
        raise NotImplementedError