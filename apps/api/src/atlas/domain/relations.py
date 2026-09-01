"""Rules for every relation type.

This turns the Phase 3 relation dictionary into data the code can check. Phase 11 uses
it to reject invalid edges before they reach the database, and the meta endpoint serves
it to the frontend so filters and labels never drift from the backend.

Two things are defined per type:

* **direction** — directed means source and target mean different things; undirected
  means the pair is symmetric.
* **allowed pairs** — which node types may be connected.

Undirected relations are stored once, with the smaller id as source (decision I-05).
`normalise_pair` is the single place that rule is applied.
"""

from dataclasses import dataclass
from enum import StrEnum
from uuid import UUID

from atlas.domain.enums import EntityType, RelationType

__all__ = [
    "RELATION_RULES",
    "Direction",
    "RelationRule",
    "is_pair_allowed",
    "normalise_pair",
]


class Direction(StrEnum):
    DIRECTED = "directed"
    UNDIRECTED = "undirected"


@dataclass(frozen=True, slots=True)
class RelationRule:
    """Everything the system knows about one relation type."""

    type: RelationType
    direction: Direction
    allowed_pairs: frozenset[tuple[EntityType, EntityType]]
    label: str
    inverse_label: str
    description: str

    @property
    def is_undirected(self) -> bool:
        return self.direction is Direction.UNDIRECTED


W = EntityType.WEBSITE
T = EntityType.TOPIC
X = EntityType.TECHNOLOGY
P = EntityType.PATH


RELATION_RULES: dict[RelationType, RelationRule] = {
    RelationType.BELONGS_TO: RelationRule(
        type=RelationType.BELONGS_TO,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, T), (X, T)}),
        label="belongs to",
        inverse_label="includes",
        description="The website or technology is part of this subject.",
    ),
    RelationType.BUILT_WITH: RelationRule(
        type=RelationType.BUILT_WITH,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, X)}),
        label="built with",
        inverse_label="used by",
        description="The product or site is built using this technology.",
    ),
    RelationType.PROVIDES: RelationRule(
        type=RelationType.PROVIDES,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, X)}),
        label="provides",
        inverse_label="provided by",
        description="The product offers this technology as its service.",
    ),
    RelationType.ALTERNATIVE_TO: RelationRule(
        type=RelationType.ALTERNATIVE_TO,
        direction=Direction.UNDIRECTED,
        allowed_pairs=frozenset({(W, W), (X, X)}),
        label="alternative to",
        inverse_label="alternative to",
        description="Does the same job. A user would choose one of them.",
    ),
    RelationType.COMPETITOR_OF: RelationRule(
        type=RelationType.COMPETITOR_OF,
        direction=Direction.UNDIRECTED,
        allowed_pairs=frozenset({(W, W)}),
        label="competitor of",
        inverse_label="competitor of",
        description="Same market. Business rivals.",
    ),
    RelationType.INTEGRATES_WITH: RelationRule(
        type=RelationType.INTEGRATES_WITH,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, W), (W, X)}),
        label="integrates with",
        inverse_label="has an integration from",
        description="Works together with the target, usually built by the source.",
    ),
    RelationType.PART_OF: RelationRule(
        type=RelationType.PART_OF,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, W), (X, X), (T, T)}),
        label="part of",
        inverse_label="contains",
        description="Belongs to a bigger family or ecosystem.",
    ),
    RelationType.RELATED_TO: RelationRule(
        type=RelationType.RELATED_TO,
        direction=Direction.UNDIRECTED,
        allowed_pairs=frozenset({(W, W), (W, X), (W, T), (X, X), (X, T), (T, T)}),
        label="related to",
        inverse_label="related to",
        description="Meaningful closeness with no better type.",
    ),
    RelationType.REPLACED_BY: RelationRule(
        type=RelationType.REPLACED_BY,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, W), (X, X)}),
        label="replaced by",
        inverse_label="replaces",
        description="The source is dead, renamed or migrated to the target.",
    ),
    RelationType.INSPIRED_BY: RelationRule(
        type=RelationType.INSPIRED_BY,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(W, W), (X, X)}),
        label="inspired by",
        inverse_label="inspired",
        description="Clear historical influence.",
    ),
    RelationType.RECOMMENDS: RelationRule(
        type=RelationType.RECOMMENDS,
        direction=Direction.DIRECTED,
        allowed_pairs=frozenset({(P, W), (P, T), (P, X)}),
        label="recommends",
        inverse_label="recommended by",
        description="A step inside an exploration route.",
    ),
}


def is_pair_allowed(relation_type: RelationType, source: EntityType, target: EntityType) -> bool:
    """Check the node types against the dictionary.

    For undirected types the pair is checked in both orders, because the stored order is
    decided by id, not by meaning.
    """
    rule = RELATION_RULES[relation_type]
    if (source, target) in rule.allowed_pairs:
        return True
    return rule.is_undirected and (target, source) in rule.allowed_pairs


def normalise_pair(
    relation_type: RelationType,
    source_id: UUID,
    target_id: UUID,
    source_type: EntityType,
    target_type: EntityType,
) -> tuple[UUID, UUID, EntityType, EntityType]:
    """Put an undirected relation into its canonical order (decision I-05).

    Without this, "A is an alternative to B" and "B is an alternative to A" become two
    rows, the map draws the edge twice, and the unique index cannot help.
    """
    if RELATION_RULES[relation_type].is_undirected and target_id < source_id:
        return target_id, source_id, target_type, source_type
    return source_id, target_id, source_type, target_type
