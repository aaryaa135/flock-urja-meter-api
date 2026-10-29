"""API routes for meter search and listing."""

from fastapi import APIRouter, Cookie, HTTPException, Query

from app.config import settings
from app.portal.client import PortalClient, PortalClientError
from app.portal.models import MeterSearchResponse
from app.service.meter_service import list_meters, search_meters

router = APIRouter(prefix="/meters", tags=["meters"])


def _get_client(cookies: dict[str, str] | None) -> PortalClient:
    return PortalClient(base_url=settings.PORTAL_BASE_URL, cookies=cookies)


@router.get("/search", response_model=MeterSearchResponse)
def search_meters_endpoint(
    q: str = Query(default="", description="Search query (meter ID or serial number)"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, description="Page size"),
    session_cookie: str | None = Cookie(
        default=None,
        alias="__Secure-better-auth.session_token",
        description="Portal session cookie observed in browser",
    ),
) -> MeterSearchResponse:
    """Search meters via the portal.

    Forwarded to the verified portal endpoint:
    GET /portal/meters/search?q=<q>&page=<page>

    Requires the portal session cookie (__Secure-better-auth.session_token) to be
    sent by the client. The authentication/acquisition flow for this cookie is
    not yet verified.
    """
    cookies = None
    if session_cookie:
        cookies = {"__Secure-better-auth.session_token": session_cookie}

    client = _get_client(cookies)
    try:
        return search_meters(client, query=q, page=page, page_size=page_size, cookies=cookies)
    except PortalClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        client.close()


@router.get("", response_model=MeterSearchResponse)
def list_meters_endpoint(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, description="Page size"),
    session_cookie: str | None = Cookie(
        default=None,
        alias="__Secure-better-auth.session_token",
        description="Portal session cookie observed in browser",
    ),
) -> MeterSearchResponse:
    """List meters with an empty search query (verified default behavior)."""
    cookies = None
    if session_cookie:
        cookies = {"__Secure-better-auth.session_token": session_cookie}

    client = _get_client(cookies)
    try:
        return list_meters(client, page=page, page_size=page_size, cookies=cookies)
    except PortalClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        client.close()
