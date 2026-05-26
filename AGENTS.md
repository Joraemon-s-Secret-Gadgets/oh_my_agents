# AGENTS.md

This file defines how agents must plan, implement, review, and secure work in this project.

For a Korean teammate-facing explanation of this file, see [AGENTS.ko.md](./AGENTS.ko.md).

## Instruction Priority

Agents must follow instructions in this order:

1. User's explicit instructions.
2. This root `AGENTS.md` for project-wide safety, security, workflow, and workspace rules.
3. The nearest folder-level `AGENTS.md` file for domain-specific local rules that do not weaken root rules.
4. General agent defaults.

When instructions conflict, the higher-priority instruction wins. Folder-level instructions may specialize local ownership and verification rules, but they must not weaken or override root-level security, workflow, or Workspace Boundary rules. If the correct action is unclear, stop and ask the user before continuing.

## Top-Level Principles

These principles apply to all agents and override role-specific instructions.

1. Work only inside the current project workspace.
2. Do not read, edit, move, delete, or format files outside the workspace.
3. Follow the approved Spec before writing implementation code.
4. Break work into small feature-level Tasks before implementation.
5. Break large feature Tasks into smaller Subtasks before implementation.
6. Implement one Task or Subtask at a time.
7. Review each completed Task or Subtask before moving to the next one.
8. If review finds issues, fix them and run review again.
9. Do not modify unrelated files or unrelated behavior.
10. Prefer existing project patterns over new abstractions.
11. Run relevant tests, checks, or verification commands before marking work complete.
12. Security, correctness, and maintainability take priority over speed.
13. **Escalation on Deadlock**: If the Fix & Re-review loop between Implementation Agent and Review Agent repeats three consecutive times, or if progress is blocked by a technical limitation, stop immediately, report the situation to the user, and request user intervention before continuing.
14. **Git Commit Convention**: Commits must be scoped by Subtask whenever possible. Every commit message must strictly follow the official Conventional Commits 1.0.0 specification and the project rules in the Git Commit Convention Details section below.
15. **Environment Variable Safety**: Never hardcode real secrets or API tokens from `.env`, `.env.local`, or other environment variable files into source code, and never commit them to Git. When environment variables are needed, share only the required structure through `.env.example` with dummy values.

## Git Commit Convention Details

Agents must follow the official Conventional Commits 1.0.0 specification when creating commits.

Official reference: https://www.conventionalcommits.org/en/v1.0.0/

Commit structure:

```md
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

Rules:

- Each commit should map to one completed Subtask whenever possible.
- The commit message must start with a `type`.
- `feat` must be used for a new feature and maps to a Semantic Versioning MINOR change.
- `fix` must be used for a bug fix and maps to a Semantic Versioning PATCH change.
- Other allowed types include `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, and `build` when they accurately describe the change.
- An optional `scope` may be added in parentheses to identify the changed module or location, such as `feat(auth):` or `fix(api):`.
- A description must follow the colon and space immediately after the type or scope.
- The description must be a concise one-line summary, must not start with an uppercase letter, and must not end with a period.
- A longer body may be added after one blank line when the change needs more context.
- Footers may be added after one blank line and must follow git trailer-style formatting.
- Breaking changes must be marked with `!` after the type or scope, such as `feat!:` or `feat(api)!:`, or with a footer that starts with `BREAKING CHANGE:`.
- `BREAKING CHANGE` must be uppercase when used as a footer token.

Examples:

```md
feat(auth): add session refresh flow
fix(api): handle missing project id
docs(agents): document folder-level inheritance
refactor(tasks): split handover template generation
test(auth): add expired token coverage
feat(api)!: change project response format

BREAKING CHANGE: project responses now wrap data in a result object
```

## Workspace Boundary

Agents may only operate inside the current project workspace.

Allowed actions inside the workspace:

- Read project files.
- Create, edit, move, or delete files required for approved Tasks.
- Run project-local commands for development, testing, formatting, and verification.
- Generate temporary, cache, or build artifacts inside the workspace.

Forbidden actions outside the workspace:

- Do not read, edit, move, delete, or format files outside the current workspace.
- Do not modify other repositories, parent directories, user home files, global config files, shell profiles, IDE settings, or OS-level settings.
- Do not use `../` paths to access unrelated projects.
- Do not install or change global dependencies unless explicitly approved by the user.
- Do not run destructive commands outside the approved Task scope.
- Do not read heavy unmanaged files: Even inside the workspace, do not read entire `.git` internals, large `.log` files, build artifacts, or data files of tens of MB or more unless the user explicitly requests it. Prefer targeted searches, metadata checks, summaries, or partial reads.
- Do not track environment files: Always verify that `.env`, `.env.local`, and other real environment files are listed in `.gitignore`, and block them from being included in `git add` or commits.

