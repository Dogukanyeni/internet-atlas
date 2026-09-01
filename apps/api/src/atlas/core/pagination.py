"""Pagination, sorting and filtering contracts.

Two pagination styles, used on purpose in different places:

* **Offset pages** (`?page=2&page_size=50`) for admin tables, where a human wants page
  numbers and a total count.
* **Cursor pages** (`?cursor=...&limit=50`) for anything public that can grow: search
  results, topic listings, graph neighbours, activity. Offset paging gets slower as the
  offset grows, and it skips or repeats rows when data changes while a user reads. A
  cursor has neither problem.

Rule for new endpoints: if the collection can grow without limit, use a cursor.

The cursor is an opaque base64 string. Clients must never build or parse one. Because
ids are time-ordered UUIDv7, the cursor is simply the last id seen.
"""

import base64
import binascii
from typing import Annotated, Self
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel, Field, computed_field

from atlas.core.errors import ErrorCode, ValidationError

__all__ = [
    "CursorPage",
    "CursorParams",
    "Page",
    "PageParams",
    "SortOrder",
    "decode_cursor",
    "encode_cursor",
]

MAX_PAGE_SIZE = 100
DEFAULT_PAGE_SIZE = 25


class PageParams(BaseModel):
    """Offset pagination input. Use for admin lists only."""

    page: Annotated[int, Query(ge=1)] = 1
    page_size: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size


class Page[T](BaseModel):
    """Offset page response."""

    items: list[T]
    total: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)

    @computed_field  # type: ignore[prop-decorator]
    @property
    def pages(self) -> int:
        if self.page_size == 0:
            return 0
        return -(-self.total // self.page_size)  # ceiling division

    @classmethod
    def build(cls, items: list[T], total: int, params: PageParams) -> Self:
        return cls(items=items, total=total, page=params.page, page_size=params.page_size)


class CursorParams(BaseModel):
    """Cursor pagination input. The default for public endpoints."""

    cursor: Annotated[str | None, Query()] = None
    limit: Annotated[int, Query(ge=1, le=MAX_PAGE_SIZE)] = DEFAULT_PAGE_SIZE

    @property
    def after_id(self) -> UUID | None:
        return decode_cursor(self.cursor) if self.cursor else None


class CursorPage[T](BaseModel):
    """Cursor page response.

    There is no `total`. Counting a large filtered set on every request is expensive,
    and users of an endless list do not need it. Endpoints that truly need a count get a
    separate facet endpoint (Phase 18).
    """

    items: list[T]
    next_cursor: str | None = None
    has_more: bool = False


def encode_cursor(last_id: UUID) -> str:
    """Make an opaque cursor from the last id in a page."""
    return base64.urlsafe_b64encode(last_id.bytes).decode("ascii").rstrip("=")


def decode_cursor(cursor: str) -> UUID:
    """Read a cursor. A broken cursor is a client error, not a server error."""
    try:
        padded = cursor + "=" * (-len(cursor) % 4)
        return UUID(bytes=base64.urlsafe_b64decode(padded))
    except (ValueError, binascii.Error) as exc:
        raise ValidationError(
            "The cursor is not valid. Start from the first page.",
            code=ErrorCode.INVALID_CURSOR,
        ) from exc


class SortOrder(BaseModel):
    """One parsed sort instruction.

    Wire format: `?sort=-created_at` where a leading minus means descending.
    Every endpoint declares which fields it allows; anything else is rejected instead of
    silently ignored, because a silently ignored sort looks like a broken feature.
    """

    field: str
    descending: bool = False

    @classmethod
    def parse(cls, raw: str | None, allowed: frozenset[str], default: str) -> Self:
        value = raw or default
        descending = value.startswith("-")
        field = value[1:] if descending else value

        if field not in allowed:
            raise ValidationError(
                f"Cannot sort by '{field}'.",
                code=ErrorCode.INVALID_SORT,
                allowed=sorted(allowed),
            )
        return cls(field=field, descending=descending)
