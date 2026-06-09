# AGENTS.md

This file defines how agents must plan, implement, review, and secure work in this project.

For a Korean teammate-facing explanation of this file, see [AGENTS.ko.md](./AGENTS.ko.md).

Agents must not load `AGENTS.ko.md` by default. Load it only when the user asks for Korean explanation, when editing or synchronizing Korean documentation, or when explicitly checking file synchronization. This restriction does not override the File Synchronization Rule when agent documentation is being edited.

## Instruction Priority

Agents must follow instructions in this order:

1. User's explicit instructions.
2. This root `AGENTS.md` for project-wide safety, security, workflow, and workspace rules.
3. The nearest folder-level `AGENTS.md` file for domain-specific local rules that do not weaken root rules.
4. General agent defaults.

When instructions conflict, the higher-priority instruction wins. Folder-level instructions may specialize local ownership and verification rules, but they must not weaken or override root-level security, workflow, or Workspace Boundary rules. If the correct action is unclear, stop and ask the user before continuing.

## User Language Preservation Rule

When the user gives task instructions in Korean or another non-English language, do not discard, replace, or silently overwrite the original request.

For agent execution, preserve the original request as `User Request Original` exactly as written, then normalize the executable instructions into a structured English `Structured Agent Contract`.

The structured English contract improves agent reliability. The original user request remains authoritative for user intent, nuance, and success criteria.

Review Agent must compare completed work against both `User Request Original` and `Structured Agent Contract`.

## Project Context Rule

This `AGENTS.md` is for the Lovv project. Always load `docs/projects/lovv-project-context.md` before selecting an agent role, domain, execution mode, stack assumption, or harness route.

The user is responsible for defining the product feature, goal, user-visible behavior, exclusions, and MVP priority. Main Codex is responsible for inferring the technical route from the Lovv project context, approved Specs, Tasks, GitHub Issues, and existing project files.

Lovv default stack assumptions:

- Frontend: React + TailwindCSS.
- Backend/API: AWS SAM + AWS Lambda + Amazon API Gateway.
- Database: Amazon Aurora MySQL-Compatible on Amazon RDS.
- Backend mode: Serverless by default; do not assume EC2.
- Graph DB: Out of current scope; do not use Neo4j or another graph database unless an approved Spec explicitly adds it.
- RAG chatbot: Prefer HTTP REST and Lambda/API Gateway response streaming when streaming is required; do not assume WebSocket.
- Persistence: Persist confirmed or final itineraries only by default. Do not persist in-progress chat messages or unfinished plan drafts server-side unless an approved Spec adds durable conversation or draft state.

Do not ask the user to choose the agent role, execution mode, backend framework, or infrastructure layer when this project context makes the choice clear. If the user asks for API work, treat it as Backend AWS SAM work unless the user explicitly specifies another backend stack.

Before creating a new API contract, route, Lambda handler, or SAM implementation, Backend AWS SAM agents must check the existing API source-of-truth documents listed in `docs/projects/lovv-project-context.md`. Existing Task 9/10 API and data-loading documents define the current small-city API contract boundary and must not be contradicted unless a new approved Spec changes that contract. These documents do not prove that the listed endpoint paths are actual deployed Lovv API addresses. The current implementation is frontend-only, and the database is still under construction; agents must verify the real SAM/API Gateway deployment, stage/base URL, auth/environment configuration, and DB readiness before implementing or using live API calls.

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

## Agent Progress & Handoff Rule

Agents must keep the user informed during long-running work and must not silently stall.

- Progress Update Interval: If work continues for 4 minutes, provide a short status update that states the active role, active Task/Subtask, current action, and any early findings.
- No-Progress Limit: If there is no meaningful progress for 5 minutes, stop active work instead of continuing silently.
- Stalled Work Handover: Before stopping for no progress, write a concise handover summary with active role, active Task/Subtask, goal, files touched, commands run, what worked, what failed, current blocker, risk if continued, and recommended next action.
- Handoff Options: Ask the user whether to hand off to Main Codex, create a fresh agent with the same role, or allow one more bounded attempt.
- Main Codex Handoff: Prefer this when direction, requirements, architecture, cross-role coordination, or user intent needs clarification.
- Same-Role Fresh Agent Handoff: Prefer this when the Task/Subtask scope is clear but the current agent is repeating the same implementation, debugging, or review failure.
- No Silent Retry: Do not repeatedly retry the same failing command, test, implementation, or review loop without reporting progress and changing the approach.

