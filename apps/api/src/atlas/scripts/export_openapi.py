"""Write the OpenAPI schema to a file.

Used by `make openapi` and by CI. CI regenerates this file and fails the build if the
result is different from what is committed — that is our schema-drift alarm (ADR-011).

The script does one thing beyond asking FastAPI for the schema: it also adds the
**domain contract models** to `components.schemas`, even when no endpoint uses them yet.

Why: Phase 6 fixes the data contract, but the endpoints that serve it arrive in Phases 9
to 11. Without this, the frontend could not generate types for `WebsiteDetail` or
`GraphNeighborhood` until months later, and would write them by hand in the meantime -
exactly the drift ADR-011 exists to prevent. The models are real Pydantic classes, so
what we publish here is the same thing the endpoints will return.
"""

import json
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel
from pydantic.json_schema import models_json_schema

from atlas.domain import schemas as domain_schemas
from atlas.main import app


def _contract_models() -> list[type[BaseModel]]:
    """Every model listed in `atlas.domain.schemas.__all__`."""
    models: list[type[BaseModel]] = []
    for name in domain_schemas.__all__:
        candidate = getattr(domain_schemas, name)
        if isinstance(candidate, type) and issubclass(candidate, BaseModel):
            models.append(candidate)
    return models


def _add_contract_models(schema: dict[str, Any]) -> None:
    """Merge the domain models into components.schemas, without overwriting."""
    _, top_level = models_json_schema(
        [(model, "serialization") for model in _contract_models()],
        ref_template="#/components/schemas/{model}",
    )
    definitions: dict[str, Any] = top_level.get("$defs", {})

    components = schema.setdefault("components", {}).setdefault("schemas", {})
    for name, definition in definitions.items():
        # An endpoint-backed model always wins: it is the one really being served.
        components.setdefault(name, definition)


def main() -> int:
    if len(sys.argv) < 2:
        sys.stdout.write("usage: python -m atlas.scripts.export_openapi <output-path>\n")
        return 1

    target = Path(sys.argv[1])
    target.parent.mkdir(parents=True, exist_ok=True)

    schema: dict[str, Any] = app.openapi()
    _add_contract_models(schema)

    # sort_keys makes the output stable, so the diff only shows real changes.
    # newline="\n" is required: without it Windows writes CRLF, the file differs from
    # the one Linux CI generates, and the drift check fails for no real reason.
    target.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    count = len(schema.get("components", {}).get("schemas", {}))
    sys.stdout.write(f"OpenAPI schema written to {target} ({count} models)\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
