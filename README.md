# sap-pyodata-test-service

Oryonix service that calls **SAP S/4HANA Cloud** OData service **API_BUSINESS_PARTNER** (Business Partner, A2X) using `requests`, matching the SAP API Business Hub sandbox pattern (APIKey header only).

> Note: The brief mentioned “Oracle Business Accelerator Hub”; the reference script and this service target **SAP API Business Hub** / SAP OData.

## Layout

- `service/main.py` — flows and compute (canonical).
- `src/main.py` — re-exports flows for `onix artifact build` when the toolchain expects `src/main.py`.
- `spec/server.yaml` — OpenAPI 3.0.0; `operationId` matches flow names.
- `ui/build/index.html` — minimal UI placeholder.
- `artifacts/` — build output directory (per Oryonix layout).
- `requirements.txt` — `requests`.

## Design (Oryonix)

| Piece | Role |
|--------|------|
| `fetch_s4hana_api_rows` | `@onix.action` — OData HTTP + parsing inside a durable action. |
| `list_business_partners` | `@onix.flow` — orchestrates one compute call; returns JSON. |
| `list_business_partners_safe` | `@onix.flow` — same, but returns structured errors for connectivity checks. |

- **Parallel stages:** none; a single sequential read.
- **Signals / human gate:** not used.
- **Streaming:** not used (no generator yields).
- **flow_id:** not required (no signal API).
- **Idempotency keys:** not used (read-only GET semantics).
- **Replay safety:** OData read is retried by Temporal; no duplicate writes.

All calls from the flow into compute use **keyword arguments** only.

## Request body

POST JSON to the mapped routes (see `spec/server.yaml`):

- `api_key` (required) — value for the `APIKey` header on SAP sandbox.
- `service_url` (optional) — defaults to SAP sandbox `API_BUSINESS_PARTNER` URL.
- `top` (optional, default `5`) — page size for `get_entities().top(...)`.