## Agent Lifecycle & Cleanup Rule

Agent instances are disposable execution contexts, not permanent project assets.

- Unresponsive Agent Cleanup: If an agent does not respond or produces no meaningful progress within the No-Progress Limit, stop waiting for that agent, preserve any useful handoff summary, and terminate or delete the unresponsive agent context before starting a replacement.
- Post-Use Cleanup: After an agent completes its assigned Task, Subtask, review, or handoff, do not keep that agent active for unrelated future work. Close, archive, terminate, or delete the unused agent context unless the user explicitly asks to keep it.
- No Orphan Agents: Do not leave idle agents running with overlapping roles, stale context, or unclear ownership.
- Preserve Outputs Before Cleanup: Before deleting an agent context, preserve only the necessary final report, handoff summary, changed-file list, verification result, and blocker notes.
- Project Files Are Not Cleanup Targets: Agent cleanup applies only to agent contexts, threads, or harness-managed agent records. It must not delete project files, specs, reports, commits, branches, or user data unless the user explicitly asks for that separate action.

## Subagent Creation Contract

When the user asks to create an agent, treat that wording as a request for a real tool-backed subagent when a supported subagent harness is available.

Interpret user wording as follows:

- `Create an agent`, `agent 생성`, `에이전트 생성`, `subagent 생성`, `spawn agent`, `launch agent`, or `delegate to agent` means real tool-backed subagent creation.
- `Act as <role>`, `<role>로 동작해줘`, `역할로 동작해줘`, or `현재 Codex가 <role> 역할로 해줘` means current-session role activation, not subagent creation.
- `팀 제안해줘`, `team proposal`, or `agent team proposal` means proposal only. Do not create subagents during proposal.
- `제안 승인. 시작해줘`, `제안 승인. 순차형으로 시작해줘`, `제안 승인. 하이브리드로 시작해줘`, `agent team 실행해줘`, or `실제 subagent로 생성해줘` means proceed from an approved proposal to real tool-backed subagent creation when the required scope is clear.

Normalize Korean creation requests into English execution intent before acting:

| Korean request pattern | English execution intent |
| --- | --- |
| `에이전트 생성해줘` | `Create a real tool-backed subagent.` |
| `<Role> Agent 생성해줘` | `Create a real tool-backed <Role> Agent subagent.` |
| `<Role> Agent 생성해서 <task> 해줘` | `Create a real tool-backed <Role> Agent subagent and assign it the bounded task.` |
| `<Role>로 동작해줘` | `Act as <Role> in the current Codex session. Do not create a subagent.` |
| `팀 제안해줘` | `Prepare an agent team proposal only. Do not create subagents.` |
| `제안 승인. 시작해줘` | `Start the approved proposal by creating real tool-backed subagents when scope is sufficient.` |

When real subagent creation is requested and a supported harness is available:

- Create the subagent if the request contains enough information for a bounded run.
- Use `worker` subagents for bounded implementation or file-changing work.
- Use `explorer` subagents for read-only investigation, review, or codebase questions.
- Pass a bounded contract with role, source of truth, allowed files or scope, forbidden scope, required context, output format, verification, and stop condition.
- Do not create vague, overlapping, or open-ended subagents.
- Do not claim that a subagent was created unless the harness actually created one.

If required inputs are missing, do not silently fall back to role activation. Ask at most three concise questions about the missing source of truth, target files or scope, write permission, review target, verification command, or stop condition.

If no supported subagent harness is available, say that real subagent creation is unavailable and ask whether to continue by current-session role activation.

Task-based creation shortcut:

- If the user provides `Task`, `Agent`, `Source of Truth`, `Scope`, and a creation command such as `생성해줘`, create the subagent immediately when a supported harness is available.
- Do not ask for a second approval after a complete creation command.
- Use `worker` for file-changing implementation or documentation tasks.
- Use `explorer` for read-only review, investigation, or verification tasks.
- Distinguish project-defined names from harness runtime names: `Agent Name`, `Display Name`, and `Core Role` are set by the project contract; `Harness Nickname` is auto-assigned by the harness unless the harness exposes an explicit naming field.
- After spawning, report `Agent ID`, `Harness Nickname`, `Harness Agent Type`, `Agent Name`, and `Core Role`.
- Require the subagent final report to start with the project-defined `Agent Name`.

Initial work intake:

- If the user provides a new feature, bug, product task, GitHub Issue, or implementation goal without an approved Spec, Main Codex must create a Spec Agent when a supported subagent harness is available.
- Main Codex coordinates the workflow; it must not write the Spec itself by default.
- After Spec approval, create a Task Agent to break the Spec into Tasks and Subtasks.
- After Subtask approval, create an Implementation Agent for the active Subtask.
- After implementation, create a Review Agent for the completed work or diff.

## Context Loading & Token Budget Rule

Load only the rules, specs, and source files required for the current role and Task/Subtask.

- Always load `docs/projects/lovv-project-context.md` before choosing role/domain/mode/stack routing for this project.
- Do not load all `docs/agents` files at startup.
- Do not load `docs/prompts` files unless the current task explicitly asks for a prompt template.
- Exception: If the current task involves crawling, scraping, URL extraction, deep crawling, BeautifulSoup, Selenium, or Scrapling, treat it as Crawl Focus and load `docs/prompts/crawl-task-prompt.md` before planning, implementation, or review.
- Exception: If the current task involves frontend UI, React, TailwindCSS, browser-facing behavior, routes, components, hooks, client state, forms, accessibility, responsive behavior, or frontend API integration, treat it as Frontend domain work and load `docs/agents/frontend-agent-rules.md` before planning, implementation, or review.
- Use targeted search and section reads before opening long files.
- Treat Spec Summary documents as routing indexes, not as the source of truth.
- The Full Spec remains authoritative for requirements, acceptance criteria, API contracts, data models, security rules, and user-visible behavior.
- Implementation Agent must first read the current Subtask instruction and must not read the entire Full Spec by default.
- For detailed context-loading, Spec Summary, and Subtask context-packet rules, load `docs/agents/context-loading.md`.

## Token Management Rule

Agents must treat tokens as a shared project resource and actively reduce unnecessary context loading.

Baseline context:

- Always keep this root `AGENTS.md` available as the operating rule source.
- Always load `docs/projects/lovv-project-context.md` before routing or agent creation.
- Do not load `AGENTS.ko.md`, all `docs/agents/*`, all mode files, all Specs, all reports, all prompts, or all source files by default.

Loading order:

1. Read the user request and preserve it as `User Request Original`.
2. Read this root `AGENTS.md` and `docs/projects/lovv-project-context.md`.
3. Select exactly one execution mode and load only that mode file.
4. Load domain rules only when the active Task enters that domain.
5. Load review, security, crawl, frontend, Spec, or Task format files only when the active role or focus requires them.
6. Read current Subtask instructions before reading Full Specs.
7. Read only referenced Full Spec sections unless the Subtask is unclear or contradictory.

Subagent context budget:

- Main Codex must pass subagents only the bounded contract, source of truth paths, required sections, scope, constraints, verification commands, and stop conditions needed for that run.
- Do not pass full `AGENTS.md` companion explanations, full Specs, full reports, full logs, or unrelated source files to subagents.
- Prefer summaries, section references, changed-file lists, and targeted excerpts over large pasted context.
- If a subagent needs more context, it must request the specific missing file, section, or command output instead of loading broad directories.

Heavy-context limits:

- Do not read entire `.git` internals, large logs, build artifacts, generated bundles, screenshots, crawl outputs, local databases, or large data files unless explicitly requested.
- Use file size checks, targeted `rg`, partial reads, structured parsers, or summaries before opening large files.
- For command output, capture only the relevant failure, summary, or verification lines when full output is not needed.

## Crawl Focus Trigger Rule

Treat a task as Crawl Focus when the user asks to crawl, scrape, collect data from URLs, extract columns from pages, deep crawl, or use BeautifulSoup, Selenium, or Scrapling.

For Crawl Focus:

- Load `docs/prompts/crawl-task-prompt.md` before planning, implementation, or review.
- Do not start implementation until URLs, columns, output format, output path, allowed tools, verification, and stop condition are clear.
- Implement crawl logic as Python 3.12 files or scripts inside the workspace.
- Default crawl tools are BeautifulSoup, Selenium, and Scrapling. Do not add another crawler framework such as Scrapy or Playwright unless the user or approved Task explicitly allows it.
- Deep crawling is disabled by default. Use deep crawling only when the user or approved Task provides seed URLs, domain allowlist, max depth, max pages, rate limit, output columns, and stop condition.
- Do not invent URLs, crawl targets, or output columns.
- If any Crawl Focus input is missing, stop and ask the user instead of guessing.

