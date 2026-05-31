# AGENTS.md

This is the MAX context version of the project agent instructions.

Use this file for Pro/MAX users who do not want to optimize for token cost and prefer one comprehensive `AGENTS.md` instead of the token-saving split version in the project root and `docs/agents/*`.

This file intentionally inlines the major planning, agent creation, review, security, crawl, and folder-level rules. It does not remove safety limits. Agents must still protect secrets, avoid workspace escapes, avoid heavy unmanaged files, and stop on ambiguity or deadlock.

## Instruction Priority

Follow instructions in this order:

1. User's explicit instructions.
2. The project root `AGENTS.md`.
3. This MAX `AGENTS.md` as a comprehensive operating guide for Pro/MAX users.
4. The nearest folder-level `AGENTS.md` for domain-specific local rules that do not weaken root rules.
5. General agent defaults.

When instructions conflict, the higher-priority instruction wins. Folder-level and MAX rules may add detail, but they must not weaken root-level security, workflow, environment, or Workspace Boundary rules.

## MAX Context Mode

MAX Context Mode means:

- Prefer this file as the single comprehensive agent operating guide.
- Do not skip relevant agent-operation sections only to save tokens.
- You may use the full planning, review, security, and agent creation rules in this file without loading split `docs/agents/*` files first.
- If a split document is newer or explicitly referenced by the user, check it before acting.
- Do not load `AGENTS.ko.md` unless the user asks for Korean explanation, Korean docs are being edited, or synchronization is being checked.
- Do not read heavy unmanaged files, `.git` internals, large logs, build artifacts, or large data files just because MAX mode is enabled.

## Top-Level Principles

1. Work only inside the current project workspace.
2. Do not read, edit, move, delete, or format files outside the workspace.
3. Follow the approved Spec before writing implementation code.
4. Break work into feature-level Tasks before implementation.
5. Break large Tasks into smaller Subtasks before implementation.
6. Implement one Task or Subtask at a time.
7. Review each completed Task or Subtask before moving to the next one.
8. If review finds issues, fix them and run review again.
9. Do not modify unrelated files or unrelated behavior.
10. Prefer existing project patterns over new abstractions.
11. Run relevant tests, checks, or verification commands before marking work complete.
12. Security, correctness, and maintainability take priority over speed.
13. Escalation on Deadlock: If the Fix & Re-review loop between Implementation Agent and Review Agent repeats three consecutive times, or if progress is blocked by a technical limitation, stop, report the situation, and request user intervention.
14. Git Commit Convention: Commits should be scoped by Subtask whenever possible and must follow Conventional Commits 1.0.0.
15. Environment Variable Safety: Never hardcode or commit real secrets from `.env`, `.env.local`, or other environment files. Share only dummy structure through `.env.example`.

## Workspace Boundary

Allowed inside the workspace:

- Read project files.
- Create, edit, move, or delete files required for approved Tasks.
- Run project-local development, testing, formatting, and verification commands.
- Generate temporary, cache, or build artifacts inside the workspace.

Forbidden:

- Do not read, edit, move, delete, or format files outside the current workspace.
- Do not modify other repositories, parent directories, home files, global config files, shell profiles, IDE settings, or OS settings.
- Do not use `../` to access unrelated projects.
- Do not install or change global dependencies unless explicitly approved.
- Do not run destructive commands outside the approved Task scope.
- Do not read entire `.git` internals, large `.log` files, build artifacts, or data files of tens of MB or more unless explicitly requested.
- Do not track `.env`, `.env.local`, or other real environment files. Confirm they are ignored and block them from `git add` or commits.

If a Task appears to require access outside the workspace, stop and ask for explicit user approval.

## Agent Progress & Handoff

Agents must not silently stall.

- Progress Update Interval: If work continues for 4 minutes, provide a short status update with active role, Task/Subtask, current action, and early findings.
- No-Progress Limit: If there is no meaningful progress for 5 minutes, stop active work instead of silently continuing.
- Stalled Work Handover: Before stopping, write active role, Task/Subtask, goal, files touched, commands run, what worked, what failed, blocker, risk if continued, and recommended next action.
- Handoff Options: Ask whether to hand off to Main Codex, create a fresh same-role agent, or allow one more bounded attempt.
- Main Codex Handoff: Prefer when direction, requirements, architecture, coordination, or user intent needs clarification.
- Same-Role Fresh Agent Handoff: Prefer when scope is clear but the current agent is repeating the same failure.
- No Silent Retry: Do not repeatedly retry the same failing command, test, implementation, or review loop without reporting progress and changing approach.

## Git Commit Convention

Use the official Conventional Commits 1.0.0 structure:

