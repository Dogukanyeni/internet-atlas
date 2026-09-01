"""Pagination and sorting contract tests."""

import pytest

from atlas.core.errors import ErrorCode, ValidationError
from atlas.core.ids import uuid7
from atlas.core.pagination import (
    CursorParams,
    Page,
    PageParams,
    SortOrder,
    decode_cursor,
    encode_cursor,
)


def test_offset_is_calculated_from_the_page_number() -> None:
    assert PageParams(page=1, page_size=25).offset == 0
    assert PageParams(page=3, page_size=25).offset == 50


def test_page_count_rounds_up() -> None:
    page: Page[str] = Page(items=[], total=101, page=1, page_size=25)

    assert page.pages == 5


def test_page_count_is_zero_when_empty() -> None:
    page: Page[str] = Page(items=[], total=0, page=1, page_size=25)

    assert page.pages == 0


def test_cursor_round_trip() -> None:
    identifier = uuid7()

    assert decode_cursor(encode_cursor(identifier)) == identifier


def test_cursor_has_no_padding_characters() -> None:
    """Padding would be percent-encoded in a URL and make links ugly and fragile."""
    assert "=" not in encode_cursor(uuid7())


def test_broken_cursor_is_a_client_error() -> None:
    with pytest.raises(ValidationError) as raised:
        decode_cursor("this-is-not-a-cursor")

    assert raised.value.code is ErrorCode.INVALID_CURSOR


def test_cursor_params_expose_the_decoded_id() -> None:
    identifier = uuid7()

    params = CursorParams(cursor=encode_cursor(identifier), limit=10)

    assert params.after_id == identifier


def test_no_cursor_means_first_page() -> None:
    assert CursorParams().after_id is None


def test_sort_parses_descending_prefix() -> None:
    order = SortOrder.parse("-created_at", frozenset({"created_at"}), "created_at")

    assert order.field == "created_at"
    assert order.descending


def test_sort_defaults_when_missing() -> None:
    order = SortOrder.parse(None, frozenset({"name", "created_at"}), "name")

    assert order.field == "name"
    assert not order.descending


def test_unknown_sort_field_is_rejected_not_ignored() -> None:
    """A silently ignored sort looks like a broken feature to the user."""
    with pytest.raises(ValidationError) as raised:
        SortOrder.parse("password", frozenset({"name"}), "name")

    assert raised.value.code is ErrorCode.INVALID_SORT
    assert raised.value.details["allowed"] == ["name"]