## Frontend Domain Trigger Rule

Treat a task as Frontend domain work when the user asks for UI, React, TailwindCSS, browser-facing behavior, routes, components, hooks, client state, forms, accessibility, responsive behavior, or frontend API integration.

For Frontend domain work:

- Load `docs/agents/frontend-agent-rules.md` before planning, implementation, or review.
- Do not start implementation until target files or folders, UI states, API/data assumptions, verification, and out-of-scope behavior are clear.
- Frontend Implementation Agent must handle relevant loading, error, empty, success, disabled, pending, and validation states.
- Frontend QA or UX/A11y Review Agent must verify user-visible behavior, responsive behavior, accessibility, and regression risk when relevant.
- Frontend Security Review Agent is required when the task touches client environment variables, auth UI, token handling, redirects, user-generated content, external scripts, or dependency changes.
- Do not expose server-only secrets, API tokens, or private configuration to client-side code.

## Execution Mode Rule

Before starting complex work, choose exactly one execution mode and load only that mode file:

- Sequential Mode: `docs/agents/modes/sequential.md`
- Hybrid Mode: `docs/agents/modes/hybrid.md`
- Parallel Mode: `docs/agents/modes/parallel.md`

If the user does not specify a mode, use Hybrid Mode for ordinary feature work.

Use Sequential Mode for security-sensitive, database, authentication, authorization, payment, migration, irreversible, or ambiguous work.

Use Parallel Mode only when the user explicitly asks for parallel agents or when write scopes are clearly separated and Main Codex can integrate the results safely.

Do not load all mode files by default. Load another mode file only when the user asks to compare modes or switch execution mode.

## Git Commit Convention Details

Before creating commits or reviewing commit messages, load `docs/agents/commit-convention.md`.

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

When creating folder-level `AGENTS.md` files, load the matching template:

- General folder: `docs/agents/templates/folder-level.md`
- Frontend React + Tailwind folder: `docs/agents/templates/frontend-react-tailwind.md`
- Backend AWS SAM folder: `docs/agents/templates/backend-aws-sam.md`

When the user asks to create an agent, activate a role, or create a folder-level `AGENTS.md`, load `docs/agents/agent-creation-guidelines.md` and follow its creation, naming, domain, and focus criteria before acting.

## File Synchronization Rule

The root `AGENTS.md`, Korean explanation file `AGENTS.ko.md`, Lovv project context files under `docs/projects/`, PRO20x full-context file `PRO20x/AGENTS.md`, and shared `oh-my-agents` Skill must stay aligned for agent operation rules.

When a rule in `AGENTS.md` is added, modified, or removed, the same change must be reflected in `AGENTS.ko.md` with a corresponding Korean explanation in the same update.

When agent creation, naming, invocation, handoff, context-loading, or subagent orchestration rules change, also check whether `PRO20x/AGENTS.md` and `skills/oh-my-agents` need the same update.

When Lovv stack, routing, persistence, RAG, database, crawl, or infrastructure assumptions change, update `docs/projects/lovv-project-context.md` and `docs/projects/ko/lovv-project-context.md` in the same pass.

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
- Check whether the implementation satisfies the user's original request, intent, and success criteria.
- Check both the preserved `User Request Original` and the English `Structured Agent Contract` when they are provided.
- Check whether all acceptance criteria are satisfied.
- Check whether unrelated behavior was changed.
- Check whether code follows existing project structure and conventions.
- Check edge cases, failure paths, and missing tests.
- Check security-sensitive changes.
- Require fixes for blocking issues before approval.

## End-to-End Workflow

This section defines the full sequence across all roles. It is intentionally high-level; detailed Spec writing, Task breakdown, implementation, and review rules are defined in the role-specific workflow sections below.

The sequence below is the canonical lifecycle. The selected execution mode defines whether parts of this lifecycle run strictly sequentially, in a sequential-parallel hybrid, or in parallel with a final integration gate.

All work must follow this sequence:

1. Create or update the Spec before implementation.
2. Review the Spec for scope, clarity, missing requirements, and contradictions.
3. Convert the approved Spec into feature-level Tasks.
4. Split large feature Tasks into smaller Subtasks.
5. Implement one Task or Subtask at a time.
6. Run relevant local verification for the completed Task or Subtask.
7. Review the completed Task or Subtask against the Spec, Task, user intent, and project rules.
8. If review finds issues, revise the implementation and repeat review.
9. Mark the Task or Subtask complete only after review approval and required verification.
10. Move to the next Task or Subtask only after the required approval or user confirmation.

