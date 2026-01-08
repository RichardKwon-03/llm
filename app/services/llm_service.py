from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional, Tuple

from app.providers.llm_provider import LLMProvider, Message
from app.services.prompt_service import PromptService


class _SafeDict(dict):
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


class LLMService:
    def __init__(self, provider: LLMProvider, prompt_service: PromptService):
        self._provider = provider
        self._prompts = prompt_service

    def provider_name(self) -> str:
        return self._provider.name()

    def _apply_vars(
        self,
        text: str,
        prompt: str,
        vars: Optional[Dict[str, Any]],
    ) -> str:
        if not vars:
            return text
        ctx: Dict[str, Any] = {"prompt": prompt}
        ctx.update(vars)
        return text.format_map(_SafeDict(ctx))

    def _build_messages(
        self,
        *,
        prompt: str,
        tag: Optional[str],
        version: Optional[int],
        system_override: Optional[str],
        vars: Optional[Dict[str, Any]],
    ) -> Tuple[List[Message], Optional[str], Optional[int]]:

        if tag is not None:
            used_tag = tag
            used_version = version or 1

            definition, few_shots = self._prompts.resolve(
                tag=used_tag,
                version=used_version,
            )

            messages: List[Message] = []

            system_text = (
                system_override
                if system_override is not None and system_override != ""
                else "\n\n".join(
                    p
                    for p in [
                        definition.persona,
                        definition.system_guardrails,
                        definition.output_guideline,
                    ]
                    if p
                )
            )
            if system_text:
                messages.append({"role": "system", "content": system_text})

            for s in few_shots:
                messages.append({"role": "user", "content": s.input_text})
                messages.append({"role": "assistant", "content": s.output_text})

            user_text = self._apply_vars(prompt, prompt, vars)
            messages.append({"role": "user", "content": user_text})

            return messages, used_tag, used_version

        messages: List[Message] = []
        if system_override:
            messages.append({"role": "system", "content": system_override})
        messages.append({"role": "user", "content": prompt})
        return messages, None, None

    def chat(
        self,
        prompt: str,
        tag: Optional[str] = None,
        version: Optional[int] = None,
        system: Optional[str] = None,
        vars: Optional[Dict[str, Any]] = None,
    ) -> Tuple[str, Optional[str], Optional[int]]:

        messages, used_tag, used_version = self._build_messages(
            prompt=prompt,
            tag=tag,
            version=version,
            system_override=system,
            vars=vars,
        )

        print("FINAL_MESSAGES =>", messages)

        reply = self._provider.chat_messages(messages)
        return reply, used_tag, used_version

    def stream_tokens(
        self,
        prompt: str,
        tag: Optional[str] = None,
        version: Optional[int] = None,
        system: Optional[str] = None,
        vars: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Iterator[str], Optional[str], Optional[int]]:

        messages, used_tag, used_version = self._build_messages(
            prompt=prompt,
            tag=tag,
            version=version,
            system_override=system,
            vars=vars,
        )

        tokens = self._provider.stream_messages(messages)
        return tokens, used_tag, used_version