If a Task appears to require access outside the workspace, the agent must stop and ask for explicit user approval before continuing.

## File-Level Agent Instructions

Use additional `AGENTS.md` files only for folders that own a clear feature, module, domain, or responsibility.

Inheritance Principle:

- Folder-level `AGENTS.md` files must cover only specialized local rules for their domain.
- Folder-level rules must not weaken, bypass, or disable root-level rules such as security, planning workflow, review workflow, environment variable safety, or Workspace Boundary rules.
- If a folder-level rule conflicts with this root `AGENTS.md`, the root rule takes precedence.

Execution Path Standard:

- Agents should run from the project root by default.
- If an agent changes into a subfolder for local commands, it must still follow the root-level security and Workspace Boundary rules.
- Running from a subfolder must never be used to access files, commands, or dependencies outside the approved workspace boundary.

Folder-level `AGENTS.md` files should contain only local rules:

- Purpose of the folder.
- Owned files and responsibilities.
- Allowed and forbidden changes in that folder.
- Local architecture or dependency rules.
- Local test and verification rules.
- Primary agent role for that folder.

Do not duplicate root-level rules in folder-level files. Keep shared rules in this root file so the project does not drift as it grows.

### Folder-Level `AGENTS.md` Template

Use this template when creating a new folder-level `AGENTS.md`:

````md
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
````

### Frontend React + Tailwind Folder-Level `AGENTS.md` Template

Use this template when creating `frontend/AGENTS.md` or a frontend feature-level `AGENTS.md`.

````md
# AGENTS.md

This file defines local frontend agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

## Agent Focus

This folder is frontend-focused.
Agents working here must prioritize React component structure, user-facing behavior, UI state, accessibility, API integration, and TailwindCSS consistency.

## Project Stack

- Framework: React
- Styling: TailwindCSS
- Language: Use the project's existing JavaScript or TypeScript choice.
- Package Manager: Detect from lockfile before running commands.

## Folder Purpose

- Describe the frontend domain, feature, route, or UI module owned by this folder.

## Ownership Scope

- Owned files:
- Related backend/API contracts:
- Explicitly out of scope:

## Local Rules

- Follow existing React component patterns.
- Prefer small, focused components with clear props.
- Keep UI state local unless shared state is clearly required.
- Handle loading, error, empty, and success states.
- Treat client-side validation as UX support only; backend validation remains required.
- Do not expose server-only environment variables or secrets to client-side code.
- Use Tailwind utility classes consistently with existing design tokens and layout patterns.
- Avoid introducing a component library, state library, or styling framework unless explicitly approved.
- Preserve accessibility with semantic HTML, labels, focus states, keyboard navigation, and readable error text.

## Allowed Changes

- React components, hooks, client utilities, route/view files, styles, tests, and frontend documentation within this folder's scope.

## Forbidden Changes

- Do not change backend API behavior from frontend folders.
- Do not hardcode API secrets, tokens, or server-only environment variables.
- Do not bypass root security, environment, or Workspace Boundary rules.
- Do not introduce new global styling conventions without approval.

## Local Verification

- Use project-defined frontend commands when available.
- If commands are unknown, inspect package scripts before running tests.
- Suggested checks once configured:
  - frontend lint
  - frontend unit/component tests
  - frontend build
  - manual UI state and accessibility check

## Primary Agent Roles

- Primary: Implementation Agent for frontend Tasks and Subtasks.
- Review: Review Agent with frontend UX, accessibility, state, and API-integration focus.
- Security-sensitive areas: client environment variables, auth UI, token handling, forms, redirects, user-generated content.

## Handover Notes

- Document API assumptions, unverified UI states, accessibility gaps, and any required backend coordination.
````

### Backend Django Folder-Level `AGENTS.md` Template

Use this template when creating `backend/AGENTS.md` or a backend app/module-level `AGENTS.md`.

````md
# AGENTS.md

This file defines local backend agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

## Agent Focus

This folder is backend-focused.
Agents working here must prioritize Django app boundaries, API contracts, validation, authentication, authorization, data integrity, error handling, observability, and server-side security.

## Project Stack

- Framework: Django
- API Layer: Use the project's existing Django API pattern, such as Django REST Framework if already present.
- Database: Use the configured project database.
- Package Manager: Detect from project files before running commands.

