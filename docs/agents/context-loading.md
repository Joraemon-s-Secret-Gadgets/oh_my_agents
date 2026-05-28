## Context Loading & Token Budget Rule

Agents must reduce token cost by loading only the context required for the current role and Task/Subtask.

Default loading rules:

- Load this root `AGENTS.md` and the nearest relevant folder-level `AGENTS.md`.
- Do not load `AGENTS.ko.md` unless the user asks for Korean explanation, the task edits Korean documentation, or the task checks synchronization between `AGENTS.md` and `AGENTS.ko.md`. This restriction does not override the File Synchronization Rule when agent documentation is being edited.
- Do not load all files in `docs/agents` at startup.
- Do not load `docs/prompts` files unless the current task explicitly asks for a prompt template.
- Use `rg` or targeted section reads before opening long files.
- Prefer referenced sections, short task packets, and current changed files over full-document reads.

## Role-Based Loading

Spec Agent should load:

- Root `AGENTS.md`.
- Relevant user request and product context.
- Existing Specs or source sections needed to write the current Spec.
- `docs/agents/spec-task-format.md` when writing Spec or Task-related sections.

Task Agent should load:

- Root `AGENTS.md`.
- The approved Full Spec or the required Full Spec sections.
- Existing Spec Summary if present.
- `docs/agents/spec-task-format.md`.
- This file when preparing Subtasks for Implementation Agent.

Implementation Agent should load:

- Root `AGENTS.md`.
- Nearest relevant folder-level `AGENTS.md`, if one exists for the target files.
- The current Subtask instruction.
- Only the Full Spec sections listed in `Must Read Before Implementation`.
- Additional referenced Full Spec sections only when the Subtask context is insufficient.

Review Agent should load:

- Root `AGENTS.md`.
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
