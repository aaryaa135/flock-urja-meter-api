"""API routes for transformer listing."""

from fastapi import APIRouter, Cookie, HTTPException, Query

from app.config import settings
from app.portal.client import PortalClient, PortalClientError
from app.portal.models import TransformerListResponse
from app.service.transformer_service import list_transformers

router = APIRouter(prefix="/transformers", tags=["transformers"])


def _get_client(cookies: dict[str, str] | None) -> PortalClient:
    return PortalClient(base_url=settings.PORTAL_BASE_URL, cookies=cookies)


@router.get("", response_model=TransformerListResponse)
def list_transformers_endpoint(
    page: int = Query(default=1, ge=1, description="Page number"),
    session_cookie: str | None = Cookie(
        default=None,
        alias="__Secure-better-auth.session_token",
        description="Portal session cookie observed in browser",
    ),
) -> TransformerListResponse:
    """List distribution transformers via the portal.

    Forwarded to the verified portal endpoint:
    GET /portal/dts?page=<page>

    Requires the portal session cookie (__Secure-better-auth.session_token) to be
    sent by the client. The authentication/acquisition flow for this cookie is
    not yet verified.
    """
    cookies = None
    if session_cookie:
        cookies = {"__Secure-better-auth.session_token": session_cookie}

    client = _get_client(cookies)
    try:
        return list_transformers(client, page=page, cookies=cookies)
    except PortalClientError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        client.close()
