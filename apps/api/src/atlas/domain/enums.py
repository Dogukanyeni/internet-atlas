"""Shared vocabulary.

These enums are the code version of the Phase 3 information architecture. They are the
single place where the words of the product are defined, so the database, the API and
the frontend can never disagree about them.

Rule: a value is never removed or renamed after it is used in stored data. Adding is
safe; changing is a migration.
"""

from enum import StrEnum

__all__ = [
    "NODE_TYPES",
    "EntityType",
    "Provenance",
    "PublicationStatus",
    "RelationType",
    "WebsiteKind",
]


class EntityType(StrEnum):
    """Every kind of object that can be referenced by id in the API."""

    WEBSITE = "website"
    TOPIC = "topic"
    TECHNOLOGY = "technology"
    CATEGORY = "category"
    PATH = "path"
    COLLECTION = "collection"


#: The three types that can appear as nodes on the map (Phase 3, glossary).
#: Categories filter, they do not appear on the graph.
NODE_TYPES: frozenset[EntityType] = frozenset(
    {EntityType.WEBSITE, EntityType.TOPIC, EntityType.TECHNOLOGY}
)


class WebsiteKind(StrEnum):
    """What a Website record actually is.

    Decision I-01: one Website entity with a kind field, instead of separate Product and
    Website tables.
    """

    PRODUCT = "product"
    TOOL = "tool"
    SERVICE = "service"
    DOCS = "docs"
    COMMUNITY = "community"
    LEARNING = "learning"
    REFERENCE = "reference"


class PublicationStatus(StrEnum):
    """Lifecycle of any editorial object (Phase 3, section 6).

    There is no `deleted`. Public content is archived, never hard deleted (I-06).
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


class ArchiveReason(StrEnum):
    """Why an object was archived. Shown to users as a badge."""

    DEAD_SITE = "dead_site"
    MERGED = "merged"
    REMOVED = "removed"
    SUPERSEDED = "superseded"


class Provenance(StrEnum):
    """Where a fact came from.

    Every published relation must carry this (data-quality target D2). It is also what
    lets us find and remove everything one bad source produced.
    """

    EDITORIAL = "editorial"
    CRAWLER = "crawler"
    DETECTOR = "detector"
    AI = "ai"
    COMMUNITY = "community"


class RelationType(StrEnum):
    """The relation dictionary from Phase 3.

    Direction and allowed node pairs are defined in `atlas.domain.relations`, not here,
    so the rules live next to the code that enforces them.
    """

    BELONGS_TO = "belongs_to"
    BUILT_WITH = "built_with"
    PROVIDES = "provides"
    ALTERNATIVE_TO = "alternative_to"
    COMPETITOR_OF = "competitor_of"
    INTEGRATES_WITH = "integrates_with"
    PART_OF = "part_of"
    RELATED_TO = "related_to"
    REPLACED_BY = "replaced_by"
    INSPIRED_BY = "inspired_by"
    RECOMMENDS = "recommends"
