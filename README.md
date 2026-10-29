# Flock Energy Urja Meter API

Minimal FastAPI service for meter search/listing and transformer listing,
built from verified observations of the Flock Energy Urja portal.

## Project status

This is a take-home implementation. The service is a thin adapter over the
portal's JSON endpoints. Authentication is **not yet verified** — the portal
requires a session cookie (`__Secure-better-auth.session_token`) that was
observed in the browser, but the login/session-acquisition flow is unknown.

## Verified observations (from RECON_LOG.md)

| Area | Endpoint | Method | Status | Key findings |
|------|----------|--------|--------|--------------|
| Meters search | `/portal/meters/search?q=&page=1` | GET | 200 | Response has `data`, `page`, `pageSize`, `total`. Observed: page=1, pageSize=20, total=403. Meter fields: `meterId`, `serialNo`, `make`, `phaseType`, `installStatus`, `dtCode`. Search matches both meter ID and serial number. |
| Transformers | `/portal/dts?page=1` | GET | 200 | Response has top-level `data` array. First record fields: `code`, `name`, `feederCode`, `capacityKva`. |
| Meter export | `export?page=1` | — | 200 | Downloaded `meter-export.json` (359 KB). Portal displayed "Exported 403 meters." |
| Authentication | — | — | — | Requests include `Cookie: __Secure-better-auth.session_token`. Flow not verified. |

## Setup

1. Ensure Python 3.11 is available.
2. Create and activate the virtual environment:
   ```
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```
   python -m pip install fastapi uvicorn httpx pydantic pydantic-settings python-dotenv pytest
   ```
4. Copy `.env.example` to `.env` and fill in values (do not commit `.env`):
   ```
   copy .env.example .env
   ```

## Run the server

```
python -m uvicorn app.main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Returns `{"status": "ok"}` |
| `/meters/search` | GET | Search meters (query `q`, `page`, `page_size`). Requires portal session cookie. |
| `/meters` | GET | List meters (empty search). Requires portal session cookie. |
| `/transformers` | GET | List distribution transformers (`page`). Requires portal session cookie. |
| `/openapi.json` | GET | OpenAPI schema |

### Sample requests

```bash
# Health check
curl http://127.0.0.1:8000/health

# Search meters (requires session cookie)
curl "http://127.0.0.1:8000/meters/search?q=J100000&page=1&page_size=20" \
  -H "Cookie: __Secure-better-auth.session_token=<your-session-token>"

# List transformers
curl "http://127.0.0.1:8000/transformers?page=1" \
  -H "Cookie: __Secure-better-auth.session_token=<your-session-token>"
```

## Run tests

Tests use mocks — no live portal access required:

```
python -m pytest tests/ -v
```

## Authentication

The portal requires a session cookie (`__Secure-better-auth.session_token`) that
was observed in Chrome DevTools. This API does **not** implement login or session
renewal. The client must supply the cookie via the `Cookie` header. How to
obtain and maintain this session is unverified — see PROTOCOL.md.

## Known limitations

- Authentication flow is not verified; no login endpoint is implemented.
- Transformer response schema is partially verified (first record only).
- Pagination behavior beyond page 1 is not fully verified.
- `signingSecret` field observed in `/portal/keys` is intentionally not used or exposed.
- Ops Desk was non-clickable during investigation; not implemented.

## Files

- `app/main.py` — FastAPI app, `/health`, router wiring
- `app/config.py` — Pydantic-settings configuration
- `app/portal/client.py` — httpx client with timeout/error handling
- `app/portal/models.py` — Pydantic models for verified fields only
- `app/service/meter_service.py` — Meter service layer
- `app/service/transformer_service.py` — Transformer service layer
- `app/api/meters.py` — Meter API routes
- `app/api/transformers.py` — Transformer API routes
- `tests/` — Mocked unit tests (no live portal)
- `openapi.json` — Generated OpenAPI schema
- `RECON_LOG.md` — Portal investigation notes (preserved)
- `.env.example` — Environment variable template (do not commit `.env`)

## Reflection

### What assumptions did you make?

I assumed the portal base URL is `https://urja-ops.flockenergy.tech`, that the meter search endpoint accepts `q` and `page` query parameters matching the verified request `search?q=&page=1`, that an empty search query returns the full paginated list, that the transformer endpoint accepts a `page` parameter (`dts?page=1`), and that forwarding the session cookie `__Secure-better-auth.session_token` is sufficient for authorization. These assumptions are documented in `PROTOCOL.md` Section 2 and are explicitly marked as potentially wrong.

### Which part was the most difficult, and how did you get unstuck?

The most difficult part was understanding the legacy portal's request structure and session-cookie behavior. Chrome DevTools showed that browser requests include a `Cookie` header with `__Secure-better-auth.session_token`, but the complete authentication flow — how to obtain, renew, or refresh the cookie — was not verified. I got unstuck by drawing a clear boundary: the API exposes the session cookie as an opaque pass-through parameter rather than implementing login logic. Verified observations (endpoint URLs, response fields, pagination values) were separated from unknowns (auth flow, full transformer schema, pagination metadata) and documented in `RECON_LOG.md` and `PROTOCOL.md`.

### If you had another day, what would you improve?

I would verify live authenticated integration safely against a staging portal instance, test pagination across multiple pages beyond page 1, improve session handling with automatic cookie refresh if a login flow is discovered, and add integration tests alongside the existing mocked unit tests. I would also expand transformer schema verification across multiple records and implement the meter export endpoint that was verified in the portal but not implemented in the API.

### What mistake did you make while solving this?

During initial Git setup, I confused the Git repository root and ran Git commands in the parent user directory (`C:\Users\tg157`) instead of the project directory (`C:\Users\tg157\flock-urja-meter-api`). This was resolved by initializing a separate Git repository in the project directory and adding the remote `https://github.com/aaryaa135/flock-urja-meter-api.git`. No unrelated files were committed; only project files are tracked.

### If you were reviewing your own submission, what would you criticise?

I would criticise that the authentication flow remains unverified and no login endpoint is implemented, leaving clients to manually supply the session cookie. The transformer schema is only partially verified from the first record, and all tests are mocked — there are no live integration tests. The reflection answers are documented in `PROTOCOL.md` rather than inline in `README.md`, which makes them harder to discover. These are honest limitations of a time-constrained submission, not hidden defects.
