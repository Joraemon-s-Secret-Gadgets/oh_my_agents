# Task 6 Subtasks: Production Map Provider and Backend City API Integration

## Context and Dependencies

- Previous Task Report: `docs/reports/TASK5_COMPLETION.md`
- Source of Truth:
  - `docs/specs/LOVV_CITY_MAP_DISCOVERY_SPEC.md`
  - `docs/specs/TASK5_LOVV_CITY_MAP_DISCOVERY_SUBTASKS.md`
  - `AGENTS.md`
  - `docs/agents/frontend-agent-rules.md`
  - `docs/agents/modes/sequential.md`
- Target app: `/Users/jeonjonghyeok/Documents/Final/Lovv-pg/frontend`
- Current MVP map provider: Leaflet + OpenStreetMap tiles.
- Current city source: frontend fixture data with 40 Korean and 360 Japanese mock records.
- Proposed next step: only start after user approval, because this task may touch backend APIs, provider keys, quotas, or deployment configuration.

## Startup and Stop Rules

- Use Sequential Mode because this task can involve API contracts, provider keys, and backend/data integration.
- Do not read or edit real `.env`, `.env.local`, or secret files.
- Do not hardcode API keys in frontend code.
- Stop if the chosen map provider, backend API base path, or city source of truth is unclear.
- Stop after three consecutive verification failures or repeated review deadlock.

## Subtask 6.1: Provider Decision and Security Contract

- Purpose: Decide whether production uses Kakao, Naver, Google, Mapbox, OpenStreetMap-compatible hosted tiles, or another provider.
- Target Files:
  - Documentation only unless the user approves implementation.
  - Possible file: `docs/specs/LOVV_MAP_PROVIDER_SECURITY_SPEC.md`
- Acceptance Criteria:
  - Provider choice is documented.
  - Key ownership, domain restrictions, quota limits, billing risk, attribution, and backend proxy needs are documented.
  - Frontend-exposed vs server-only environment variables are clearly separated.
- Verification:
  - Security review against `docs/agents/security-review-checklist.md`.

## Subtask 6.2: Backend City API Contract

- Purpose: Replace fixture assumptions with an API contract for DB-backed city records.
- Target Files:
  - Possible frontend contract/types file.
  - Possible backend API spec document.
- Acceptance Criteria:
  - `GET /api/small-cities` contract is defined for country, query, theme, pagination, and result count.
  - `GET /api/small-cities/:id` contract is defined for detail data.
  - Coordinate precision, source metadata, images, themes, and route seed fields are defined.
  - Error, loading, empty, and stale-data states are defined.
- Verification:
  - Contract review against current `SmallCity` and `PlannerCityContext` types.

## Subtask 6.3: Frontend Data Adapter

- Purpose: Let the map UI consume either fixture data or backend API data without rewriting the UI flow.
- Target Files:
  - `Lovv-pg/frontend/src/data/smallCities.ts`
  - Possible new frontend adapter/hook file.
  - `Lovv-pg/frontend/src/App.tsx`
  - `Lovv-pg/frontend/src/App.test.tsx`
- Acceptance Criteria:
  - Fixture mode remains available for local MVP.
  - API mode handles loading, error, empty, and success states.
  - The planner handoff still uses `PlannerCityContext`.
  - No server-only secret is exposed to the client.
- Verification:
  - `npm run test`
  - `npm run lint`
  - `npm run build`
  - Browser check for loading, error, empty, and success states.

## Subtask 6.4: Production Map Adapter

- Purpose: Swap or wrap the current Leaflet adapter only if the approved provider requires it.
- Target Files:
  - `Lovv-pg/frontend/src/components/SmallCityLeafletMap.tsx` or new provider component.
  - `Lovv-pg/frontend/src/index.css`
  - `Lovv-pg/frontend/src/App.test.tsx`
- Acceptance Criteria:
  - Markers are rendered from latitude/longitude in the provider coordinate system.
  - Marker positions remain correct on resize and country switch.
  - Attribution and provider terms are respected.
  - The map remains keyboard usable through the result list.
- Verification:
  - `npm run test`
  - `npm run lint`
  - `npm run build`
  - Browser check on desktop and mobile widths.

## Subtask 6.5: QA and Regression Review

- Purpose: Verify production-provider/backend integration without regressing the MVP flow.
- Target Files:
  - No implementation files unless fixes are required.
- Acceptance Criteria:
  - QA confirms country switching, filtering, detail panel, and planner handoff.
  - QA confirms key/secret handling is safe.
  - QA confirms provider attribution and marker alignment.
  - QA confirms browser-visible errors are handled.
- Verification:
  - Unit/component tests.
  - Lint.
  - Build.
  - Browser screenshots for Korea and Japan.
  - Security review when provider keys or backend APIs are involved.