## Folder Purpose

- Describe the backend domain, Django app, API area, or service module owned by this folder.

## Ownership Scope

- Owned files:
- Related frontend/API consumers:
- Explicitly out of scope:

## Local Rules

- Follow Django app boundaries and existing project structure.
- Keep business logic out of views when it grows; prefer services, selectors, forms, serializers, managers, or existing local patterns.
- Validate all user input server-side.
- Enforce authentication and authorization server-side.
- Never log passwords, tokens, API keys, secrets, or sensitive user data.
- Use Django migrations for model changes and review migrations before applying them.
- Use Django settings and environment variables safely; never hardcode secrets in settings or source code.
- Use Django's built-in password hashing and security mechanisms.
- Consider rate limiting or abuse protection for authentication-sensitive or costly endpoints.
- Return consistent error responses without leaking stack traces or internal details.

## Allowed Changes

- Django apps, models, migrations, views, serializers/forms, services, selectors, permissions, tests, and backend documentation within this folder's scope.

## Forbidden Changes

- Do not change frontend behavior from backend folders unless explicitly scoped.
- Do not bypass authentication, authorization, validation, or migration review.
- Do not commit real `.env` files, credentials, local databases, or generated secrets.
- Do not weaken root security, environment, or Workspace Boundary rules.

## Local Verification

- Use project-defined backend commands when available.
- If commands are unknown, inspect project scripts or Django management configuration before running tests.
- Suggested checks once configured:
  - backend lint
  - Django system checks
  - migrations check
  - backend unit/API tests
  - security-sensitive manual checks for auth, permissions, and validation

## Primary Agent Roles

- Primary: Implementation Agent for backend Tasks and Subtasks.
- Review: Review Agent with backend correctness, API contract, data integrity, and security focus.
- Security-sensitive areas: settings, environment variables, authentication, authorization, permissions, password handling, tokens, sessions, migrations, file access, external APIs.

## Handover Notes

- Document API contracts, migration status, auth/permission assumptions, unverified edge cases, and required frontend coordination.
````

## File Synchronization Rule

The root `AGENTS.md` file and the Korean explanation file `AGENTS.ko.md` must always describe the same current rules.

When a rule in `AGENTS.md` is added, modified, or removed, the same change must be reflected in `AGENTS.ko.md` with a corresponding Korean explanation in the same update.

## Agent Roles

The project uses four core roles.

### Spec Agent

Spec Agent prepares Kiro-style planning material before implementation starts.

Responsibilities:

1. Requirements
   - Define goals and non-goals.
   - Identify users or actors.
   - Write user stories and expected behavior.
   - Write acceptance criteria.
   - Capture constraints, edge cases, and security, privacy, or accessibility concerns.

2. Design
   - Summarize existing system context.
   - Propose the chosen approach.
   - Identify affected files, folders, modules, APIs, data models, or UI flows.
   - Define error handling, compatibility, migration, and testing strategy.

3. Task Preparation
   - Identify feature boundaries.
   - Identify dependencies, risks, assumptions, and verification needs.
   - Prepare enough detail for Task Agent to split the work into Tasks and Subtasks.
   - Keep the Spec understandable enough for the user to review and approve.
   - Do not write implementation code.

### Task Agent

Task Agent breaks the approved Spec into work that can be implemented and reviewed safely.

Responsibilities:

- Split the Spec into feature-level Tasks.
- Split large feature Tasks into smaller Subtasks.
- Define dependencies and execution order.
- Write completion criteria for each Task and Subtask.
- Ensure each unit of work is small enough to review independently.
- Confirm that every Task stays inside the workspace boundary.

### Implementation Agent

Implementation Agent implements one approved Task or Subtask at a time.

Responsibilities:

- Follow the approved Spec, Task, and Subtask instructions.
- Follow existing project structure and coding patterns.
- Keep changes scoped to the current Task or Subtask.
- Avoid unrelated refactors.
- Run relevant local checks before handing work to Review Agent.
- Report changed files, implementation decisions, checks run, and known limitations.

### Review Agent

Review Agent validates completed work before the next Task or Subtask starts.

Responsibilities:

- Check whether the implementation matches the approved Spec, Task, and Subtask.
- Check whether all acceptance criteria are satisfied.
- Check whether unrelated behavior was changed.
- Check whether code follows existing project structure and conventions.
- Check edge cases, failure paths, and missing tests.
- Check security-sensitive changes.
- Require fixes for blocking issues before approval.

## Planning Workflow

All work must follow this sequence:

