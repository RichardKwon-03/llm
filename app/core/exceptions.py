from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int = 500
    details: Optional[dict[str, Any]] = None


class BadRequest(AppError):
    def __init__(self, message: str = "Bad request", details: Optional[dict[str, Any]] = None):
        super().__init__(code="BAD_REQUEST", message=message, status_code=400, details=details)


class UpstreamError(AppError):
    def __init__(self, message: str = "Upstream provider error", details: Optional[dict[str, Any]] = None):
        super().__init__(code="UPSTREAM_ERROR", message=message, status_code=502, details=details)


class RateLimited(AppError):
    def __init__(self, message: str = "Rate limited", details: Optional[dict[str, Any]] = None):
        super().__init__(code="RATE_LIMITED", message=message, status_code=429, details=details)


class Unauthorized(AppError):
    def __init__(self, message: str = "Unauthorized", details: Optional[dict[str, Any]] = None):
        super().__init__(code="UNAUTHORIZED", message=message, status_code=401, details=details)