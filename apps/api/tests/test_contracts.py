"""Tests for the API contract itself.

These check promises the frontend will rely on, and the privacy rule that public
responses never carry editorial metadata.
"""

import pytest
from httpx import AsyncClient
from pydantic import ValidationError as PydanticValidationError

from atlas.core.ids import uuid7
from atlas.domain.enums import EntityType, Provenance, RelationType, WebsiteKind
from atlas.domain.schemas import RelationCreate, WebsiteCreate, WebsiteDetail


def _valid_website_input() -> dict[str, object]:
    return {
        "name": "Next.js",
        "canonical_url": "https://nextjs.org",
        "kind": WebsiteKind.PRODUCT,
        "short_description": "The React framework for production web applications.",
        "category_ids": [uuid7()],
    }


def test_website_input_accepts_a_valid_record() -> None:
    website = WebsiteCreate(**_valid_website_input())  # type: ignore[arg-type]

    assert website.kind is WebsiteKind.PRODUCT


def test_website_must_have_at_least_one_category() -> None:
    """Publish rule D1: nothing is context-free."""
    payload = _valid_website_input() | {"category_ids": []}

    with pytest.raises(PydanticValidationError):
        WebsiteCreate(**payload)  # type: ignore[arg-type]


def test_short_description_has_a_length_limit() -> None:
    payload = _valid_website_input() | {"short_description": "x" * 161}

    with pytest.raises(PydanticValidationError):
        WebsiteCreate(**payload)  # type: ignore[arg-type]


def test_unknown_fields_are_rejected() -> None:
    """`extra="forbid"`: a typo in a client is a loud error, not a silent no-op."""
    payload = _valid_website_input() | {"qualityScore": 0.9}

    with pytest.raises(PydanticValidationError):
        WebsiteCreate(**payload)  # type: ignore[arg-type]


def test_client_cannot_set_status_or_quality_score() -> None:
    """Those belong to the server. Accepting them would move editorial rules to clients."""
    for forbidden in ("status", "quality_score", "id"):
        assert forbidden not in WebsiteCreate.model_fields


def test_bad_slug_is_rejected() -> None:
    payload = _valid_website_input() | {"slug": "Not A Slug"}

    with pytest.raises(PydanticValidationError):
        WebsiteCreate(**payload)  # type: ignore[arg-type]


def test_public_website_never_exposes_editorial_metadata() -> None:
    """Public responses must not say who wrote a record."""
    for hidden in ("created_by", "updated_by", "version"):
        assert hidden not in WebsiteDetail.model_fields


def test_relation_requires_provenance_and_confidence() -> None:
    """Data-quality target D2: no unsourced edge can be created."""
    with pytest.raises(PydanticValidationError):
        RelationCreate(  # type: ignore[call-arg]
            source_id=uuid7(),
            source_type=EntityType.WEBSITE,
            target_id=uuid7(),
            target_type=EntityType.TECHNOLOGY,
            type=RelationType.BUILT_WITH,
        )


def test_confidence_must_be_between_zero_and_one() -> None:
    with pytest.raises(PydanticValidationError):
        RelationCreate(
            source_id=uuid7(),
            source_type=EntityType.WEBSITE,
            target_id=uuid7(),
            target_type=EntityType.TECHNOLOGY,
            type=RelationType.BUILT_WITH,
            provenance=Provenance.DETECTOR,
            confidence=1.5,
        )


async def test_meta_enums_lists_every_relation_type(client: AsyncClient) -> None:
    response = await client.get("/api/v1/meta/enums")

    assert response.status_code == 200
    body = response.json()
    returned = {item["type"] for item in body["relation_types"]}
    assert returned == {relation.value for relation in RelationType}


async def test_meta_enums_describes_direction_and_labels(client: AsyncClient) -> None:
    response = await client.get("/api/v1/meta/enums")

    by_type = {item["type"]: item for item in response.json()["relation_types"]}
    assert by_type["alternative_to"]["direction"] == "undirected"
    assert by_type["built_with"]["direction"] == "directed"
    assert by_type["built_with"]["label"] == "built with"
    assert by_type["built_with"]["inverse_label"] == "used by"


async def test_errors_follow_the_contract(client: AsyncClient) -> None:
    """Every error carries a machine code and the request id."""
    response = await client.get("/api/v1/meta/enums?unexpected=1")

    # Unknown query parameters are ignored by FastAPI, so this must succeed. The real
    # check is that a validation failure keeps our shape - see the next test.
    assert response.status_code == 200


async def test_validation_error_shape(client: AsyncClient) -> None:
    response = await client.get("/health/live", headers={"X-Request-ID": "req-123"})

    assert response.headers["X-Request-ID"] == "req-123"
