from __future__ import annotations

from typing import Iterator, Optional, List

from groq import Groq
from groq._exceptions import APIError, BadRequestError, RateLimitError, AuthenticationError

from app.core.config import settings
from app.core.exceptions import BadRequest, RateLimited, Unauthorized, UpstreamError
from app.providers.llm_provider import LLMProvider, Message


class GroqProvider(LLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self._client = Groq(api_key=api_key or settings.GROQ_API_KEY)
        self._model = model or settings.GROQ_MODEL

    def name(self) -> str:
        return "groq"

    def chat(self, prompt: str) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.choices[0].message.content or ""
        except BadRequestError as e:
            raise BadRequest(message="Bad request", details={"upstream": "groq", "error": str(e)})
        except AuthenticationError as e:
            raise Unauthorized(message="Unauthorized", details={"upstream": "groq", "error": str(e)})
        except RateLimitError as e:
            raise RateLimited(message="Rate limited", details={"upstream": "groq", "error": str(e)})
        except APIError as e:
            raise UpstreamError(message="Upstream provider error", details={"upstream": "groq", "error": str(e)})

    def stream(self, prompt: str) -> Iterator[str]:
        try:
            stream = self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except BadRequestError as e:
            raise BadRequest(message="Bad request", details={"upstream": "groq", "error": str(e)})
        except AuthenticationError as e:
            raise Unauthorized(message="Unauthorized", details={"upstream": "groq", "error": str(e)})
        except RateLimitError as e:
            raise RateLimited(message="Rate limited", details={"upstream": "groq", "error": str(e)})
        except APIError as e:
            raise UpstreamError(message="Upstream provider error", details={"upstream": "groq", "error": str(e)})

    def chat_messages(self, messages: List[Message]) -> str:
        try:
            resp = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            raise UpstreamError(details={"upstream": "groq", "type": e.__class__.__name__})

    def stream_messages(self, messages: List[Message]) -> Iterator[str]:
        try:
            stream = self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except Exception as e:
            raise UpstreamError(details={"upstream": "groq", "type": e.__class__.__name__})