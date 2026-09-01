"""UUIDv7 tests.

The point of choosing v7 was time ordering. If that breaks, index locality and cursor
pagination both quietly get worse, so it is worth a real test.
"""

import time

from atlas.core.ids import is_uuid7, uuid7


def test_version_and_variant_are_correct() -> None:
    value = uuid7()

    assert value.version == 7
    assert is_uuid7(value)
    assert (value.bytes[8] & 0xC0) == 0x80  # RFC 4122 variant bits


def test_ids_are_unique() -> None:
    values = {uuid7() for _ in range(10_000)}

    assert len(values) == 10_000


def test_ids_sort_by_creation_time() -> None:
    first = uuid7()
    time.sleep(0.01)  # cross a millisecond boundary
    second = uuid7()

    assert first < second
    assert str(first) < str(second)


def test_timestamp_is_close_to_now() -> None:
    now_ms = int(time.time() * 1000)

    encoded_ms = int.from_bytes(uuid7().bytes[:6], "big")

    assert abs(encoded_ms - now_ms) < 1000
