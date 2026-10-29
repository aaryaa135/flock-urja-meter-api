"""Service layer for meter operations."""

from typing import Any

from app.portal.client import PortalClient, PortalClientError
from app.portal.models import MeterSearchResponse


def search_meters(
    client: PortalClient,
    query: str = "",
    page: int = 1,
    page_size: int = 20,
    cookies: dict[str, str] | None = None,
) -> MeterSearchResponse:
    """Search meters via the portal.

    Mirrors the verified portal endpoint:
    GET /portal/meters/search?q=<query>&page=<page>

    Verified behavior:
    - Returns JSON with top-level data, page, pageSize, total.
    - Search matches both meter ID and serial number.
    - Unmatched queries return zero results.
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")

    params: dict[str, Any] = {"q": query, "page": page}
    response = client.get("/portal/meters/search", params=params, cookies=cookies)

    if response.status_code >= 400:
        raise PortalClientError(
            f"Portal meter search failed with status {response.status_code}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise PortalClientError(
            f"Portal meter search returned invalid JSON: {exc}"
        ) from exc

    return MeterSearchResponse.model_validate(payload)


def list_meters(
    client: PortalClient,
    page: int = 1,
    page_size: int = 20,
    cookies: dict[str, str] | None = None,
) -> MeterSearchResponse:
    """List meters with an empty search query (verified default behavior)."""
    return search_meters(client, query="", page=page, page_size=page_size, cookies=cookies)