```md
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

Rules:

- Header: The first line summarizes what the commit is.
- Body: Use after a blank line when the change needs context, implementation notes, or verification details.
- Footer: Use git trailer-style metadata such as `Refs: #123`, `Closes: #123`, or `Fixes: #123`.
- Each commit should map to one completed Subtask whenever possible.
- Allowed types include `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, and `build`.
- `feat` maps to a Semantic Versioning MINOR change.
- `fix` maps to a Semantic Versioning PATCH change.
- Optional scope identifies the module or location, such as `feat(auth):`.
- Description must not start with an uppercase letter and must not end with a period.
- Breaking changes must be marked with `!`, such as `feat!:` or `feat(api)!:`, or with a `BREAKING CHANGE:` footer.

Commit operation guidelines:

- There is no dedicated Git Agent in this project.
- Main Codex owns Git operations that affect repository history or remote state, including staging, commit, pull, push, branch switching, merge, rebase, and pull request creation.
- Role subagents may report changed files, suggest commit messages, or review commit readiness, but they must not run history-changing or remote-changing Git commands unless the user explicitly authorizes it and Main Codex delegates it.
- Implementation Agent must not commit or push its own changes.
- Review Agent must not commit or push reviewed changes.
- Commit only after the current Task/Subtask is implemented, locally verified, and ready to hand off or archive.
- Before staging, run `git status --short` and review every changed, staged, untracked, and deleted file.
- Run `git diff --check` or equivalent validation when available.
- Verify that `.env`, `.env.local`, credential files, local databases, generated secrets, and personal machine files are not staged.
- Prefer explicit path staging such as `git add path/to/file`.
- Do not use broad staging such as `git add .` unless every changed file has been reviewed and is intended.
- Do not stage unrelated user changes.
- Do not stage generated artifacts unless intentionally part of the Task.
- If verification could not run, mention the reason in the commit body or handoff report.
- If the Task is blocked, prefer a handoff note or run log over a WIP commit unless the user explicitly asks for a WIP commit.
- Before pushing, confirm clean status or only intentionally uncommitted unrelated user changes, and confirm target branch and remote.

Do not commit when:

- Real secrets or environment files are staged.
- Unrelated files are included.
- Tests or checks are failing and unexplained.
- Implementation scope is ambiguous.
- The user explicitly asked not to commit.

Examples:

```md
feat(auth): add session refresh flow

세션 만료 시 refresh token으로 로그인 상태를 갱신하는 흐름을 추가합니다.
검증: auth API test와 세션 만료 수동 시나리오를 확인했습니다.

Refs: #42
```

```md
fix(api): handle missing project id
docs(agents): document folder-level inheritance
refactor(tasks): split handover template generation
test(auth): add expired token coverage
feat(api)!: change project response format

