# Recon Log — Flock Energy Urja Meter API

## Instructions
- All observations must be factual.
- Unknown behavior must be marked as "Unknown".
- Do not add guessed endpoints, credentials, cookies, or session tokens.

## Entry Template

| Field | Details |
|-------|---------|
| Date and time | |
| Page or area inspected | |
| Action performed | |
| Observation | |
| Evidence or screenshot reference | |
| Interpretation | |
| Open questions | |

## Investigation Entry — Meters Page

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Meters page |
| Action performed | Reloaded the page and inspected the `search?q=&page=1` request in Chrome DevTools Network |
| Observation | GET request to `https://urja-ops.flockenergy.tech/portal/meters/search?q=&page=1` returned HTTP 200 OK with `application/json` content type. Response contains `data`, `page`, `pageSize`, and `total`. Observed pagination: page 1, pageSize 20, total 403. Meter records contain fields: `meterId`, `serialNo`, `make`, `phaseType`, `installStatus`, `dtCode`. First record examples: meterId `J100000`, serialNo `SE33962`, make `HPL`, phaseType `single`, installStatus `Decommissioned`, dtCode `DT-001`. |
| Evidence or screenshot reference | Chrome DevTools screenshots supplied during this investigation |
| Interpretation | The portal exposes a paginated JSON endpoint for listing meters. No authentication details were captured. |
| Open questions | Whether search matches meter ID and serial number; how later pages behave; what other portal sections expose; authentication/session behavior. |

## Investigation Entry — Manual Meter Search

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Meters page |
| Action performed | Searched for `J100000`, `SE33962`, and `NO_MATCH_12345` in the portal UI search box |
| Observation | Searching `J100000` returned one matching meter. Searching `SE33962` returned the same meter, `J100000`. Searching `NO_MATCH_12345` returned zero results and displayed "No meters found." The displayed pagination was Page 1 of 1 for these searches. |
| Evidence or screenshot reference | Portal UI screenshots supplied by the user |
| Interpretation | Search matches both meter ID and serial number; unmatched queries return an empty result set with a "No meters found" message. |
| Open questions | Authentication/session behavior; how later pages behave when more results exist; what other portal sections expose. |

## Investigation Entry — Pagination Test

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Meters page |
| Action performed | Cleared the search and clicked Next |
| Observation | Page 2 loaded and displayed different meter records. |
| Evidence or screenshot reference | User-reported manual browser observation |
| Interpretation | Pagination advances to page 2 when the user clears the search and clicks Next. |
| Open questions | Exact page 2 request URL and parameters; response pagination metadata; behavior on the last page. |

## Investigation Entry — Transformers Page Investigation

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Transformers / Distribution Transformers |
| Action performed | Reloaded the page and inspected the `dts?page=1` request in Chrome DevTools Network |
| Observation | GET request to `https://urja-ops.flockenergy.tech/portal/dts?page=1` returned HTTP 200 OK with `application/json` content type. Response preview contains a top-level `data` field with transformer records. Visible UI columns: Code, Name, Feeder, Capacity (kVA). Example record: code `DT-001`, name `Malviya Nagar DT 1`, feeder `F-001`, capacity `100` kVA. |
| Evidence or screenshot reference | Chrome DevTools screenshots supplied by the user |
| Interpretation | The portal exposes a JSON endpoint for listing distribution transformers with columns Code, Name, Feeder, and Capacity (kVA). |
| Open questions | Complete response schema; pagination behavior; total record count; authentication/session behavior. |

## Investigation Entry — Transformers Record Fields (Supplementary)

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Transformers / Distribution Transformers |
| Action performed | Expanded the first record in the response Preview of the `dts?page=1` request in Chrome DevTools Network |
| Observation | The expanded first record in the `data` array shows: `code` `DT-001`, `name` `Malviya Nagar DT 1`, `feederCode` `F-001`, `capacityKva` `100`. The response contains a top-level `data` array of transformer records. These fields were visible in the expanded first record only; it is not claimed that these are all fields in every record. |
| Evidence or screenshot reference | Chrome DevTools screenshot supplied by the user |
| Interpretation | Transformer records include at least the fields code, name, feederCode, and capacityKva in the first record. |
| Open questions | Complete response schema for all transformer records; response pagination metadata; total record count; authentication/session behavior. |

## Investigation Entry — Meter Export Investigation

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Transformers / Distribution Transformers |
| Action performed | Clicked the `Export all meters` button and inspected the `export?page=1` request in Chrome DevTools Network |
| Observation | The portal displayed `Exported 403 meters.` A file named `meter-export.json` downloaded successfully. The Network panel showed `export?page=1` with status 200. The Preview showed a top-level `data` field containing meter records, including visible `meterId` and `serialNo` fields. The downloaded file was reported by Chrome as 359 KB. |
| Evidence or screenshot reference | Chrome DevTools screenshot supplied by the user |
| Interpretation | The portal can export all meters to a JSON file named `meter-export.json`. |
| Open questions | Full request URL; HTTP method; response headers; total number of records inside the response; pagination behavior for the export endpoint. |

## Investigation Entry — Authentication and Session Observation

| Field | Details |
|-------|---------|
| Date and time | 2026-10-30, time not recorded |
| Page or area inspected | Meters page |
| Action performed | Inspected the Request Headers of `search?q=&page=1` in Chrome DevTools |
| Observation | The request uses HTTPS and includes a `Cookie` header with a cookie named `__Secure-better-auth.session_token`. |
| Evidence or screenshot reference | Screenshot supplied by the user |
| Interpretation | The observed request relies on a session cookie being sent with the request. |
| Open questions | Session lifetime; login/session renewal behavior; whether an Authorization header is used by other requests; how an API client should obtain and maintain an authenticated session. |

