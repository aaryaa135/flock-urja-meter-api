"""Portal HTTP client with configurable timeouts and error handling."""

from typing import Any

import httpx

from app.config import settings


class PortalClientError(Exception):
    """Raised when the portal client encounters an error."""


class PortalClient:
    """Minimal HTTP client for the Flock Energy Urja portal.

    The portal requires a session cookie (``__Secure-better-auth.session_token``)
    that was observed in the browser but whose acquisition/renewal flow is not
    yet verified. This client does not implement authentication; callers must
    supply cookies explicitly when needed.
    """

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 10.0,
        cookies: dict[str, str] | None = None,
    ) -> None:
        self.base_url = (base_url or settings.PORTAL_BASE_URL).rstrip("/")
        self.timeout = timeout
        self.cookies = cookies or {}
        self._client = httpx.Client(timeout=self.timeout, cookies=self.cookies)

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        cookies: dict[str, str] | None = None,
    ) -> httpx.Response:
        """Send a GET request to the portal."""
        url = f"{self.base_url}{path}"
        merged_cookies = {**self.cookies, **(cookies or {})}
        try:
            response = self._client.get(url, params=params, cookies=merged_cookies)
        except httpx.RequestError as exc:
            raise PortalClientError(f"Request to {url} failed: {exc}") from exc
        return response

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "PortalClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