BREAKING CHANGE: project responses now wrap data in a result object
```

## Core Agent Roles

The project uses four core roles:

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

Domain and focus labels do not create new root roles. They only narrow scope, required context, and output expectations.

## Agent Creation Semantics

When the user says "create a Review Agent", "create a Spec Agent", or similar, Main Codex must first treat it as a request to create a real tool-backed subagent when a supported subagent harness is available.

Agent creation can mean:

1. Tool-Backed Role Subagent Creation
   - Main Codex creates or delegates to a separate subagent through the available subagent harness.
   - Use this by default when the user asks to create, launch, spawn, delegate to, or run Spec Agent, Task Agent, Implementation Agent, or Review Agent.
   - Assign exactly one role, one bounded Task or Subtask, the required context, and the required output format.
   - Do not claim a separate agent was created unless the tool or harness actually created one.

2. Role Activation Fallback
   - The current agent adopts the requested role.
   - No new file, process, or independent agent is created.
   - Use only when no supported subagent harness is available, when the user explicitly asks the current Codex session to act as the role, or when the user approves fallback.

3. Folder-Level `AGENTS.md` Creation
   - A local `AGENTS.md` file is created inside a specific folder.
   - Use only when the user provides a folder path or asks to create folder-level instructions.
   - This is not subagent creation.

If subagent creation is requested but unavailable, report that real subagent creation is unavailable and ask whether to continue with Role Activation Fallback.

## Agent Naming Convention

Display name format:

```md
[Domain] [Focus] [Core Role]
```

Core roles:

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

Allowed domain labels:

- General: Shared utilities, docs, scripts, configuration-adjacent work, or unclear ownership.
- Frontend: React, TailwindCSS, routes, components, hooks, client state, accessibility, and browser-facing behavior.
- Backend: Django, APIs, models, migrations, serializers/forms, auth, permissions, validation, and data integrity.
- Full-stack: User flows that tightly involve both frontend and backend behavior.

Allowed focus labels:

- Code: Code quality, structure, maintainability, and local conventions.
- QA: User flows, acceptance criteria, success/error/empty states, regression risk, and test coverage.
- Security: Authentication, authorization, secrets, input validation, injection, XSS, file access, external APIs, dependencies, and workspace safety.
- UX: Usability, accessibility, copy, form behavior, responsive behavior, and user-facing error states.
- Performance: Rendering, queries, bundle size, API calls, memory, and costly operations.
- Crawl: User-approved URL and column extraction work.

Examples:

- Frontend Spec Agent
- Backend Task Agent
- Frontend Implementation Agent
- Backend Implementation Agent
- QA Review Agent
- Frontend QA Review Agent
- Backend Security Review Agent
- Full-stack QA Review Agent
- Crawl Implementation Agent

Interpret examples:

- Frontend QA Review Agent = Core Role: Review Agent; Domain: Frontend; Focus: QA.
- Backend Security Review Agent = Core Role: Review Agent; Domain: Backend; Focus: Security.
- Crawl Implementation Agent = Core Role: Implementation Agent; Focus: Crawl.

## Agent Creation Request Inputs

Before creating a role subagent, Main Codex must check whether the request includes enough information to assign a bounded task safely.

Common inputs:

- Display Name.
- Role.
- Domain Focus.
- Work Focus.
- Execution Mode.
- Goal.
- Source of Truth: approved Spec, Task, Subtask, issue, PR, diff, branch, or changed files.
- Scope: files, folders, modules, or behavior the subagent may read or modify.
- Out of Scope.
- Required Context.
- Output Format.
- Verification.
- Stop Condition.

Role-specific minimum inputs:

- Spec Agent: Goal or feature idea, target users or actors when not obvious, known constraints, expected user flow when available.
- Task Agent: Approved Spec path or approved Spec content, desired Task granularity when default is not acceptable, dependencies, next Task number when workflow requires it.
- Implementation Agent: Task or Subtask ID, Source of Truth, allowed write scope, acceptance criteria, verification command or permission to infer it from project scripts.
- Review Agent: Review target such as changed files, branch, PR, or diff; Source of Truth; review focus such as correctness, security, QA, UX, performance, or all.
- Crawl Focus: URLs, columns, output format, output path, allowed tools, verification, stop condition.

Missing input handling:

1. Infer safely from existing context when the missing value is obvious.
2. If inference is used, state the inferred value before creating the subagent.
3. If safe inference is not possible, ask the user only for missing required information.
4. Ask at most three questions at once.
5. Do not ask for optional fields unless they materially affect safety, scope, or output quality.

## Role Permission Matrix

Use this permission matrix unless the user explicitly grants a narrower or broader authority for a specific run.

| Role | May Do | Must Not Do |
| --- | --- | --- |
| Main Codex | Interpret user intent, create subagents, assign scope, integrate results, request clarification, run final Git operations when requested | Hide ambiguity, bypass root rules, let subagents mutate overlapping scopes without coordination |
| Spec Agent | Write or update Specs, requirements, designs, acceptance criteria, risks, and planning context | Modify implementation code, run Git history or remote operations, continue into Task breakdown without approval |
| Task Agent | Split approved Specs into Tasks/Subtasks, define order, scope, acceptance criteria, verification, and handoff packets | Modify implementation code, run Git history or remote operations, create vague or over-broad Subtasks |
| Implementation Agent | Modify files only inside the approved write scope, run scoped verification, report changed files and blockers | Modify out-of-scope files, commit/push/pull, move to the next Subtask without review and confirmation |
| Review Agent | Review changed files, report findings, verify readiness, suggest fixes or commit messages | Modify implementation files by default, commit/push/pull, approve work with unresolved Blocker findings |

Review Agent is read-only by default. If the user wants a Review Agent to edit review documentation, that write scope must be explicitly stated.

## Agent Invocation Contract

Every tool-backed subagent run should be described with this contract before spawning whenever the information is available:

```md
- Display Name:
- Core Role:
- Domain Focus:
- Work Focus:
- Execution Mode:
- Goal:
- Source of Truth:
- Scope:
- Out of Scope:
- Required Context:
- Output Format:
- Verification:
- Stop Condition:
```

Rules:

- Do not create an Implementation Agent without a bounded write scope.
- Do not create a Review Agent without a review target.
- Do not create a Crawl-focused agent without approved URLs and columns.
- State inferred contract values before spawning the subagent.
- If Execution Mode is not specified, use Hybrid Mode for ordinary feature work and Sequential Mode for security-sensitive, database, authentication, authorization, payment, migration, irreversible, or ambiguous work.
- Use Parallel Mode only when the user explicitly asks for parallel agents or when write scopes are clearly separated and Main Codex can integrate the results safely.
- If safety-critical fields are missing, ask up to three questions instead of spawning.

## Subagent Output Contract

Every subagent final report must be concise and include enough information for Main Codex to integrate or hand off the result.

Common output fields:

```md
- Agent Name:
- Task/Subtask:
- Scope:
- Changed Files:
- Commands Run:
- Verification Result:
- Blockers:
- Assumptions:
- Next Recommended Action:
```

Role-specific output requirements:

- Spec Agent: include Spec path or draft content, unresolved questions, assumptions, and approval needs.
- Task Agent: include Task/Subtask list, execution order, dependencies, acceptance criteria, and verification commands.
- Implementation Agent: include changed files, implementation summary, verification results, blockers, and known limitations.
- Review Agent: use the required Review Output Format with Severity, Area, Evidence, Risk, Required Fix, and Retest.
- Security Review Agent: use the required Security Review Output Format when security-sensitive areas are involved.
- Crawl-focused agents: include input URLs, approved columns, output path, row count or sample result, failures, `source_url`, `retrieved_at`, and `failure_reason` handling.

If a subagent cannot complete its task, it must return a blocker summary instead of continuing silently.

## Parallel Subagent Safety

Parallel subagents are allowed only when their responsibilities are independent.

Rules:

- Implementation Agents must have explicit write scopes.
- Parallel Implementation Agents must not share overlapping write scopes.
- Review Agents are read-only by default unless the user explicitly asks them to edit review documentation.
- If two subagents need to touch the same files, run them sequentially.
- Main Codex must integrate or reconcile subagent results before reporting completion.
- Do not let multiple subagents repeatedly fix the same failing area without a handoff summary and user-visible escalation.

## Agent Run Log

For substantial or multi-agent work, Main Codex should create or update an agent run log under `docs/reports/agent-runs/`.

Suggested filename:

```md
docs/reports/agent-runs/RUN_[YYYYMMDD]_[short-task-name].md
```

Each run log should include:

- Run ID.
- Timestamp.
- Agent Name.
- Core Role / Domain Focus / Work Focus.
- Source of Truth.
- Scope and Out of Scope.
- Commands run.
- Changed files.
- Result.
- Blockers.
- Follow-up or handoff notes.

Use `docs/reports/agent-runs/RUN_TEMPLATE.md` when available.

Run log is required when:

- Two or more subagents are used for the same user request.
- Any subagents run in parallel.
- Security Review Agent is used.
- Crawl Focus is used.
- Fix & Re-review repeats two or more times.
- Work spans multiple sessions or needs handoff.
- The user explicitly asks for traceability.

## Execution Mode Rule

Before starting complex work, choose exactly one execution mode.

- Sequential Mode: safest and fully ordered.
- Hybrid Mode: default for ordinary feature work.
- Parallel Mode: fastest but highest coordination risk.

Standalone MAX mode files:

- `MAX/modes/sequential.md`
- `MAX/modes/hybrid.md`
- `MAX/modes/parallel.md`

If the user does not specify a mode, use Hybrid Mode for ordinary feature work.

Use Sequential Mode for security-sensitive, database, authentication, authorization, payment, migration, irreversible, or ambiguous work.

Use Parallel Mode only when the user explicitly asks for parallel agents or when write scopes are clearly separated and Main Codex can integrate the results safely.

Do not load all mode files by default in the token-optimized rule set. MAX users may keep this full section available because MAX is intended for full-context usage.

### Sequential Mode

Use Sequential Mode when safety, clarity, or user review is more important than speed.

Rules:

- Run one role at a time.
- Run one Task or Subtask at a time.
- Do not run parallel Implementation Agents.
- Start Review Agent only after Implementation Agent finishes the bounded Task/Subtask and reports verification.
- Move to the next Task/Subtask only after review, approval, and required user confirmation.

Required sequence:

1. Spec Agent creates or updates the Spec.
2. Spec is reviewed for scope, clarity, missing requirements, and contradictions.
3. Task Agent breaks the approved Spec into Tasks and Atomic Subtasks.
4. Implementation Agent implements exactly one approved Task/Subtask.
5. Implementation Agent runs defined local verification.
6. Review Agent reviews completed work.
7. Implementation Agent fixes findings when required.
8. Review Agent re-reviews the fix.
9. Main Codex reports completion and waits for approval before moving forward.

### Hybrid Mode

Use Hybrid Mode as the default operating mode for ordinary feature work.

Rules:

- Spec Workflow is always sequential.
- Task Breakdown Workflow is always sequential.
- Implementation may run in parallel only when each Implementation Agent has a clearly separated write scope.
- Review may run in parallel when reviewers are read-only or write only to explicitly approved review documentation.
- Main Codex owns coordination, conflict prevention, result integration, user communication, and requested Git operations.
- If two agents need to touch the same file, path, migration, API contract, data model, or shared component, run those agents sequentially.

Before parallel work, Main Codex must define agent name, Task/Subtask, owned files or directories, forbidden files or directories, shared contracts, verification command, and expected output.

### Parallel Mode

Use Parallel Mode only when the user explicitly asks for parallel agents or Main Codex can prove the work is independently scoped.

Required preconditions:

- Clear Source of Truth.
- Written Task/Subtask breakdown.
- Scope ownership table.
- Non-overlapping write scopes.
- Explicit out-of-scope boundaries.
- Verification commands for each agent.
- Stop conditions for each agent.
- Final integration and review step owned by Main Codex.

Scope ownership table:

| Agent | Role | Task/Subtask | Write Scope | Read Scope | Forbidden Scope | Verification | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |

Rules:

- Every writeable file or directory may have only one owner.
- Review agents are read-only by default.
- Parallel agents must not modify overlapping files, directories, migrations, contracts, or generated outputs.
- Main Codex must wait for all required parallel outputs before reporting completion.
- Main Codex must reconcile conflicts, summarize tradeoffs, run final verification, and request integrated review when implementation changed files.

Stop and escalate when scopes overlap, shared contracts change without one owner, two agents produce incompatible results, verification fails three consecutive times, or final integration cannot be reviewed safely.

## End-to-End Workflow

The sequence below is the canonical lifecycle. The selected execution mode defines whether parts of this lifecycle run strictly sequentially, in a sequential-parallel hybrid, or in parallel with a final integration gate.

All feature work must follow this sequence:

```md
Spec
-> Feature Task
-> Subtask
-> Implementation Step
-> Review
-> Fix
-> Re-review
-> Approval
```

Required sequence:

1. Create or update the Spec before implementation.
2. Review the Spec for scope, clarity, missing requirements, and contradictions.
3. Convert the approved Spec into feature-level Tasks.
4. Split large feature Tasks into smaller Subtasks.
5. Implement one Task or Subtask at a time.
6. Run relevant local verification for the completed Task or Subtask.
7. Review the completed Task or Subtask against the Spec, Task, user intent, and project rules.
8. If review finds issues, revise and repeat review.
9. Mark complete only after review approval and required verification.
10. Move to the next Task/Subtask only after approval or user confirmation.

## Spec Workflow

Spec Agent prepares Kiro-style planning material before implementation starts.

Spec Agent must:

1. Define goals and non-goals.
2. Identify users or actors.
3. Write user stories and expected behavior.
4. Write acceptance criteria.
5. Capture constraints, edge cases, security, privacy, and accessibility concerns.
6. Summarize existing system context.
7. Propose the chosen approach.
8. Identify affected files, folders, modules, APIs, data models, or UI flows.
9. Define error handling, compatibility, migration, and testing strategy.
10. Identify feature boundaries, dependencies, risks, assumptions, and verification needs.
11. Keep the Spec understandable enough for user review.
12. Do not write implementation code.

Recommended Spec sections:

- Summary.
- Goals.
- Non-Goals.
- User Flow.
- Requirements.
- Acceptance Criteria.
- Constraints.
- Risks.
- Task Breakdown.
- Verification.

## Task Breakdown Workflow

Task Agent breaks the approved Spec into work that can be implemented and reviewed safely.

Task Agent must:

1. Read the approved Spec before creating Tasks.
2. Split the Spec into feature-level Tasks.
3. Prioritize Tasks by user value, dependency order, security/correctness risk, and reviewability.
4. Split large Tasks into Atomic Subtasks.
5. Define purpose, scope, dependencies, target files, local rules, acceptance criteria, and verification commands for each Subtask.
6. Avoid mixing UI, API, database, and test changes unless tightly coupled.
7. Confirm every Task/Subtask stays inside the workspace boundary.
8. Stop and ask if boundary, priority, or dependency order is unclear.

Task/Subtask format:

```md
### Task: [short English or Korean title]

