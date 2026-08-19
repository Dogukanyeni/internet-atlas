"""Write the OpenAPI schema to a file.

Used by `make openapi` and by CI. CI regenerates this file and fails the build if the
result is different from what is committed — that is our schema-drift alarm (ADR-011).
"""

import json
import sys
from pathlib import Path

from atlas.main import app


def main() -> int:
    if len(sys.argv) < 2:
        sys.stdout.write("usage: python -m atlas.scripts.export_openapi <output-path>\n")
        return 1

    target = Path(sys.argv[1])
    target.parent.mkdir(parents=True, exist_ok=True)

    schema = app.openapi()
    # sort_keys makes the output stable, so the diff only shows real changes.
    # newline="\n" is required: without it Windows writes CRLF, the file differs from
    # the one Linux CI generates, and the drift check fails for no real reason.
    target.write_text(
        json.dumps(schema, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    sys.stdout.write(f"OpenAPI schema written to {target}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
