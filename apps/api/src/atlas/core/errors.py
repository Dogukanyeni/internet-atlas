"""One error shape for the whole API.

Phase 6 will grow this into the full error-code dictionary. The important part is set
now: every error the client sees has the same JSON shape, and it never leaks internals.
"""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from atlas.core.logging import get_logger

logger = get_logger(__name__)


class AtlasError(Exception):
    """Base class for errors we raise on purpose."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "bad_request"
    message: str = "The request could not be processed."

    def __init__(self, message: str | None = None, **details: Any) -> None:
        self.message = message or self.message
        self.details = details
        super().__init__(self.message)


class NotFoundError(AtlasError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"
    message = "This item does not exist."


class PermissionDeniedError(AtlasError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "permission_denied"
    message = "You are not allowed to do this."


class ConflictError(AtlasError):
    status_code = status.HTTP_409_CONFLICT
    code = "conflict"
    message = "This item already exists."


def _body(code: str, message: str, details: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details:
        payload["error"]["details"] = details
    return payload


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AtlasError)
    async def _atlas_error(_: Request, exc: AtlasError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=_body(exc.code, exc.message, exc.details or None),
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_body("validation_error", "Some fields are not valid.", {"fields": exc.errors()}),
        )

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        # Never show the real reason to the client. Log it with the request id instead.
        logger.exception("unhandled_error", path=request.url.path, error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_body("internal_error", "Something went wrong on our side."),
        )
