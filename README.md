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
