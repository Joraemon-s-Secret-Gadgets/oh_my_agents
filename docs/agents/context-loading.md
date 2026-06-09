## Context Loading & Token Budget Rule

Agents must reduce token cost by loading only the context required for the current role and Task/Subtask.

Default loading rules:

- Load this root `AGENTS.md` and the nearest relevant folder-level `AGENTS.md`.
- Always load `docs/projects/lovv-project-context.md` before choosing role, domain, execution mode, stack assumption, or harness route in this project.
- Do not load `AGENTS.ko.md` unless the user asks for Korean explanation, the task edits Korean documentation, or the task checks synchronization between `AGENTS.md` and `AGENTS.ko.md`. This restriction does not override the File Synchronization Rule when agent documentation is being edited.
- Do not load all files in `docs/agents` at startup.
- Do not load `docs/prompts` files unless the current task explicitly asks for a prompt template.
- Exception: Crawl Focus tasks must load `docs/prompts/crawl-task-prompt.md` even when the user did not explicitly ask for a prompt template. Crawl Focus includes crawling, scraping, URL extraction, deep crawling, BeautifulSoup, Selenium, and Scrapling work.
- Exception: Frontend domain tasks must load `docs/agents/frontend-agent-rules.md` even when the user did not explicitly ask for frontend rules. Frontend domain includes UI, React, TailwindCSS, browser-facing behavior, routes, components, hooks, client state, forms, accessibility, responsive behavior, and frontend API integration.
- Use `rg` or targeted section reads before opening long files.
- Prefer referenced sections, short task packets, and current changed files over full-document reads.

## Token Management Rule

Baseline context for this project is root `AGENTS.md` plus `docs/projects/lovv-project-context.md`.

Do not eagerly load:

- `AGENTS.ko.md`.
- All files under `docs/agents/`.
- All execution mode files.
- All Specs or reports.
- All prompt templates.
- Whole source folders.
- Large unmanaged files, logs, generated outputs, or data dumps.

Load context in this order:

1. User request and preserved `User Request Original`.
2. Root `AGENTS.md`.
3. `docs/projects/lovv-project-context.md`.
4. Exactly one selected execution mode file.
5. Current role-specific rule file only when needed.
6. Current Subtask packet or approved Spec section references.
7. Target files, changed files, or diff.

When spawning subagents, pass a compact context packet instead of broad documents:

- Role, domain, focus, execution mode.
- Source of truth paths and required sections.
- Allowed scope and forbidden scope.
- Acceptance criteria.
- Verification commands.
- Stop condition and escalation rule.
- Short summary of relevant prior decisions.

If a subagent needs more context, it must request specific files, sections, or command output. It must not load broad directories, full Specs, full reports, or unrelated source files by default.

For large files or command output:

- Check size or use targeted search before reading.
- Read only relevant sections or line ranges.
- Summarize logs, crawl output, screenshots, browser output, and test output before handoff.
- Keep only actionable errors, verification results, and decision-relevant evidence.

## Crawl Focus Loading

For Crawl Focus tasks:

- Load `docs/prompts/crawl-task-prompt.md` before planning, implementation, or review.
- Do not load unrelated prompt templates.
- Ask for missing URLs, columns, output format, output path, allowed tools, verification, and stop condition before implementation.
- For deep crawling, also require seed URLs, domain allowlist, max depth, max pages, rate limit, output columns, and stop condition.
- Summarize large crawl results before passing them to another agent.

## Frontend Domain Loading

For Frontend domain tasks:

- Load `docs/agents/frontend-agent-rules.md` before planning, implementation, or review.
- Do not load unrelated frontend docs or design assets unless needed for the active Task/Subtask.
- Ask for missing target files or folders, UI states, API/data assumptions, verification, and out-of-scope behavior before implementation.
- Load `docs/agents/security-review-checklist.md` when frontend work touches client environment variables, auth UI, token handling, redirects, user-generated content, external scripts, or dependency changes.
- Summarize large design references, screenshots, or browser logs before passing them to another agent.

## Backend AWS SAM Domain Loading

For Backend AWS SAM or API domain tasks:

- Load `docs/projects/lovv-project-context.md` before planning, implementation, or review.
- If the task touches small-city APIs, city data loading, map/backend integration, API Gateway routes, Lambda handlers, SAM templates, or frontend API adapters, read the Existing API Source Of Truth section in `docs/projects/lovv-project-context.md`.
- Read only the listed API source-of-truth documents that match the active Task/Subtask; do not load every report or Spec by default.
- Treat Task 9/10 API documents as the current contract and adapter boundary, not as proof of a deployed backend.
- Treat endpoint paths in those documents as placeholders until the actual SAM/API Gateway base URL, stage, auth/environment configuration, and DB readiness are verified.
- Do not implement live API calls if the current implementation remains frontend-only or backend/DB readiness is unclear.
- Do not create conflicting endpoints, response shapes, filters, pagination rules, metadata exposure rules, or adapter behavior unless a new approved Spec changes the contract.

