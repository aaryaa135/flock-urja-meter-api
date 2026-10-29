# PROTOCOL — Flock Energy Urja Meter API

Protocol notes, verified observations, assumptions, unknowns, trade-offs,
skipped features, and reflection for the take-home implementation.

---

## 1. Verified observations

These were observed directly in the Flock Energy Urja portal (Chrome DevTools
Network panel) and are recorded in `RECON_LOG.md`:

- **Meter search**: `GET /portal/meters/search?q=&page=1` → HTTP 200,
  `application/json`. Response contains `data`, `page`, `pageSize`, `total`.
  Observed: page=1, pageSize=20, total=403.
- **Meter fields** (verified): `meterId`, `serialNo`, `make`, `phaseType`,
  `installStatus`, `dtCode`. Example: `J100000`, `SE33962`, `HPL`, `single`,
  `Decommissioned`, `DT-001`.
- **Meter search behavior**: Searching `J100000` returned one matching meter.
  Searching `SE33962` returned the same meter (`J100000`). Searching
  `NO_MATCH_12345` returned zero results ("No meters found").
- **Pagination**: Page 2 loaded after clearing search and clicking Next.
- **Transformers**: `GET /portal/dts?page=1` → HTTP 200, `application/json`.
  Top-level `data` array. First record fields: `code`, `name`, `feederCode`,
  `capacityKva`. Example: `DT-001`, `Malviya Nagar DT 1`, `F-001`, `100`.
- **Export**: Clicking "Export all meters" triggered `export?page=1` (status
  200), downloaded `meter-export.json` (359 KB), portal displayed
  "Exported 403 meters."
- **Authentication**: Browser requests include a `Cookie` header with
  `__Secure-better-auth.session_token`. HTTPS is used.
- **Keys endpoint**: `GET /portal/keys` returned JSON containing a field named
  `signingSecret`. This value is **never** printed, stored, exposed, or
  hardcoded. Its purpose is not assumed.

---

## 2. Assumptions

- The portal base URL is `https://urja-ops.flockenergy.tech` (configurable via
  `PORTAL_BASE_URL`).
- The meter search endpoint accepts `q` and `page` query parameters, matching
  the verified request `search?q=&page=1`.
- Search matches both meter ID and serial number (verified for two examples).
- An empty search query (`q=""`) returns the full paginated list.
- The transformer endpoint accepts a `page` parameter (`dts?page=1`).
- The session cookie `__Secure-better-auth.session_token` must be forwarded by
  the client for authenticated portal requests.

---

## 3. Unknowns

- **Authentication flow**: How to obtain, renew, or refresh the
  `__Secure-better-auth.session_token` cookie is not verified.
- **Authorization header**: It is unknown whether any portal request uses an
  `Authorization` header in addition to or instead of the session cookie.
- **Transformer schema completeness**: Only the first transformer record was
  expanded; other fields may exist.
- **Transformer pagination**: Page/total metadata for transformers is unknown.
- **Meter export details**: Full request URL, HTTP method, response headers,
  and record count inside the export response are unknown.
- **Session lifetime and renewal**: Unknown.
- **Ops Desk**: Non-clickable during investigation; no data available.
- **signingSecret purpose**: Unknown and not assumed.

---

## 4. Trade-offs

- **No authentication implementation**: Because the auth flow is unverified,
  the API exposes the session cookie as a pass-through parameter rather than
  implementing login. This avoids fabricating authentication logic.
- **Pydantic `extra="allow"`**: Unknown response metadata is preserved rather
  than stripped or invented, to avoid losing data the portal may return.
- **No database, caching, or frontend**: Out of scope for a minimal,
  testable submission. The service is a stateless adapter.
- **Timeouts hardcoded at 10s**: A sensible default; configurable via the
  `PortalClient` constructor if needed later.
- **No `.env` committed**: `.env.example` is provided; `.env` is gitignored.

---

## 5. Skipped features

- Frontend/UI
- Database or persistence layer
- Caching
- Meter export endpoint (verified in portal but not implemented in API)
- Transformer search/filtering (only listing verified)
- Authentication/login endpoints
- `/portal/keys` integration (signingSecret observed but purpose unknown)
- Ops Desk integration (non-clickable during investigation)

---

## 6. Reflection questions

### Q1. What was the most significant technical decision you made, and why?

The most significant decision was to **not implement authentication** and
instead treat the session cookie as an opaque pass-through. The portal requires
`__Secure-better-auth.session_token` but the login/renewal flow is unverified.
Implementing a guessed auth flow would risk fabricating behavior that doesn't
match the portal. A clean adapter boundary with documented unknowns is more
honest and safer for a take-home submission.

### Q2. What are the main limitations of your implementation, and how would you address them with more time?

Limitations:
1. No authentication — clients must manually supply the session cookie.
2. Transformer schema is partially verified (first record only).
3. No live integration tests — all tests use mocks.

With more time, I would: verify the auth flow (login endpoint, cookie
acquisition/renewal), expand transformer schema verification across multiple
records, add integration tests against a portal test instance, and implement
the meter export endpoint.

### Q3. What assumptions did you make that could turn out to be wrong?

1. That `GET /portal/meters/search?q=&page=1` is the correct pattern for all
   meter search requests (other query parameters may exist).
2. That an empty `q` returns the full list (verified for page 1 only).
3. That the transformer endpoint behaves the same on page 2+ (unverified).
4. That forwarding the session cookie is sufficient for authorization (other
   headers may be required).
5. That `signingSecret` is not needed for the API client (purpose unknown).

### Q4. What would you prioritize if you had to extend this implementation?

1. Verify and implement authentication (login, session refresh, cookie
   management).
2. Expand transformer schema verification and add pagination metadata.
3. Add integration tests against a staging portal instance.
4. Implement the meter export endpoint.
5. Add structured logging and metrics.

### Q5. How does your design separate verified behavior from unverified assumptions?

The service layer mirrors verified portal endpoints exactly (URL, parameters,
response shape). Pydantic models include only verified fields with
`extra="allow"` to preserve unknown metadata. All unverified items (auth flow,
full schema, pagination metadata, export details) are documented as open
questions in PROTOCOL.md and RECON_LOG.md, not assumed in code.
