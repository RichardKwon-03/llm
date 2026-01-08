import json
from typing import Any, Optional

import redis

from app.core.config import settings

_redis: redis.Redis | None = None


def _get_redis() -> redis.Redis:
    global _redis
    if _redis is None:
        _redis = redis.Redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
        )
    return _redis


class PromptCache:
    """
    프롬프트 템플릿 캐시
    key = prompt:{template_name}:{version}
    """

    def _key(self, name: str, version: int) -> str:
        return f"prompt:{name}:{version}"

    def get(self, name: str, version: int) -> Optional[dict[str, Any]]:
        r = _get_redis()
        raw = r.get(self._key(name, version))
        if not raw:
            return None
        try:
            return json.loads(raw)
        except Exception:
            return None

    def set(self, name: str, version: int, payload: dict[str, Any]) -> None:
        r = _get_redis()
        r.setex(
            self._key(name, version),
            settings.PROMPT_CACHE_TTL_SECONDS,
            json.dumps(payload, ensure_ascii=False),
        )

    def delete(self, name: str, version: int) -> None:
        r = _get_redis()
        r.delete(self._key(name, version))