## Role-Based Loading

Spec Agent should load:

- Root `AGENTS.md`.
- Relevant user request and product context.
- `docs/projects/lovv-project-context.md`.
- Existing Specs or source sections needed to write the current Spec.
- `docs/agents/spec-task-format.md` when writing Spec or Task-related sections.

Task Agent should load:

- Root `AGENTS.md`.
- `docs/projects/lovv-project-context.md`.
- The approved Full Spec or the required Full Spec sections.
- Existing Spec Summary if present.
- `docs/agents/spec-task-format.md`.
- This file when preparing Subtasks for Implementation Agent.

Implementation Agent should load:

- Root `AGENTS.md`.
- `docs/projects/lovv-project-context.md` when the Subtask touches stack routing, API, RAG, database, crawl, infrastructure, persistence, or cross-domain behavior.
- Nearest relevant folder-level `AGENTS.md`, if one exists for the target files.
- The current Subtask instruction.
- Only the Full Spec sections listed in `Must Read Before Implementation`.
- Additional referenced Full Spec sections only when the Subtask context is insufficient.

Review Agent should load:

- Root `AGENTS.md`.
- `docs/projects/lovv-project-context.md` when reviewing stack routing, API, RAG, database, crawl, infrastructure, persistence, or cross-domain behavior.
- Current Subtask instruction.
- Changed files.
- Acceptance criteria and referenced Full Spec sections needed to verify behavior.
- `docs/agents/review-format.md`.
- `docs/agents/security-review-checklist.md` only when the change is security-sensitive under the root security rule.

## Spec Summary Rule

Spec Summary documents are indexes, not replacements for the Full Spec.

- Spec Summary must not be treated as authoritative.
- Full Spec is the source of truth for requirements, acceptance criteria, API contracts, data models, security rules, and user-visible behavior.
- Spec Summary should help agents find relevant Full Spec sections quickly.
- Spec Summary should include coverage notes when a topic is full, partial, or not covered.

Recommended Spec Summary format:

```md
# Spec Summary: [feature name]

This summary is not authoritative. Use it only to find relevant Full Spec sections.

## Source of Truth

- Full Spec: `docs/specs/[FEATURE]_SPEC.md`

## Section Map

- User flow: `#user-flow`
- Theme selection: `#theme-selection`
- API contract: `#api-contract`
- Security requirements: `#security`
- Acceptance criteria: `#acceptance-criteria`

## Coverage

- Theme selection: full
- Recommendation ranking: partial
- Community review: not covered
```

## Subtask Context Packet Rule

Task Agent must make each Subtask usable without forcing Implementation Agent to read the entire Full Spec.

Each Subtask should include:

- Purpose.
- Required Context.
- Context Budget.
- Source of Truth.
- Required Sections.
- Must Read Before Implementation.
- Target Files.
- Out of Scope.
- Acceptance Criteria.
- Verification.

Recommended Subtask format:

```md
### Subtask [number]: [title]

- Purpose: 이 작업이 필요한 이유를 한글로 설명합니다.
- Required Context:
  - 이 Subtask 구현에 반드시 필요한 Spec 맥락만 적습니다.
- Context Budget:
  - Must read:
  - Do not read:
  - Optional read:
- Source of Truth:
  - Full Spec: `docs/specs/[FEATURE]_SPEC.md`
- Required Sections:
  - `#relevant-section`
  - `#acceptance-criteria`
- Must Read Before Implementation:
  - `#relevant-section`
  - `#acceptance-criteria`
- Target Files:
  - `path/to/file`
- Out of Scope:
  - 이번 Subtask에서 구현하지 않을 범위를 적습니다.
- Acceptance Criteria:
  - 완료로 판단할 수 있는 기준을 원문 의미가 손상되지 않게 적습니다.
- Verification:
  - 실행할 테스트, 빌드, 린트, 수동 확인 방법을 적습니다.
```

## Implementation Spec Reading Rule

Implementation Agent must not read the entire Full Spec by default.

Implementation Agent must:

1. Read the current Subtask instruction first.
2. Read every section listed under `Must Read Before Implementation`.
3. Read additional referenced Full Spec sections only when the Subtask context is insufficient.
4. Stop and ask the user if the Subtask, referenced Spec sections, or acceptance criteria conflict.

Implementation Agent must read the referenced Full Spec sections before changing behavior related to:

- User-visible behavior.
- Acceptance criteria.
- API contracts.
- Data models or migrations.
- Authentication or authorization.
- Security, privacy, or sensitive data.
- External APIs or file handling.

## Review Spec Reading Rule

Review Agent must verify against the relevant Full Spec sections, not only against the Spec Summary.

Review Agent should:

- Compare the implementation with the current Subtask's acceptance criteria.
- Read referenced Full Spec sections for user-visible behavior, API contracts, data models, security-sensitive changes, and acceptance criteria.
- Treat missing or unclear Spec references as a review finding or escalation point.
