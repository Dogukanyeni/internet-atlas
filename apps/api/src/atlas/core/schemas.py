"""Base schema classes.

Two rules decided in Phase 6 and enforced by these classes:

1. **Public DTOs never expose internal fields.** `created_by`, `updated_by` and
   `version` are editorial metadata. Showing who wrote a record is a privacy decision we
   have not made, so public responses simply do not carry it. Admin responses do.
2. **API field names are `snake_case`.** The generated TypeScript client keeps the same
   names, so a field is called the same thing in the database, the API and the UI.
   One name, everywhere, is worth more than idiomatic camelCase.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from atlas.domain.enums import EntityType

__all__ = [
    "AdminAudit",
    "ApiModel",
    "EntityRef",
    "PublicEntity",
]


class ApiModel(BaseModel):
    """Base for everything that crosses the API boundary."""

    model_config = ConfigDict(
        from_attributes=True,  # build directly from ORM objects
        extra="forbid",  # an unknown field is a bug, not something to ignore
        frozen=True,  # responses are values, never mutated after building
        str_strip_whitespace=True,
        use_enum_values=False,
    )


class EntityRef(ApiModel):
    """A light pointer to another object.

    Used anywhere we mention something without sending the whole record: relation ends,
    graph nodes, search results, breadcrumbs. It carries exactly what a link needs -
    what it is, how to fetch it, and what to show.
    """

    id: UUID
    type: EntityType
    slug: str
    name: str


class PublicEntity(ApiModel):
    """Fields every public object shares."""

    id: UUID
    slug: str
    created_at: datetime
    updated_at: datetime


class AdminAudit(ApiModel):
    """Editorial metadata, added only to admin responses.

    `version` supports optimistic locking: an update sends the version it read, and the
    API rejects the write if someone else changed the row first. Without it, two editors
    silently overwrite each other, which is very hard to notice in a catalog.
    """

    created_by: UUID | None = None
    updated_by: UUID | None = None
    version: int = Field(ge=1)
