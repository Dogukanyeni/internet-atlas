"""Meta endpoints: the vocabulary of the product, served to clients.

Why this exists as a real endpoint instead of a constant in the frontend: relation
types, their direction and their labels are product rules. If the frontend keeps its own
copy, the two drift, and the interface starts showing wrong labels for edges. One
source, fetched once and cached.
"""

from fastapi import APIRouter
from pydantic import BaseModel

from atlas.domain.enums import (
    EntityType,
    Provenance,
    PublicationStatus,
    RelationType,
    WebsiteKind,
)
from atlas.domain.relations import RELATION_RULES, Direction

router = APIRouter(prefix="/meta", tags=["meta"])


class RelationTypeInfo(BaseModel):
    type: RelationType
    direction: Direction
    label: str
    inverse_label: str
    description: str
    allowed_pairs: list[list[EntityType]]


class EnumsResponse(BaseModel):
    entity_types: list[EntityType]
    node_types: list[EntityType]
    website_kinds: list[WebsiteKind]
    publication_statuses: list[PublicationStatus]
    provenances: list[Provenance]
    relation_types: list[RelationTypeInfo]


@router.get("/enums", response_model=EnumsResponse)
async def enums() -> EnumsResponse:
    """Everything a client needs to render filters, labels and legends."""
    return EnumsResponse(
        entity_types=list(EntityType),
        node_types=[EntityType.WEBSITE, EntityType.TOPIC, EntityType.TECHNOLOGY],
        website_kinds=list(WebsiteKind),
        publication_statuses=list(PublicationStatus),
        provenances=list(Provenance),
        relation_types=[
            RelationTypeInfo(
                type=rule.type,
                direction=rule.direction,
                label=rule.label,
                inverse_label=rule.inverse_label,
                description=rule.description,
                allowed_pairs=[[source, target] for source, target in sorted(rule.allowed_pairs)],
            )
            for rule in RELATION_RULES.values()
        ],
    )
