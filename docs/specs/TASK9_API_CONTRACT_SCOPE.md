# Task 9 Scope: Backend/API Contract Scaffolding

## User Request Original

```text
그래 그래
```

## Structured Agent Contract

Proceed with Task 9 using the previously recommended direction: backend/API contract scaffolding. Do not ask for additional permission. Do not connect a real backend, use real provider credentials, add environment variables, or introduce secrets. Add a bounded frontend adapter and documentation that prepares Lovv's city map data flow for future backend integration.

## Selected Direction

Task 9 direction: `Backend/API contract scaffolding`.

## In Scope

- Define the small-city list/detail API contract.
- Add frontend types for the expected API response.
- Add an adapter that converts backend-style records into the existing `SmallCity` frontend model.
- Preserve the Task 8 boundary: `SmallCity[] -> SmallCityMapMarker[] -> SmallCityLeafletMap`.
- Add tests for valid rows, rejected invalid rows, query generation, and metadata separation.

## Out of Scope

- Real network calls.
- Real backend endpoint implementation.
- Database migrations.
- API keys, `.env`, `.env.local`, or provider credentials.
- Authenticated requests.
- Real ranking or personalization scoring.
- Map provider replacement.

## Acceptance Criteria

- API response rows can be adapted into `SmallCity[]`.
- Invalid rows are rejected without crashing.
- Internal backend metadata does not flow into map markers.
- Query serialization supports country, search query, themes, page, and page size.
- Existing tests, lint, and build pass.
