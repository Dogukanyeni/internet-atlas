"""Entity identifiers.

Decision (Q10, open since Phase 3): **UUID version 7**.

A UUIDv7 starts with a 48-bit millisecond timestamp, so ids sort by creation time.
That matters for us in three places:

* B-tree indexes stay compact, because new rows are appended instead of scattered
  (the main problem with random UUIDv4 as a primary key).
* Cursor pagination can order by id and get a stable, meaningful order for free.
* Debugging is easier: an id tells you roughly when the row was created.

Rejected: UUIDv4 (random, bad index locality), auto-increment integers (leak how many
rows exist and make merging data sets painful), ULID (same benefits, but stored as text
or a custom type instead of the native PostgreSQL `uuid`).

We generate the value in the application, not in the database, so a service can build a
complete object graph before writing anything.
"""

import secrets
import time
from uuid import UUID

__all__ = ["is_uuid7", "uuid7"]


def uuid7() -> UUID:
    """Return a time-ordered UUID version 7.

    Layout (RFC 9562): 48 bits of Unix time in milliseconds, 4 version bits,
    12 random bits, 2 variant bits, 62 random bits.

    Two ids created in the same millisecond have no defined order between them. That is
    fine for us: nothing in the product depends on ordering inside one millisecond.
    """
    timestamp_ms = int(time.time() * 1000)
    raw = bytearray(timestamp_ms.to_bytes(6, "big") + secrets.token_bytes(10))

    raw[6] = (raw[6] & 0x0F) | 0x70  # version 7
    raw[8] = (raw[8] & 0x3F) | 0x80  # RFC 4122 variant

    return UUID(bytes=bytes(raw))


def is_uuid7(value: UUID) -> bool:
    """True if the value is a version 7 UUID. Used in tests and data checks."""
    return value.version == 7
