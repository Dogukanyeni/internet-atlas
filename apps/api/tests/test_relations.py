"""Relation dictionary tests.

These rules are what stop the graph from filling with nonsense edges, so they are tested
before any code can create a relation.
"""

import pytest

from atlas.core.ids import uuid7
from atlas.domain.enums import EntityType, RelationType
from atlas.domain.relations import (
    RELATION_RULES,
    Direction,
    is_pair_allowed,
    normalise_pair,
)


def test_every_relation_type_has_a_rule() -> None:
    """A type without a rule could never be validated, so it must not exist."""
    assert set(RELATION_RULES) == set(RelationType)


@pytest.mark.parametrize("rule", RELATION_RULES.values(), ids=lambda r: r.type.value)
def test_rules_are_complete(rule: object) -> None:
    assert rule.allowed_pairs
    assert rule.label
    assert rule.description


def test_website_can_be_built_with_technology() -> None:
    assert is_pair_allowed(RelationType.BUILT_WITH, EntityType.WEBSITE, EntityType.TECHNOLOGY)


def test_technology_cannot_be_built_with_website() -> None:
    """built_with is directed: the reverse direction is meaningless."""
    assert not is_pair_allowed(RelationType.BUILT_WITH, EntityType.TECHNOLOGY, EntityType.WEBSITE)


def test_topic_cannot_be_built_with_anything() -> None:
    assert not is_pair_allowed(RelationType.BUILT_WITH, EntityType.TOPIC, EntityType.TECHNOLOGY)


def test_undirected_pairs_are_allowed_in_both_orders() -> None:
    assert RELATION_RULES[RelationType.RELATED_TO].direction is Direction.UNDIRECTED

    assert is_pair_allowed(RelationType.RELATED_TO, EntityType.WEBSITE, EntityType.TOPIC)
    assert is_pair_allowed(RelationType.RELATED_TO, EntityType.TOPIC, EntityType.WEBSITE)


def test_undirected_relation_is_stored_in_one_canonical_order() -> None:
    """Decision I-05: the smaller id is always the source.

    Without this, the same "A is an alternative to B" edge can be stored twice.
    """
    first, second = sorted([uuid7(), uuid7()])

    forward = normalise_pair(
        RelationType.ALTERNATIVE_TO, first, second, EntityType.WEBSITE, EntityType.WEBSITE
    )
    backward = normalise_pair(
        RelationType.ALTERNATIVE_TO, second, first, EntityType.WEBSITE, EntityType.WEBSITE
    )

    assert forward == backward
    assert forward[0] == first


def test_directed_relation_keeps_its_order() -> None:
    first, second = sorted([uuid7(), uuid7()])

    source_id, target_id, _, _ = normalise_pair(
        RelationType.BUILT_WITH, second, first, EntityType.WEBSITE, EntityType.TECHNOLOGY
    )

    assert (source_id, target_id) == (second, first)


def test_node_types_are_swapped_together_with_ids() -> None:
    """A swap that moves ids but not their types would corrupt the edge."""
    first, second = sorted([uuid7(), uuid7()])

    _, _, source_type, target_type = normalise_pair(
        RelationType.RELATED_TO, second, first, EntityType.TECHNOLOGY, EntityType.TOPIC
    )

    assert (source_type, target_type) == (EntityType.TOPIC, EntityType.TECHNOLOGY)
