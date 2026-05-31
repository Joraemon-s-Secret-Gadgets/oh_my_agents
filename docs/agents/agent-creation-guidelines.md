## Agent Creation Guidelines

Use this guide when the user asks to create an agent, activate a role, or create a folder-level `AGENTS.md` file.

## Agent Creation Semantics

When the user says "create a Review Agent", "create a Spec Agent", or similar, Main Codex must first treat it as a request to create a real tool-backed subagent when a supported subagent harness is available.

Agent creation can mean one of three things:

1. Tool-Backed Role Subagent Creation
   - Main Codex creates or delegates to a separate subagent through the available subagent harness.
   - Use this by default when the user asks to create, launch, spawn, delegate to, or run Spec Agent, Task Agent, Implementation Agent, or Review Agent.
   - Assign exactly one role, one bounded Task or Subtask, the minimum required context, and the required output format.
   - Do not claim that a separate agent was created unless the tool or harness actually created one.

2. Role Activation Fallback
   - The current agent adopts the requested role for the current task.
   - No new file, process, or independent agent is created.
   - Use this only when no supported subagent harness is available, when the user explicitly asks the current Codex session to act as the role, or when the user approves fallback after subagent creation is unavailable.

3. Folder-Level `AGENTS.md` Creation
   - A local `AGENTS.md` file is created inside a specific folder.
   - Use this only when the user provides a folder path or asks to create folder-level instructions.
   - Use the matching template from `docs/agents/templates`.

## Default Interpretation

- "Review Agent 생성해서 리뷰해줘" means Tool-Backed Role Subagent Creation when a supported harness is available.
- "Spec Agent 생성해서 스펙 작성해줘" means Tool-Backed Role Subagent Creation when a supported harness is available.
- "Task Agent 생성해서 Task를 쪼개줘" means Tool-Backed Role Subagent Creation when a supported harness is available.
- "Implementation Agent 생성해서 Subtask 2.1 구현해줘" means Tool-Backed Role Subagent Creation when a supported harness is available.
- "현재 Codex가 Review Agent 역할로 리뷰해줘" means Role Activation Fallback by explicit user request.
- "`frontend/AGENTS.md` 생성해줘" means Folder-Level `AGENTS.md` Creation.
- "`backend/AGENTS.md` 생성해줘" means Folder-Level `AGENTS.md` Creation.
- "별도 에이전트/서브에이전트를 생성해서 맡겨줘" means Tool-Backed Role Subagent Creation only if a supported tool or harness exists.

If subagent creation is requested but unavailable, Main Codex must report that real subagent creation is unavailable in the current environment and ask whether to continue with Role Activation Fallback.

## Current Role Agents

The current project role agents are:

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

These are intended to be created as tool-backed subagents when a supported subagent harness is available. Role activation in the current Codex session is only a fallback.

## Role Agent Creation Criteria

Create or activate role agents by task phase:

- Spec Agent: Create when the requested work needs requirements, design, goals, non-goals, user flow, acceptance criteria, constraints, risks, or implementation planning before Tasks exist.
- Task Agent: Create when an approved Spec exists and the work needs feature Tasks, ordered Subtasks, dependencies, acceptance criteria, verification commands, or next-agent handoff instructions.
- Implementation Agent: Create when an approved Task or Subtask exists and the user asks to implement, modify, refactor, test, or document the scoped work.
- Review Agent: Create when completed work needs validation against the Spec, user intent, acceptance criteria, correctness, security, maintainability, tests, or workspace safety.

Role boundaries:

- Spec Agent and Task Agent must not implement code unless the user explicitly changes the role and approved scope.
- Implementation Agent must not move to the next Subtask without the required review, verification, and user confirmation rules.
- Do not treat "Frontend Agent" or "Backend Agent" as new core roles by default. Treat them as domain focus for Implementation Agent or Review Agent, or create a folder-level `AGENTS.md` only when the user provides a folder path or requests local folder instructions.
- If the requested role is unclear, state the role interpretation before acting.

## Agent Naming Convention

