"""Service layer for transformer operations."""

from typing import Any

from app.portal.client import PortalClient, PortalClientError
from app.portal.models import TransformerListResponse


def list_transformers(
    client: PortalClient,
    page: int = 1,
    cookies: dict[str, str] | None = None,
) -> TransformerListResponse:
    """List distribution transformers via the portal.

    Mirrors the verified portal endpoint:
    GET /portal/dts?page=<page>

    Verified behavior:
    - Returns JSON with a top-level data array of transformer records.
    - First observed record fields: code, name, feederCode, capacityKva.
    - Complete schema and pagination behavior are not yet verified.
    """
    if page < 1:
        raise ValueError("page must be >= 1")

    params: dict[str, Any] = {"page": page}
    response = client.get("/portal/dts", params=params, cookies=cookies)

    if response.status_code >= 400:
        raise PortalClientError(
            f"Portal transformer list failed with status {response.status_code}"
        )

    try:
        payload = response.json()
    except ValueError as exc:
        raise PortalClientError(
            f"Portal transformer list returned invalid JSON: {exc}"
        ) from exc

    return TransformerListResponse.model_validate(payload)
