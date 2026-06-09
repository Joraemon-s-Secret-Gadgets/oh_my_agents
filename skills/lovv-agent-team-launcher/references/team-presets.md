# Lovv Agent Team Presets

Use these presets when selecting a team for a GitHub Issue.

## Planning Team

Use for new ideas, unclear requirements, product planning, requirements, design, or task breakdown.

- Execution Mode: Sequential Mode for ambiguous work, Hybrid Mode for clear planning updates.
- Coordinator: Main Codex.
- Members:
  - Spec Agent
  - Task Agent
- Order:
  1. Spec Agent drafts or updates requirements/design.
  2. Task Agent splits approved Spec into Tasks/Subtasks.
  3. Main Codex asks for user approval before implementation.

## Frontend Feature Team

Use for React, Tailwind, UI flows, routes, components, hooks, client state, responsive behavior, and accessibility.

- Execution Mode: Hybrid Mode by default.
- Coordinator: Main Codex.
- Members:
  - Frontend Implementation Agent
  - Frontend QA Review Agent
- Order:
  1. Implementation Agent edits only approved frontend scope.
  2. QA Review Agent reviews visible behavior, accessibility, responsive behavior, and tests.
  3. Main Codex summarizes integration and asks before commit/PR.

## Backend API Team

Use for Lovv AWS SAM APIs, Lambda handlers, API Gateway contracts, Aurora MySQL data access, migrations or schema work, server validation, and backend tests.

When the work overlaps small-city APIs, city data loading, frontend API adapters, or map/backend integration, include the Existing API Source Of Truth section from `docs/projects/lovv-project-context.md` as required context. Treat Task 9/10 API documents as the current contract and adapter boundary, not as proof that a live AWS SAM backend endpoint already exists. Treat listed endpoint paths as placeholders until real SAM/API Gateway deployment, stage/base URL, auth/environment configuration, and DB readiness are verified.

- Execution Mode: Sequential Mode by default.
- Coordinator: Main Codex.
- Members:
  - Backend Implementation Agent
  - Backend API Review Agent
- Order:
  1. Implementation Agent edits approved backend/API scope.
  2. API Review Agent checks contracts, validation, error behavior, data integrity, and tests.
  3. Main Codex summarizes integration and asks before commit/PR.

## Security Review Team

Use for auth, authorization, token handling, secrets, environment files, dependency risk, redirects, external APIs, or sensitive data.

- Execution Mode: Sequential Mode.
- Coordinator: Main Codex.
- Members:
  - Security Review Agent
  - Domain Review Agent when frontend/backend scope is known
- Order:
  1. Security Review Agent reviews risks and blockers.
  2. Domain Review Agent checks domain-specific behavior if needed.
  3. Main Codex requires fixes before approval.

## Crawl Data Team

Use for crawling, scraping, URL data extraction, BeautifulSoup, Selenium, Scrapling, or crawl output review.

- Execution Mode: Sequential Mode by default.
- Coordinator: Main Codex.
- Members:
  - Crawl Implementation Agent
  - Crawl QA Review Agent
- Required Inputs:
  - URLs
  - Columns
  - Output path
  - Output format
  - Allowed tools
  - Rate limit
  - Stop condition
- Order:
  1. Crawl Implementation Agent writes scoped Python 3.12 crawl script.
  2. Crawl QA Review Agent checks output columns, source_url, retrieved_at, failure_reason, and safety rules.
  3. Main Codex asks before committing output data or generated artifacts.

## Release Gate Team

Use before merge, demo, release, or final validation.

- Execution Mode: Sequential Mode.
- Coordinator: Main Codex.
- Members:
  - Review Agent
  - QA Review Agent
  - Security Review Agent when sensitive scope exists
- Order:
  1. Review Agent checks spec alignment and code quality.
  2. QA Review Agent checks workflow and regression risk.
  3. Security Review Agent checks sensitive areas if applicable.
  4. Main Codex summarizes blockers and readiness.