Core roles remain limited to:

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

Subagents may use domain and focus labels in their display names to make scope clear.

Display name format:

```md
[Domain] [Focus] [Core Role]
```

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

Examples:

- Frontend Spec Agent
- Backend Task Agent
- Frontend Implementation Agent
- Backend Implementation Agent
- QA Review Agent
- Frontend QA Review Agent
- Backend Security Review Agent
- Full-stack QA Review Agent

Domain and focus labels do not create new root roles. They only narrow the subagent's scope, required context, and output expectations.

Interpret examples:

- Frontend QA Review Agent = Core Role: Review Agent; Domain: Frontend; Focus: QA.
- Backend Security Review Agent = Core Role: Review Agent; Domain: Backend; Focus: Security.
- Frontend Implementation Agent = Core Role: Implementation Agent; Domain: Frontend; Focus: Code unless another focus is specified.

QA Review Agents must check:

- User flows against the approved Spec and acceptance criteria.
- Success, error, empty, loading, permission, and edge states.
- Regression risk and missing test coverage.
- Frontend accessibility, responsive behavior, form UX, and client-side error handling when relevant.
- Backend API validation, error responses, permission behavior, and data integrity when relevant.

## Agent Creation Request Inputs

Before creating a role subagent, Main Codex must check whether the request includes enough information to assign a bounded task safely.

Common inputs:

- Display Name: The requested subagent name, such as Frontend QA Review Agent.
- Role: Spec Agent, Task Agent, Implementation Agent, or Review Agent.
- Domain Focus: General, Frontend, Backend, or Full-stack when relevant.
- Work Focus: Code, QA, Security, UX, Performance, or another explicit focus when relevant.
- Goal: What the subagent must accomplish.
- Source of Truth: The approved Spec, Task, Subtask, issue, PR, diff, branch, or changed files the subagent must follow.
- Scope: Files, folders, modules, or behavior the subagent may read or modify.
- Out of Scope: Files, folders, modules, or behavior the subagent must not touch.
- Required Context: Specific docs or sections the subagent must read.
- Output Format: The report, Spec, Task list, patch summary, or review format expected from the subagent.
- Verification: Tests, checks, build commands, lint commands, or manual validation the subagent should run or report as not applicable.
- Stop Condition: When the subagent must stop and escalate instead of continuing.

Role-specific minimum inputs:

- Spec Agent: Goal or feature idea, target users or system actors when not obvious, known constraints, and expected user flow when available.
- Task Agent: Approved Spec path or approved Spec content, desired Task granularity when the default is not acceptable, dependencies, and next Task number when the workflow requires one.
- Implementation Agent: Task or Subtask ID, Source of Truth, allowed write scope, acceptance criteria, verification command or permission to infer one from project scripts.
- Review Agent: Review target such as changed files, branch, PR, or diff; Source of Truth; review focus such as correctness, security, UX, performance, or all.

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
- State any inferred contract values before spawning the subagent.
- If Execution Mode is not specified, use Hybrid Mode for ordinary feature work and Sequential Mode for security-sensitive, database, authentication, authorization, payment, migration, irreversible, or ambiguous work.
- Use Parallel Mode only when the user explicitly asks for parallel agents or when write scopes are clearly separated and Main Codex can integrate the results safely.
- If the contract is missing safety-critical fields, ask the user up to three questions instead of spawning.

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

## Review Gate Policy

After implementation, use review gates appropriate to risk:

- Code Review Agent: Use for non-trivial code changes.
- QA Review Agent: Use for user-visible flows, acceptance criteria, UI/API behavior, data output, or regression-sensitive changes.
- Security Review Agent: Use when the Task touches authentication, authorization, user input, file access, external APIs, dependencies, configuration, data storage, logging, crawl behavior, or workspace operations.

All review gates do not have to run for every tiny documentation change. Main Codex should choose the smallest review set that still protects correctness, security, and user intent.

## Missing Input Handling

If required input is missing, Main Codex must not create a vague or over-scoped subagent.

Use this order:

1. Infer safely from existing context when the missing value is obvious.
2. If inference is used, state the inferred value before creating the subagent.
3. If safe inference is not possible, ask the user only for the missing required information.
4. Ask at most three questions at once.
5. Do not ask for optional fields unless they materially affect safety, scope, or output quality.

Example questions:

```md
Implementation Agent를 생성하려면 범위를 안전하게 제한해야 합니다.

1. 구현할 Task/Subtask ID는 무엇인가요?
2. 수정 가능한 파일 또는 폴더 범위는 어디까지인가요?
3. 완료 후 실행해야 할 검증 명령이 있나요?
```

```md
Review Agent를 생성하려면 리뷰 대상을 확정해야 합니다.

1. 리뷰할 변경 파일, 브랜치, PR, 또는 diff는 무엇인가요?
2. 기준이 되는 Spec/Task 문서는 어디인가요?
3. 리뷰 초점은 전체 검토인가요, 보안 중심인가요?
```

## Current Folder-Level Templates

Use these templates only for folder-level `AGENTS.md` files:

- General folder: `docs/agents/templates/folder-level.md`
- Frontend React + Tailwind folder: `docs/agents/templates/frontend-react-tailwind.md`
- Backend Django folder: `docs/agents/templates/backend-django.md`

## Folder-Level Template Creation Criteria

Use the template that matches the folder's stable ownership:

- General: Use for shared utilities, common modules, documentation areas, scripts, configuration-adjacent folders, or any folder without a clear frontend/backend ownership model.
- Frontend React + Tailwind: Use for `frontend/`, React route folders, UI feature folders, component libraries, hooks, client utilities, Tailwind styling areas, and browser-facing behavior.
- Backend Django: Use for `backend/`, Django apps, API modules, models, migrations, serializers/forms, permissions, services, selectors, server-side validation, and data integrity areas.

Do not create a folder-level `AGENTS.md` only because a folder exists. Create one only when stable local rules will reduce ambiguity for future agents.

## When To Create A Folder-Level `AGENTS.md`

Create one only when:

- The folder owns a clear domain, feature, module, or responsibility.
- Local rules differ from the root `AGENTS.md`.
- The folder has special verification, security, stack, ownership, or handoff rules.
- Repeated work in that folder would benefit from stable local instructions.

Do not create one when:

- The folder is temporary.
- The folder has no clear ownership.
- The rules would only repeat root `AGENTS.md`.
- A one-time prompt is enough for the task.

## Template Selection

- Use the General template for shared utilities, docs areas, common modules, or folders without a frontend/backend-specific stack.
- Use the Frontend React + Tailwind template for `frontend/` or frontend feature folders.
- Use the Backend Django template for `backend/` or Django app/module folders.

If the correct template is unclear, ask the user before creating the file.

## Required Checks Before Creating

- Read root `AGENTS.md`.
- Read the nearest parent folder-level `AGENTS.md` if one exists.
- Confirm the folder purpose and owned files.
- Confirm local rules do not weaken root rules.
- Keep the new folder-level `AGENTS.md` short.

## What To Include

- Folder purpose.
- Ownership scope.
- Local rules.
- Allowed changes.
- Forbidden changes.
- Local verification.
- Primary agent roles.
- Handover notes.

## What Not To Include

- Do not duplicate root security rules.
- Do not copy long templates blindly.
- Do not add broad project-wide workflow rules.
- Do not add rules for unrelated folders.
- Do not include secrets, environment values, credentials, or local machine paths.

## Token Budget

- Keep folder-level `AGENTS.md` files short, preferably 20-60 lines.
- Link to root or `docs/agents` files instead of copying long shared rules.
- Do not load `AGENTS.ko.md` unless editing Korean docs, checking synchronization, or responding to a Korean explanation request.
- Do not load all templates; load only the selected template.

## Creation Output

After creating a folder-level `AGENTS.md`, report:

- Created path.
- Selected template.
- Folder purpose.
- Local rules added.
- Verification commands.
- Unresolved assumptions.