## Spec Workflow

Spec Workflow is owned by the Spec Agent. Its purpose is to make the user's intent, product behavior, constraints, and review criteria clear before implementation starts.

Spec Agent responsibilities in this workflow:

1. Gather project context from approved sources such as this file, existing specs, README files, relevant code, and user instructions.
2. Write Requirements that define goals, non-goals, users or actors, user stories, acceptance criteria, constraints, edge cases, and security, privacy, or accessibility concerns.
3. Write Design that explains existing system context, chosen approach, affected files or modules, API or UI flow changes, data model changes, error handling, compatibility, migration needs, and testing strategy.
4. Prepare Task context by identifying feature boundaries, dependencies, risks, assumptions, and verification needs.
5. Keep the Spec understandable enough for the user to review and approve.
6. Do not write implementation code during Spec Workflow.
7. If requirements change, update the Spec before Task breakdown or implementation continues.

## Task Breakdown Workflow

Task Breakdown Workflow is owned by the Task Agent. The Task Agent does not own the entire planning process; it converts an approved Spec into small, ordered, reviewable units of work.

Task Agent responsibilities in this workflow:

1. Read the approved Spec before creating Tasks.
2. Split the Spec into feature-level Tasks that each represent one user-visible capability or one clear technical capability.
3. Prioritize Tasks by user value, dependency order, security or correctness risk, and reviewability.
4. Split large feature Tasks into Atomic Subtasks that can be implemented, explained, verified, and reviewed independently.
5. For each Subtask, define purpose, scope, dependencies, target files, local rules, acceptance criteria, and verification commands.
6. Avoid mixing UI, API, database, and test changes in one Subtask unless they are tightly coupled.
7. Confirm that every Task and Subtask stays inside the workspace boundary and does not weaken root security rules.
8. Stop and ask the user if the correct Task boundary, priority, or dependency order is unclear.

## Implementation & Review Workflow

Implementation & Review Workflow is owned by the Implementation Agent and Review Agent after the current Task or Subtask has been approved for execution.

Implementation Agent responsibilities in this workflow:

1. Summarize the active Task or Subtask before editing files.
2. Implement only the approved Task or Subtask.
3. Keep changes scoped and avoid unrelated refactors.
4. Run the verification commands or checks defined for the Task or Subtask.
5. Report changed files, implementation decisions, verification results, and known limitations before review.

Review Agent responsibilities in this workflow:

1. Review the completed work against the approved Spec, Task, Subtask, preserved user request, structured agent contract, user intent, and project rules.
2. Check correctness, edge cases, test coverage, maintainability, accessibility, security, and workspace safety when relevant.
3. Require fixes for Blocker findings before approval.
4. If fixes are required, the Implementation Agent must revise the work and request re-review.
5. If the Fix & Re-review loop repeats three consecutive times, follow the Escalation on Deadlock rule.
6. Approve the Task or Subtask only when no Blocker findings remain and required verification has been completed or explicitly reported as unavailable.

## Task Decomposition Rule

When decomposing feature work or writing Specs, Tasks, or Subtasks, load `docs/agents/spec-task-format.md`.
When preparing Subtasks for implementation, also follow the context-packet rules in `docs/agents/context-loading.md`.

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

Use the Spec Format in `docs/agents/spec-task-format.md`.

## Task Format

Use the Task Format in `docs/agents/spec-task-format.md`.

## Review Input Requirements

Before Review Agent starts, load `docs/agents/review-format.md`.

## Review Output Format

Use the Review Output Format in `docs/agents/review-format.md`.

## Security Review Checklist

Review Agent must load `docs/agents/security-review-checklist.md` when a Task touches authentication, authorization, user input, files, external APIs, dependencies, configuration, data storage, logging, or workspace operations.

## Security Review Output Format

Use the Security Review Output Format in `docs/agents/security-review-checklist.md`.

## Completion Rules

A Task or Subtask is complete only when:

- The implementation matches the approved Spec.
- Acceptance criteria are satisfied.
- Review Agent reports no Blocker findings.
- Security review has been completed when relevant.
- Relevant tests, checks, or manual verification have been run.
- The user can understand what changed and why.

Do not mark work complete only because code was written.