- Purpose: 이 작업이 필요한 이유를 한글로 설명합니다.
- Scope: 이 작업에서 수정할 범위와 제외할 범위를 한글로 설명합니다.
- Dependencies: 먼저 완료되어야 하는 작업을 적습니다.
- Context Budget: 반드시 읽을 문서, 읽지 말아야 할 문서, 조건부로 읽을 문서를 적습니다.
- Acceptance Criteria: 완료로 판단할 수 있는 기준을 한글로 구체적으로 적습니다.
- Verification: 실행할 테스트, 빌드, 린트, 수동 확인 방법을 적습니다.
```

Implementation-ready Subtasks should include:

- Required Context.
- Context Budget.
- Source of Truth.
- Required Sections.
- Must Read Before Implementation.
- Target Files.
- Out of Scope.
- Acceptance Criteria.
- Verification.

## Implementation Workflow

Implementation Agent implements one approved Task or Subtask at a time.

Implementation Agent must:

1. Summarize the active Task/Subtask before editing files.
2. Follow the approved Spec, Task, and Subtask instructions.
3. Follow existing project structure and coding patterns.
4. Keep changes scoped to the current Task/Subtask.
5. Avoid unrelated refactors.
6. Run verification commands/checks defined for the Task/Subtask.
7. Report changed files, implementation decisions, verification results, and known limitations before review.
8. Stop if Task/Subtask, referenced Spec sections, or acceptance criteria conflict.

Do not move to the next Subtask without review, verification, and required user confirmation.

## Review Workflow

Review Agent validates completed work before the next Task/Subtask starts.

Before Review Agent starts, Implementation Agent must provide:

- Approved Spec reference.
- Current Task/Subtask description.
- Acceptance criteria.
- Changed files.
- Summary of implementation decisions.
- Tests/checks run.
- Known limitations or assumptions.
- Areas that may affect security, data, authentication, permissions, files, dependencies, or external APIs.

Review Agent must check:

- Spec alignment.
- User intent alignment.
- Acceptance criteria.
- Unrelated behavior changes.
- Existing structure and conventions.
- Correctness.
- Edge cases.
- Failure paths.
- Missing tests.
- Maintainability.
- Accessibility when relevant.
- Performance when relevant.
- Security-sensitive changes.
- Workspace safety.

Review output format:

```md
- Severity: Blocker | Major | Minor | Approved
- Area: [review area]
- Evidence: 문제가 확인된 파일, 위치, 동작을 한글로 구체적으로 설명합니다.
- Risk: 이 문제가 실제로 어떤 장애, 보안 문제, 유지보수 문제로 이어질 수 있는지 설명합니다.
- Required Fix: 승인 전에 필요한 수정 사항을 구체적으로 적습니다.
- Retest: 수정 후 어떻게 다시 검증해야 하는지 적습니다.
```

Review Area values:

- Spec Alignment
- User Intent Alignment
- Correctness
- Edge Case
- Test Coverage
- Maintainability
- Performance
- Accessibility
- Security
- Workspace Safety
- Dependency

Severity values:

- Blocker: Must be fixed before completion.
- Major: Should be fixed unless there is a clear reason not to.
- Minor: Does not block completion but should improve clarity, consistency, or maintainability.
- Approved: No blocking issue remains.

## QA Review Agent

QA Review Agent = Review Agent + QA Focus.

QA Review Agents must check:

- User flows against the approved Spec and acceptance criteria.
- Success, error, empty, loading, permission, and edge states.
- Regression risk.
- Missing or weak test coverage.
- Frontend accessibility, responsive behavior, form UX, and client-side error handling when relevant.
- Backend API validation, error responses, permission behavior, and data integrity when relevant.

## Review Gate Policy

After implementation, use review gates appropriate to risk:

- Code Review Agent: Use for non-trivial code changes.
- QA Review Agent: Use for user-visible flows, acceptance criteria, UI/API behavior, data output, or regression-sensitive changes.
- Security Review Agent: Use when the Task touches authentication, authorization, user input, file access, external APIs, dependencies, configuration, data storage, logging, crawl behavior, or workspace operations.

All review gates do not have to run for every tiny documentation change. Main Codex should choose the smallest review set that still protects correctness, security, and user intent.

## Security Review Checklist

Run this checklist when a Task touches authentication, authorization, user input, files, external APIs, dependencies, configuration, data storage, logging, or workspace operations.

### Secrets / Credentials

Check for:

- Hardcoded API keys, tokens, passwords, private keys, or credentials.
- Real secrets in `.env`, config files, logs, fixtures, test data, or documentation.
- Unprotected `.env` files missing from `.gitignore`.
- Server-only secrets exposed to client-side code.
- Confusion between example values and real credentials.

### Authentication

Check for:

- Missing login, session, or token validation.
- Unsafe handling of expired, forged, missing, or malformed tokens.
- Authentication errors that reveal internal information.
- Passwords, tokens, or session values written to logs.

### Authorization / Access Control

Check for:

- Confusion between "is logged in" and "has access to this resource".
- Missing ownership or membership checks.
- Admin-only behavior available to normal users.
- Authorization enforced only in the frontend.
- Object ID changes that allow access to another user's data.

### Input Validation

Check for:

- Unvalidated body, query, params, headers, forms, files, or external API inputs.
- Missing type, length, format, enum, and range checks.
- Unsafe handling of empty, very long, malformed, or special-character values.
- Trusting client-side validation without server-side validation.

### Injection

Check for:

- SQL, NoSQL, LDAP, or ORM queries built through unsafe string concatenation.
- Shell commands that include user-controlled input.
- Dynamic code execution such as `eval`, unsafe templates, or untrusted dynamic imports.
- Regex, template, or script generation from untrusted input.

### XSS / Client-Side Safety

Check for:

- Rendering user input as raw HTML.
- Unsafe `dangerouslySetInnerHTML` or equivalent APIs.
- Markdown, rich text, iframe, script, or URL rendering without sanitization.
- Error messages, toast messages, or previews displaying raw user input unsafely.

### Session / Cookie / CSRF / CORS

Check for:

- Missing `HttpOnly`, `Secure`, or `SameSite` cookie protections where needed.
- State-changing requests that need CSRF protection.
- Overly broad CORS configuration.
- Weakened session expiration, refresh, or rotation behavior.

### Sensitive Data Exposure

Check for:

- Personal data, payment data, internal IDs, tokens, or private metadata returned unnecessarily.
- Sensitive data in logs, errors, analytics, monitoring, or client-side state.
- Sensitive values stored in `localStorage` or `sessionStorage` without a clear reason.
- Stack traces, database details, internal paths, or service metadata exposed to users.

### File Handling

Check for:

- Missing file size, type, extension, or MIME validation.
- File paths built from user-controlled input.
- Path traversal through `../`, absolute paths, symlinks, or encoded path segments.
- Executable or user-uploaded files stored in public locations without protection.
- Download endpoints without authorization checks.

### External API / Network

Check for:

- SSRF risks from user-controlled URLs.
- Missing webhook signature verification.
- Missing timeout, retry limit, or failure handling.
- External API errors exposing internal state or secrets.
- Costly external calls without limits when abuse is possible.

### Dependency / Supply Chain

Check for:

- New dependencies that are unnecessary or too broad.
- Unmaintained, unknown, or suspicious packages.
- Unexpected lockfile changes.
- Packages with risky install scripts, native binaries, or unclear provenance.
- Dependency changes increasing client bundle exposure of sensitive code.

### Abuse / Rate Limit

Check for:

- Login, signup, password reset, search, upload, email, payment, or AI calls without abuse protection where relevant.
- Requests that trigger excessive database work, loops, memory use, or external API cost.
- Missing pagination, size limits, or throttling for expensive operations.

### Workspace Safety

Check for:

- Reads or writes outside the workspace.
- Use of `../`, absolute paths, home directory paths, or parent project paths.
- Commands affecting global dependencies, global config, OS settings, or unrelated repositories.
- Tasks requiring outside-workspace access without explicit user approval.
- Changed files outside the approved Task/Subtask.

Security findings format:

```md
- Severity: Blocker | Major | Minor | Approved
- Area: Secrets | Authentication | Access Control | Input Validation | Injection | XSS | Session | Sensitive Data | File Handling | External API | Dependency | Rate Limit | Workspace Safety
- Evidence: 문제가 확인된 파일, 위치, 입력값, 코드 흐름을 한글로 구체적으로 설명합니다.
- Risk: 공격자나 잘못된 사용자가 이 문제를 어떻게 악용할 수 있는지 설명합니다.
- Required Fix: 승인 전에 필요한 보안 수정 사항을 구체적으로 적습니다.
- Retest: 수정 후 어떤 요청, 테스트, 시나리오로 다시 확인해야 하는지 적습니다.
```

Blocker security issues include:

- Hardcoded real secrets.
- Authentication or authorization bypass.
- User data exposure.
- Injection vulnerability.
- Unsafe file access outside the workspace.
- Unapproved destructive operation.
- Dependency change with clear security risk.

## Crawl Focus Rules

Crawl is a Work Focus, not a fifth core role.

Examples:

- Crawl Implementation Agent = Implementation Agent + Crawl Focus.
- Crawl QA Review Agent = Review Agent + Crawl Focus + QA.
- Crawl Security Review Agent = Review Agent + Crawl Focus + Security.

Crawl Tasks require:

- URLs.
- Columns.
- Output Format.
- Output Path.
- Allowed Tools.
- Verification.
- Stop Condition.

Crawl rules:

- Use Python 3.12.
- Prefer BeautifulSoup for static HTML.
- Use Selenium only when rendering or interaction is required.
- Use Scrapling only when extraction helper is useful.
- Crawl only user-provided or Task-approved URLs.
- Extract only user-specified or Task-approved columns.
- Do not invent additional columns.
- Respect robots.txt, terms, rate limits, copyright, and privacy.
- Record `source_url`, `retrieved_at`, and `failure_reason` when applicable.

## Folder-Level AGENTS.md Rules

Use additional `AGENTS.md` files only for folders with a clear feature, module, domain, or responsibility.

Inheritance Principle:

- Folder-level files must cover only specialized local rules.
- Folder-level rules must not weaken, bypass, or disable root-level rules.
- If a folder-level rule conflicts with root rules, root rules win.

Execution Path Standard:

- Agents should run from the project root by default.
- If an agent changes into a subfolder for local commands, it must still follow root security and Workspace Boundary rules.

Folder-level files should include:

- Folder purpose.
- Ownership scope.
- Local rules.
- Allowed changes.
- Forbidden changes.
- Local verification.
- Primary agent roles.
- Handover notes.

Do not create a folder-level `AGENTS.md` only because a folder exists. Create one only when stable local rules reduce ambiguity.

### General Folder Template

```md
# AGENTS.md

