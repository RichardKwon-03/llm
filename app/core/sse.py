from __future__ import annotations
import json
from typing import Iterator, Optional
from app.core.exceptions import AppError

def sse_event(data: str, event: Optional[str] = None) -> str:
    lines = []
    if event:
        lines.append(f"event: {event}")
    lines.append(f"data: {data}")
    return "\n".join(lines) + "\n\n"

def sse_stream(
    tokens: Iterator[str],
    *,
    flush_chars: int = 64,
    flush_on_newline: bool = True,
) -> Iterator[str]:
    buf: list[str] = []
    buf_len = 0

    def flush() -> Optional[str]:
        nonlocal buf_len
        if not buf:
            return None
        chunk = "".join(buf)
        buf.clear()
        buf_len = 0
        return sse_event(chunk, event="token")

    try:
        for t in tokens:
            if not t:
                continue

            buf.append(t)
            buf_len += len(t)

            if buf_len >= flush_chars or (flush_on_newline and "\n" in t):
                out = flush()
                if out:
                    yield out

        out = flush()
        if out:
            yield out

        yield sse_event("done", event="done")

    except AppError as e:
        payload = json.dumps(
            {"code": e.code, "message": e.message, "details": e.details or {}},
            ensure_ascii=False,
        )
        yield sse_event(payload, event="error")

    except Exception as e:
        payload = json.dumps(
            {
                "code": "INTERNAL_ERROR",
                "message": "Internal server error",
                "details": {"type": e.__class__.__name__},
            },
            ensure_ascii=False,
        )
        yield sse_event(payload, event="error")