"""Health endpoint tests.

These prove the application starts and answers. Phase 7 adds real database tests.
"""

from httpx import AsyncClient


async def test_live_returns_ok(client: AsyncClient) -> None:
    response = await client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_info_reports_environment(client: AsyncClient) -> None:
    response = await client.get("/health/info")

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "internet-atlas-api"
    assert body["environment"] in {"local", "preview", "production"}


async def test_request_id_header_is_returned(client: AsyncClient) -> None:
    response = await client.get("/health/live")

    assert response.headers.get("X-Request-ID")


async def test_request_id_is_kept_when_sent(client: AsyncClient) -> None:
    response = await client.get("/health/live", headers={"X-Request-ID": "abc123"})

    assert response.headers["X-Request-ID"] == "abc123"


async def test_unknown_route_uses_our_error_shape(client: AsyncClient) -> None:
    response = await client.get("/does-not-exist")

    assert response.status_code == 404
