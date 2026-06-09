# Task 10 Scope: Static Small-City Data Loading Boundary

## Summary

Task 10 keeps the Lovv small-city map frontend-only while adding a data-loading boundary that looks like the future API integration path.

The selected source is `static-catalog`. It wraps the existing frontend city catalog into the Task 9 API-shaped adapter chain, then exposes the result as `SmallCity[]` for the map, detail card, and planner flow.

## User Request Original

```text
ㄱㄱ
```

## Structured Agent Contract

Continue the remaining approved Lovv Spec task inside `/Users/jeonjonghyeok/Documents/Final`.

- Use the existing Task 10 packet.
- Do not ask for permissions.
- Do not introduce a real backend call, protected API key, or `.env` dependency.
- Make the current city catalog pass through the backend-ready adapter boundary.
- Preserve Korea and Japan map behavior.
- Verify tests, lint, build, and browser-visible map/planner behavior.

## Selected Direction

- Data source: `static-catalog`
- Runtime boundary: frontend-only deterministic catalog loader
- API behavior: no real network request
- Auth: not applicable
- API key: not applicable
- Pagination: simulated in the static loader for contract readiness only
- Error handling: represented through explicit catalog state factories
- Secret handling: no secrets, no client env vars, no `.env` changes

## Goals

- Reuse the Task 9 `SmallCityApiRecord -> SmallCity` adapter path.
- Add a single data-source module that can later be replaced by a fetch-based implementation.
- Keep the map component receiving normalized marker records only.
- Preserve full city detail resolution in the parent app state.
- Represent loading, success, empty, and error states even though the current source is static.
- Keep user-facing UI free of backend, fixture, SDK, API, mock, or route-seed implementation copy.

## Non-Goals

- Do not call a real backend endpoint.
- Do not add a map SDK provider, map API key, clustering library, or dependency.
- Do not change authentication, authorization, login, logout, or profile logic.
- Do not introduce real backend pagination semantics.
- Do not validate production Japanese or Korean city data quality.
- Do not commit `.env`, `.env.local`, or real secrets.

## Affected Frontend Flow

1. Static city rows are converted into API-shaped records.
2. API-shaped records pass through `adaptSmallCityApiResponse`.
3. The resulting `SmallCity[]` becomes the shared catalog state.
4. The map derives marker records from the full city list.
5. The detail card resolves the selected full `SmallCity`.
6. The planner receives selected city context from the detail action.

## Acceptance Criteria

- Static catalog state returns a successful `SmallCity[]` by default.
- Korea defaults to 40 city-name markers.
- Japan switching shows 40 unique city-name markers.
- Search and theme filters operate on city records, not map-specific metadata.
- Loading, empty, and error states are represented in code and covered by tests.
- No real network request is introduced.
- No real env var or secret is introduced.
- The planner entry from selected city detail remains intact.

## Verification

- `npm run test -- --run`
- `npm run lint`
- `npm run build`
- Browser QA on a local Vite server:
  - Korea map visible.
  - Japan country switch visible.
  - Marker counts are correct.
  - City detail opens.
  - AI planner entry opens.
  - No internal debug or backend wording appears.