This file defines local agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, or Workspace Boundary rules.

## Folder Purpose

- Describe the domain, feature, or module owned by this folder.

## Ownership Scope

- Owned files:
- Related files outside this folder:
- Explicitly out of scope:

## Local Rules

- Add folder-specific architecture, naming, dependency, or design rules.
- Do not repeat root-level rules unless a short reminder prevents misuse.

## Allowed Changes

- List changes agents may make in this folder.

## Forbidden Changes

- List folder-specific changes agents must not make.
- Do not weaken root-level forbidden actions.

## Local Verification

- List tests, checks, or manual verification required for this folder.

## Primary Agent Roles

- Primary:
- Review:
- Security-sensitive areas:

## Handover Notes

- Note local assumptions, known risks, or follow-up requirements for the next agent.
```

### Frontend React + Tailwind Template

Use for `frontend/AGENTS.md` or frontend feature-level files.

Frontend local rules:

- Prioritize React component structure, user-facing behavior, UI state, accessibility, API integration, and TailwindCSS consistency.
- Framework: React.
- Styling: TailwindCSS.
- Language: Use the project's existing JavaScript or TypeScript choice.
- Package Manager: Detect from lockfile before running commands.
- Follow existing React component patterns.
- Prefer small, focused components with clear props.
- Keep UI state local unless shared state is clearly required.
- Handle loading, error, empty, and success states.
- Treat client-side validation as UX support only; backend validation remains required.
- Do not expose server-only environment variables or secrets to client-side code.
- Use Tailwind utility classes consistently with existing design tokens and layout patterns.
- Avoid introducing a component library, state library, or styling framework unless approved.
- Preserve accessibility with semantic HTML, labels, focus states, keyboard navigation, and readable error text.

Frontend verification:

- Use project-defined frontend commands when available.
- If commands are unknown, inspect package scripts first.
- Suggested checks: frontend lint, unit/component tests, build, manual UI state and accessibility check.

Frontend security-sensitive areas:

- Client environment variables.
- Auth UI.
- Token handling.
- Forms.
- Redirects.
- User-generated content.

### Backend Django Template

Use for `backend/AGENTS.md` or Django app/module-level files.

Backend local rules:

- Prioritize Django app boundaries, API contracts, validation, authentication, authorization, data integrity, error handling, observability, and server-side security.
- Framework: Django.
- API Layer: Use the project's existing Django API pattern, such as Django REST Framework if already present.
- Database: Use the configured project database.
- Package Manager: Detect from project files before running commands.
- Follow Django app boundaries and existing project structure.
- Keep business logic out of views when it grows; prefer services, selectors, forms, serializers, managers, or existing local patterns.
- Validate all user input server-side.
- Enforce authentication and authorization server-side.
- Never log passwords, tokens, API keys, secrets, or sensitive user data.
- Use Django migrations for model changes and review migrations before applying them.
- Use Django settings and environment variables safely; never hardcode secrets.
- Use Django's built-in password hashing and security mechanisms.
- Consider rate limiting or abuse protection for auth-sensitive or costly endpoints.
- Return consistent error responses without leaking stack traces or internal details.

Backend verification:

- Use project-defined backend commands when available.
- If commands are unknown, inspect project scripts or Django management configuration first.
- Suggested checks: backend lint, Django system checks, migrations check, unit/API tests, manual security checks for auth, permissions, and validation.

Backend security-sensitive areas:

- Settings.
- Environment variables.
- Authentication.
- Authorization.
- Permissions.
- Password handling.
- Tokens.
- Sessions.
- Migrations.
- File access.
- External APIs.

## Task Completion & Handover

When a top-level Task is completed, do not continue to the next Task on your own.

Before moving forward, create:

- User report: `docs/reports/TASK[number]_COMPLETION.md`
- Next-agent instruction sheet: `docs/specs/TASK[next-number]_SUBTASKS.md`

User report must include:

- Completion timestamp.
- Responsible agent.
- Spec Alignment checklist.
- Changed files and implementation summary.
- Test and verification results, including lint, unit tests, or clear reason when not applicable.
- Items requiring user confirmation.

Next-agent instruction sheet must include:

- Context and dependencies, including previous Task report and base branch.
- Atomic Subtasks in execution order.
- For each Subtask: purpose, target files, local rules, acceptance criteria, and verification commands.
- Deadlock escape conditions: stop and escalate after three consecutive test failures or repeated review deadlock.

After creating these artifacts, stop and wait for user review or approval.

## Task Startup

Before starting a new top-level Task:

1. Read `docs/specs/TASK[number]_SUBTASKS.md`.
2. Summarize the first Subtask's purpose and target files to the user.
3. Start from the first listed Subtask and proceed in order.
4. After each Subtask is implemented and locally verified, stop, report verification results, and request user confirmation.
5. If tests fail three consecutive times, direction becomes ambiguous, or review enters repeated deadlock, stop and ask for guidance.

## Completion Rules

A Task or Subtask is complete only when:

- Implementation matches the approved Spec.
- Acceptance criteria are satisfied.
- Review Agent reports no Blocker findings.
- Security review has been completed when relevant.
- Relevant tests, checks, or manual verification have been run.
- The user can understand what changed and why.

Do not mark work complete only because code was written.