1. Write or update the Spec before implementation.
2. Review the Spec for scope, clarity, missing requirements, and contradictions.
3. Break the approved Spec into feature-level Tasks.
4. Break each large feature Task into smaller Subtasks.
5. Implement one Task or Subtask at a time.
6. Review the completed Task or Subtask.
7. If review finds issues, revise the implementation and repeat review.
8. Mark the Task or Subtask complete only after review approval.
9. Move to the next Task or Subtask.

## Task Decomposition Rule

Feature work should be decomposed so the user can follow progress without needing to understand a large implementation all at once.

Use this hierarchy:

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

Guidelines:

- A Feature Task should represent one user-visible capability or one clear technical capability.
- A Subtask should be small enough to implement, explain, and review independently.
- A Subtask should have clear inputs, outputs, and completion criteria.
- A Subtask should avoid mixing UI, API, database, and test changes unless they are tightly coupled.
- If a Subtask feels hard to explain in a few sentences, split it again.
- Do not start implementation until the current Task or Subtask is clear.

## Task Completion & Handover Rule

When a top-level Task is completed, the agent must not continue to the next Task on its own.

Before moving forward, the agent must create two handover artifacts:

- User report: `docs/reports/TASK[number]_COMPLETION.md`
- Next-agent instruction sheet: `docs/specs/TASK[next-number]_SUBTASKS.md`

The user report must summarize what was completed, what changed, what was verified, and any remaining risks or decisions needed from the user.

The user report must include:

- Completion timestamp.
- Responsible agent.
- Spec Alignment checklist.
- Changed files and implementation summary.
- Test and verification results, including lint, unit tests, or a clear reason when not applicable.
- Items requiring user confirmation.

The next-agent instruction sheet must break the next Task into Subtasks with purpose, scope, dependencies, acceptance criteria, and verification steps.

The next-agent instruction sheet must include:

- Context and dependencies, including the previous Task report and the base branch.
- Atomic Subtasks in execution order.
- For each Subtask: purpose, target files, local rules, acceptance criteria, and verification commands.
- Deadlock escape conditions: stop and escalate to the user after three consecutive test failures or a repeated review deadlock.

After creating these artifacts, stop and wait for user review or approval before starting the next top-level Task.

## Task Startup Rule

Before starting a new top-level Task, the agent must read `docs/specs/TASK[number]_SUBTASKS.md` first and summarize the first Subtask's purpose and target files to the user.

Agents must start from the first listed Subtask and proceed in order.

After each Subtask is implemented and locally verified, the agent must stop, report the verification results, and request user confirmation before moving to the next Subtask.

If tests fail three consecutive times, the Subtask direction becomes ambiguous, or review enters a repeated deadlock, stop immediately and ask the user for guidance.

## Spec Format

Specs should be written clearly enough for both the user and agents to follow.

Recommended Spec sections:

- Summary: What is being built and why.
- Goals: What this work must accomplish.
- Non-Goals: What this work intentionally does not include.
- User Flow: How the user or system moves through the feature.
- Requirements: Functional requirements.
- Acceptance Criteria: Conditions that must be true for approval.
- Constraints: Technical, product, security, or workspace limits.
- Risks: Known risks and assumptions.
- Task Breakdown: Feature Tasks and Subtasks.
- Verification: Tests, checks, or manual validation required.

## Task Format

Tasks and Subtasks should use this format:

```md
### Task: [short English or Korean title]

- Purpose: 이 작업이 필요한 이유를 한글로 설명합니다.
- Scope: 이 작업에서 수정할 범위와 제외할 범위를 한글로 설명합니다.
- Dependencies: 먼저 완료되어야 하는 작업을 적습니다.
- Acceptance Criteria: 완료로 판단할 수 있는 기준을 한글로 구체적으로 적습니다.
- Verification: 실행할 테스트, 빌드, 린트, 수동 확인 방법을 적습니다.
```

## Review Input Requirements

Before Review Agent starts, Implementation Agent must provide:

- Approved Spec reference.
- Current Task or Subtask description.
- Acceptance criteria for the Task or Subtask.
- List of changed files.
- Summary of implementation decisions.
- Tests or checks that were run.
- Known limitations or assumptions.
- Areas that may affect security, data, authentication, permissions, files, dependencies, or external APIs.

## Review Output Format

Review field names and category values must be written in English.
All explanatory content after the colon must be written in Korean.

Use this format for each finding:

```md
- Severity: Blocker | Major | Minor | Approved
- Area: [review area]
- Evidence: 문제가 확인된 파일, 위치, 동작을 한글로 구체적으로 설명합니다.
- Risk: 이 문제가 실제로 어떤 장애, 보안 문제, 유지보수 문제로 이어질 수 있는지 설명합니다.
- Required Fix: 승인 전에 필요한 수정 사항을 구체적으로 적습니다.
- Retest: 수정 후 어떻게 다시 검증해야 하는지 적습니다.
```

Severity values:

- Blocker: 반드시 수정해야 하며, 수정 전에는 Task를 완료할 수 없습니다.
- Major: 수정하는 것이 원칙이며, 미수정 시 명확한 이유가 필요합니다.
- Minor: 완료를 막지는 않지만 유지보수성, 명확성, 일관성을 위해 개선하는 것이 좋습니다.
- Approved: 차단 이슈가 없고 다음 Task로 넘어갈 수 있습니다.

Review Area values:

- Spec Alignment
- Correctness
- Edge Case
- Test Coverage
- Maintainability
- Performance
- Accessibility
- Security
- Workspace Safety
- Dependency

## Security Review Checklist

Review Agent must run this checklist when a Task touches authentication, authorization, user input, files, external APIs, dependencies, configuration, data storage, logging, or workspace operations.

### Secrets / Credentials

Check for:

- Hardcoded API keys, tokens, passwords, private keys, or credentials.
- Real secrets in `.env`, config files, logs, fixtures, test data, or documentation.
- Unprotected `.env` files that are missing from `.gitignore` and could be included in agent commits.
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
- Missing ownership or membership checks for user-specific data.
- Admin-only behavior available to normal users.
- Authorization enforced only in the frontend.
- Object ID changes that allow access to another user's data.

### Input Validation

Check for:

- Unvalidated user input from body, query, params, headers, forms, files, or external APIs.
- Missing type, length, format, enum, and range checks.
- Unsafe handling of empty values, very long values, malformed JSON, or special characters.
- Trusting client-side validation without server-side validation.

### Injection

Check for:

- SQL, NoSQL, LDAP, or ORM queries built through unsafe string concatenation.
- Shell commands that include user-controlled input.
- Dynamic code execution such as `eval`, unsafe template execution, or untrusted dynamic imports.
- Regex, template, or script generation from untrusted input.

### XSS / Client-Side Safety

Check for:

- Rendering user input as raw HTML.
- Unsafe use of `dangerouslySetInnerHTML` or equivalent APIs.
- Markdown, rich text, iframe, script, or URL rendering without sanitization.
- Error messages, toast messages, or previews that display raw user input unsafely.

### Session / Cookie / CSRF / CORS

Check for:

- Missing `HttpOnly`, `Secure`, or `SameSite` cookie protections where needed.
- State-changing requests that need CSRF protection.
- Overly broad CORS configuration such as unrestricted origins.
- Changes that weaken session expiration, refresh, or rotation behavior.

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
- Download endpoints that return files without authorization checks.

### External API / Network

Check for:

- SSRF risks from user-controlled URLs.
- Missing webhook signature verification.
- Missing timeout, retry limit, or failure handling for external calls.
- External API errors that expose internal state or secrets.
- Costly external calls without limits when abuse is possible.

### Dependency / Supply Chain

Check for:

- New dependencies that are unnecessary or too broad for the Task.
- Unmaintained, unknown, or suspicious packages.
- Unexpected lockfile changes.
- Packages with risky install scripts, native binaries, or unclear provenance.
- Dependency changes that increase client bundle exposure of sensitive code.

### Abuse / Rate Limit

Check for:

- Login, signup, password reset, search, upload, email, payment, or AI calls without abuse protection where relevant.
- Requests that can trigger excessive database work, loops, memory use, or external API cost.
- Missing pagination, size limits, or throttling for expensive operations.

### Workspace Safety

Check for:

- Reads or writes outside the current workspace.
- Use of `../`, absolute paths, home directory paths, or parent project paths.
- Commands that affect global dependencies, global config, OS settings, or unrelated repositories.
- Generated Tasks that require access outside the workspace without explicit user approval.
- Changed files that are not part of the approved Task or Subtask.

## Security Review Output Format

Security findings must use English field names and English category values.
All explanation after the colon must be written in Korean.

Use this format:

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

## Completion Rules

A Task or Subtask is complete only when:

- The implementation matches the approved Spec.
- Acceptance criteria are satisfied.
- Review Agent reports no Blocker findings.
- Security review has been completed when relevant.
- Relevant tests, checks, or manual verification have been run.
- The user can understand what changed and why.

Do not mark work complete only because code was written.
