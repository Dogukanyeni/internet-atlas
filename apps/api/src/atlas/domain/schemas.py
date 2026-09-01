"""The data contract.

These are the shapes the API promises to send and accept. Phases 9 to 11 build the
tables and services behind them, but the contract is fixed here so the frontend can be
built against something real instead of invented types.

Naming rule:

* `...Summary` — what a card or list row needs. Small on purpose.
* `...Detail`  — what one full page needs.
* `...Create` / `...Update` — admin input.

A list endpoint returns summaries, never details. This is not only about speed: a list
of full records tempts the frontend to render a page from a list item, and then the two
shapes slowly drift apart.
"""

from datetime import date, datetime
from typing import Annotated
from uuid import UUID

from pydantic import Field, HttpUrl, StringConstraints

from atlas.core.schemas import ApiModel, EntityRef, PublicEntity
from atlas.domain.enums import (
    ArchiveReason,
    EntityType,
    Provenance,
    PublicationStatus,
    RelationType,
    WebsiteKind,
)

__all__ = [
    "CategorySummary",
    "GraphEdge",
    "GraphNeighborhood",
    "GraphNode",
    "RelationCreate",
    "RelationGroup",
    "RelationView",
    "TechnologyDetail",
    "TechnologySummary",
    "TopicDetail",
    "TopicSummary",
    "WebsiteCreate",
    "WebsiteDetail",
    "WebsiteSummary",
    "WebsiteUpdate",
]

# Slug rules from Phase 3, section 5: lower case, letters, digits and hyphens, max 60.
Slug = Annotated[str, StringConstraints(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=60)]

# One sentence. The limit is what fits on a card and in a search result.
ShortText = Annotated[str, StringConstraints(min_length=10, max_length=160)]

Score = Annotated[float, Field(ge=0.0, le=1.0)]


# --------------------------------------------------------------------------- taxonomy


class CategorySummary(PublicEntity):
    """A filtering drawer. Editors only; never created by users."""

    name: str
    parent_id: UUID | None = None


class TopicSummary(PublicEntity):
    name: str
    short_description: str | None = None
    website_count: int = Field(ge=0)


class TopicDetail(TopicSummary):
    long_description: str | None = None
    parent: EntityRef | None = None
    children: list[TopicSummary] = Field(default_factory=list)
    featured_websites: list["WebsiteSummary"] = Field(default_factory=list)
    related_topics: list[TopicSummary] = Field(default_factory=list)


class TechnologySummary(PublicEntity):
    name: str
    short_description: str | None = None
    website_count: int = Field(ge=0)


class TechnologyDetail(TechnologySummary):
    long_description: str | None = None
    homepage_url: HttpUrl | None = None
    topics: list[TopicSummary] = Field(default_factory=list)


# --------------------------------------------------------------------------- website


class WebsiteSummary(PublicEntity):
    """What a card shows. Kept small on purpose."""

    name: str
    kind: WebsiteKind
    primary_domain: str
    short_description: ShortText
    logo_url: HttpUrl | None = None
    quality_score: Score | None = None
    status: PublicationStatus


class WebsiteDetail(WebsiteSummary):
    """Everything one website page needs, in one response.

    The detail page must answer four questions on one screen (Phase 2, F1): what is it,
    which area, what is it connected to, what are the alternatives. So relations travel
    with the record instead of needing a second request.
    """

    canonical_url: HttpUrl
    long_description: str | None = None
    organization_name: str | None = None  # plain text in v1 (decision I-02)
    screenshot_url: HttpUrl | None = None
    launch_date: date | None = None

    categories: list[CategorySummary] = Field(default_factory=list)
    topics: list[TopicSummary] = Field(default_factory=list)
    technologies: list[TechnologySummary] = Field(default_factory=list)
    relations: list["RelationGroup"] = Field(default_factory=list)

    # Trust, shown in the interface and never hidden (vision behaviour 4).
    last_verified_at: datetime | None = None
    archive_reason: ArchiveReason | None = None
    replaced_by: EntityRef | None = None


# --------------------------------------------------------------------------- relations


class RelationView(ApiModel):
    """One edge, as the interface shows it."""

    id: UUID
    type: RelationType
    label: str  # already resolved for the reading direction
    target: EntityRef
    weight: Score
    confidence: Score
    provenance: Provenance
    note: str | None = None


class RelationGroup(ApiModel):
    """Relations of one type, grouped so the page can render sections directly."""

    type: RelationType
    label: str
    items: list[RelationView]
    total: int = Field(ge=0)


# --------------------------------------------------------------------------- graph


class GraphNode(ApiModel):
    """A node as the map draws it. Deliberately tiny — hundreds travel at once."""

    id: UUID
    type: EntityType
    slug: str
    name: str
    kind: WebsiteKind | None = None
    degree: int = Field(ge=0, description="How many published relations this node has.")


class GraphEdge(ApiModel):
    id: UUID
    type: RelationType
    source_id: UUID
    target_id: UUID
    weight: Score


class GraphNeighborhood(ApiModel):
    """The answer to `GET /graph/neighbors/{id}`.

    `truncated` is part of the contract, not an afterthought: the map must be able to
    tell the user "there is more here" instead of quietly hiding nodes. Limits come from
    decision A-10 — depth 3, 300 nodes.
    """

    focus: EntityRef
    depth: int = Field(ge=1, le=3)
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    truncated: bool = False


# --------------------------------------------------------------------------- admin input


class WebsiteCreate(ApiModel):
    """Admin input. Note what is missing: no id, no status, no quality score.

    The server owns those. Letting a client choose an id or publish directly would move
    editorial rules out of the service layer, which is where they belong.
    """

    name: Annotated[str, StringConstraints(min_length=1, max_length=120)]
    canonical_url: HttpUrl
    kind: WebsiteKind
    short_description: ShortText
    long_description: str | None = None
    organization_name: str | None = None
    launch_date: date | None = None
    category_ids: list[UUID] = Field(min_length=1)
    topic_ids: list[UUID] = Field(default_factory=list)
    slug: Slug | None = Field(default=None, description="Generated from the name when not given.")


class WebsiteUpdate(ApiModel):
    """Partial update.

    `version` is required: the client sends the version it read, and the server rejects
    the write if the row changed since then (`version_conflict`). Two editors working on
    the same record must not silently overwrite each other.
    """

    version: int = Field(ge=1)

    name: Annotated[str, StringConstraints(min_length=1, max_length=120)] | None = None
    canonical_url: HttpUrl | None = None
    kind: WebsiteKind | None = None
    short_description: ShortText | None = None
    long_description: str | None = None
    organization_name: str | None = None
    launch_date: date | None = None
    category_ids: list[UUID] | None = None
    topic_ids: list[UUID] | None = None


class RelationCreate(ApiModel):
    """Creating an edge.

    `provenance` and `confidence` are required, with no default. A default would let an
    unsourced fact enter the graph quietly, and data-quality target D2 says every
    published relation must say where it came from.
    """

    source_id: UUID
    source_type: EntityType
    target_id: UUID
    target_type: EntityType
    type: RelationType
    provenance: Provenance
    confidence: Score
    weight: Score = 0.5
    note: Annotated[str, StringConstraints(max_length=200)] | None = None
