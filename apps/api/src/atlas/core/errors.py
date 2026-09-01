"""The error contract.

Every error the API returns has the same shape:

```json
{
  "error": {
    "code": "not_found",
    "message": "This item does not exist.",
    "details": { "...": "optional, machine readable" },
    "request_id": "9f2c..."
  }
}
```

Three decisions behind this:

* **`code` is for machines, `message` is for people.** The frontend switches on `code`
  and never parses `message`. That means we can improve wording, or translate it later,
  without breaking any client.
* **`request_id` is always included.** A user can send a screenshot, and that id finds
  the exact request in the logs. Support work is impossible without it.
* **Internal details never leak.** An unexpected exception returns a generic message;
  the real reason goes to the logs only.
"""

from enum import StrEnum
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from atlas.core.logging import get_logger, request_id_var

__all__ = [
    "AtlasError",
    "ConflictError",
    "ErrorCode",
    "NotFoundError",
    "PermissionDeniedError",
    "RateLimitedError",
    "UnauthenticatedError",
    "ValidationError",
    "register_error_handlers",
]

logger = get_logger(__name__)


class ErrorCode(StrEnum):
    """The full dictionary. Clients may rely on these strings.

    A code is never renamed once released. New codes may be added at any time, so
    clients must handle an unknown code by falling back to the message.
    """

    # --- generic ---
    VALIDATION_ERROR = "validation_error"
    NOT_FOUND = "not_found"
    CONFLICT = "conflict"
    UNAUTHENTICATED = "unauthenticated"
    PERMISSION_DENIED = "permission_denied"
    RATE_LIMITED = "rate_limited"
    INTERNAL_ERROR = "internal_error"
    SERVICE_UNAVAILABLE = "service_unavailable"

    # --- request shape ---
    INVALID_CURSOR = "invalid_cursor"
    INVALID_SORT = "invalid_sort"
    INVALID_FILTER = "invalid_filter"

    # --- catalog and taxonomy ---
    SLUG_TAKEN = "slug_taken"
    DUPLICATE_DOMAIN = "duplicate_domain"
    INVALID_URL = "invalid_url"
    ENTITY_ARCHIVED = "entity_archived"
    PUBLISH_REQUIREMENTS_NOT_MET = "publish_requirements_not_met"

    # --- graph ---
    INVALID_RELATION_PAIR = "invalid_relation_pair"
    DUPLICATE_RELATION = "duplicate_relation"
    SELF_RELATION = "self_relation"
    CYCLE_DETECTED = "cycle_detected"
    DEPTH_LIMIT_EXCEEDED = "depth_limit_exceeded"

    # --- editing ---
    VERSION_CONFLICT = "version_conflict"


class AtlasError(Exception):
    """Base class for errors we raise on purpose."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    default_code: ErrorCode = ErrorCode.VALIDATION_ERROR
    default_message: str = "The request could not be processed."

    def __init__(
        self,
        message: str | None = None,
        *,
        code: ErrorCode | None = None,
        **details: Any,
    ) -> None:
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.details = details
        super().__init__(self.message)


class ValidationError(AtlasError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    default_code = ErrorCode.VALIDATION_ERROR
    default_message = "Some values are not valid."


class NotFoundError(AtlasError):
    status_code = status.HTTP_404_NOT_FOUND
    default_code = ErrorCode.NOT_FOUND
    default_message = "This item does not exist."


class UnauthenticatedError(AtlasError):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_code = ErrorCode.UNAUTHENTICATED
    default_message = "You need to sign in to do this."


class PermissionDeniedError(AtlasError):
    status_code = status.HTTP_403_FORBIDDEN
    default_code = ErrorCode.PERMISSION_DENIED
    default_message = "You are not allowed to do this."


class ConflictError(AtlasError):
    status_code = status.HTTP_409_CONFLICT
    default_code = ErrorCode.CONFLICT
    default_message = "This item already exists."


class RateLimitedError(AtlasError):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = ErrorCode.RATE_LIMITED
    default_message = "Too many requests. Please slow down."


def error_body(
    code: ErrorCode, message: str, details: dict[str, Any] | None = None
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "error": {
            "code": code.value,
            "message": message,
            "request_id": request_id_var.get(),
        }
    }
    if details:
        payload["error"]["details"] = details
    return payload


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AtlasError)
    async def _atlas_error(_: Request, exc: AtlasError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_body(exc.code, exc.message, exc.details or None),
        )

    @app.exception_handler(RequestValidationError)
    async def _request_validation(_: Request, exc: RequestValidationError) -> JSONResponse:
        # FastAPI's own validation errors are reshaped into our contract, so a client
        # never has to handle two different error formats.
        fields = [
            {
                "field": ".".join(str(part) for part in error["loc"][1:]),
                "reason": error["msg"],
            }
            for error in exc.errors()
        ]
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content=error_body(
                ErrorCode.VALIDATION_ERROR,
                "Some fields are not valid.",
                {"fields": fields},
            ),
        )

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        # Never show the real reason to the client. Log it with the request id instead.
        logger.exception("unhandled_error", path=request.url.path, error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_body(ErrorCode.INTERNAL_ERROR, "Something went wrong on our side."),
        )
