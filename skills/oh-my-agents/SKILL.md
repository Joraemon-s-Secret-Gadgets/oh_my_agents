---
name: oh-my-agents
description: Use when the user asks to create, launch, spawn, delegate to, or coordinate project role subagents such as Spec Agent, Task Agent, Implementation Agent, Review Agent, Frontend QA Review Agent, Backend Security Review Agent, or Crawl Implementation Agent according to a project's AGENTS.md.
metadata:
  version: "0.6.6"
---

# Oh My Agents

Use this skill as a lightweight router for project-defined role subagents.

The root `AGENTS.md` is the source of truth. This skill must never bypass, weaken, or replace project rules. It only helps interpret abstract user requests and coordinate tool-backed subagent creation.

Version: 0.6.6

## Agent Creation Semantics

Treat "agent 생성", "에이전트 생성", "subagent 생성", "create agent", "spawn agent", "launch agent", and "delegate to agent" as requests for real tool-backed subagent creation when a supported harness is available.

Do not silently convert creation requests into current-session role activation. If a supported harness is unavailable, say that real subagent creation is unavailable and ask whether to continue by role activation.

Interpret related wording as follows:

- "팀 제안해줘", "team proposal", or "agent team proposal" means proposal only. Do not spawn subagents.
- "제안 승인. 시작해줘", "agent team 실행해줘", or "실제 subagent로 생성해줘" means create approved tool-backed subagents when scope is clear.
- "<role>로 동작해줘", "역할로 동작해줘", or "현재 Codex가 <role> 역할로 해줘" means current-session role activation, not subagent creation.

Normalize Korean requests into English execution intent before acting:

- `에이전트 생성해줘` -> `Create a real tool-backed subagent.`
- `<Role> Agent 생성해줘` -> `Create a real tool-backed <Role> Agent subagent.`
- `<Role> Agent 생성해서 <task> 해줘` -> `Create a real tool-backed <Role> Agent subagent and assign it the bounded task.`
- `<Role>로 동작해줘` -> `Act as <Role> in the current Codex session. Do not create a subagent.`
- `팀 제안해줘` -> `Prepare an agent team proposal only. Do not create subagents.`
- `제안 승인. 시작해줘` -> `Start the approved proposal by creating real tool-backed subagents when scope is sufficient.`

## Task-Based Creation Gate

When the user provides `Task` plus `Agent` plus a creation command, do not stop at proposal or role activation.

If these fields are present, create a real tool-backed subagent immediately when a supported harness is available:

- Task or Goal
- Agent name or role
- Source of Truth
- Scope or target files
- Verification, review focus, or expected output
- Creation command such as `생성해줘`, `만들어줘`, `spawn`, `launch`, or `delegate`

Before spawning, state only a concise creation summary:

```md
Creating Subagent:
- Agent:
- Display Name:
- Core Role:
- Harness Agent Type:
- Harness Nickname: auto-assigned by harness
- Task:
- Source of Truth:
- Scope:
- Verification / Output:
```

Then call the supported subagent harness. Do not ask for a second approval when the user already used a creation command and the required fields are sufficient.

Harness nickname rules:

- `Agent Name`, `Display Name`, and `Core Role` are project-defined names that Main Codex must set in the subagent prompt and required final report.
- `Harness Nickname` is a runtime nickname returned by the subagent harness.
- Do not claim that `Harness Nickname` was manually set unless the harness exposes an explicit naming field.
- After spawning, report `Agent ID`, `Harness Nickname`, `Harness Agent Type`, `Agent Name`, and `Core Role`.
- Require the subagent final report to start with the project-defined `Agent Name`.

Harness agent type mapping:

- Use `worker` for implementation, file edits, test fixes, docs writing, or any task that may change files.
- Use `explorer` for read-only review, codebase investigation, issue analysis, or verification questions.
- Use the default subagent type only when the task is neither clearly worker nor explorer.

If one or two required fields are missing, ask only for those missing fields. If more than two safety-critical fields are missing, ask for a bounded Task/Agent/Scope input block instead of trying to infer.

## Initial Work Intake Rule

When the user provides a new feature, bug, product task, GitHub Issue, or implementation goal but does not provide an approved Spec, Main Codex must not write the Spec itself by default.

Instead, create a real tool-backed Spec Agent when a supported subagent harness is available.

Use this rule for requests such as:

- `이 기능 작업 시작해줘`
- `Lovv #123 작업 시작해줘`
- `회원가입 기능 만들어야 해`
- `이 이슈 기반으로 작업해줘`
- `Task 시작하자`
- `새 기능 구현 플로우 잡아줘`

The Spec Agent must produce or update the Spec. After the Spec is approved, create or request a Task Agent to break it into Tasks and Subtasks. Main Codex coordinates and integrates; it should not replace Spec Agent or Task Agent work unless the user explicitly asks for current-session role activation or no subagent harness is available.

Initial intake routing:

1. No approved Spec exists -> create Spec Agent.
2. Approved Spec exists but Tasks/Subtasks do not -> create Task Agent.
3. Approved Subtask exists and implementation is requested -> create Implementation Agent.
4. Completed work or diff exists and review is requested -> create Review Agent.

## Core Flow

When the user asks to create or run an agent:

1. Read the root `AGENTS.md`.
2. Read `docs/projects/lovv-project-context.md`.
3. If present, read `docs/agents/agent-creation-guidelines.md`.
4. Parse the request into:
   - User Request Original
   - Structured Agent Contract
   - Display Name
   - Core Role
   - Domain Focus
   - Work Focus
   - Execution Mode
   - Goal
   - Source of Truth
   - Scope
   - Out of Scope
   - Required Context
   - Output Format
   - Verification
   - Stop Condition
5. If required inputs are missing, ask at most three questions.
6. Load only the docs required for the parsed role, focus, and execution mode.
7. If a supported subagent harness is available, create a tool-backed subagent.
8. If no harness is available, tell the user and ask whether to continue by current-session role activation.
9. Pass only the minimum required context to the subagent.
10. Collect the result, check it against the user's request, and summarize it.
11. After completion, close, archive, terminate, or delete unused subagent contexts unless the user explicitly asks to keep them.

## Routing Defaults

Use these defaults for abstract Korean or English requests:

- "스펙", "기획", "requirements", "design" -> Spec Agent.
- "작업 쪼개", "Task", "Subtask", "breakdown" -> Task Agent.
- "구현", "수정", "fix", "implement" -> Implementation Agent.
- "리뷰", "검토", "review" -> Review Agent.
- "프론트", "화면", "UI", "React", "Tailwind" -> Frontend domain.
- "접근성", "반응형", "폼", "컴포넌트", "라우트", "hook", "client state" -> Frontend domain.
- Lovv "백엔드", "API", "endpoint", "Lambda", "SAM", "API Gateway", "serverless" -> Backend AWS SAM domain.
- Lovv "DB", "database", "schema", "migration", "data model" -> Aurora MySQL-compatible data/API domain.
- "RAG", "챗봇", "recommendation", "itinerary generation", "AI 일정" -> infer RAG/API/Frontend scope from the requested behavior and Lovv project context.
- "전체 흐름", "E2E", "full-stack" -> Full-stack domain.
- "QA", "검증", "시나리오" -> QA focus.
- "보안", "취약점", "secret", "auth" -> Security focus.
- "크롤링", "수집", "crawl", "scrape" -> Crawl focus.
- "딥크롤링", "deep crawl" -> Crawl focus with Deep Crawl gate.
- "BeautifulSoup", "Selenium", "Scrapling" -> Crawl focus.
- "에이전트 팀", "agent team", "team launcher", "Owner Auto Team" -> Use `lovv-agent-team-launcher` when installed.
- "순차", "sequential" -> Sequential Mode.
- "하이브리드", "혼합", "hybrid" -> Hybrid Mode.
- "병렬", "parallel" -> Parallel Mode.

For detailed naming and prompt examples, read `references/role-routing.md` only when needed.

## Required Input Gate

Do not spawn vague or over-scoped subagents.

Ask only for missing required inputs that materially affect safety, scope, or output quality. Ask at most three questions at once.

Typical missing inputs:

- Implementation Agent: Task/Subtask ID, Source of Truth, allowed write scope, verification command.
- Review Agent: review target, Source of Truth, review focus.
- Spec Agent: feature idea or goal, target user when not obvious, constraints when known.
- Task Agent: approved Spec path or approved Spec content.
- Frontend Domain: target files or folders, UI states, API/data assumptions, responsive requirements, accessibility requirements, verification command or browser check, out-of-scope behavior.
- Backend AWS SAM Domain: Lambda function, API route, SAM template scope, request/response contract, Aurora MySQL assumptions, auth/IAM assumptions, verification command, out-of-scope behavior.
- Crawl Focus: URLs, columns, output path, output format, allowed tools, verification, stop condition.
- Deep Crawl: seed URLs, domain allowlist, max depth, max pages, rate limit, output columns, stop condition.

For question templates, read `references/missing-input-questions.md` only when needed.

## Invocation Safety

- Do not create an Implementation Agent without a bounded write scope.
- Do not create a Review Agent without a review target.
- Do not create a Crawl-focused agent without approved URLs and columns.
- State inferred values before spawning a subagent.
- Preserve the user's original Korean or non-English request as `User Request Original`.
- Create `Structured Agent Contract` in English for execution reliability.
- The original request remains authoritative for user intent and success criteria.
- Lovv work must load `docs/projects/lovv-project-context.md` before selecting role, domain, execution mode, stack assumption, or harness route.
- Lovv API work defaults to Backend AWS SAM.
- Lovv API work that overlaps small-city, city data loading, map/backend integration, API Gateway routes, Lambda handlers, SAM templates, or frontend API adapters must read the Existing API Source Of Truth section in `docs/projects/lovv-project-context.md` before creating or changing contracts.
- Treat Task 9/10 API documents as the current contract and adapter boundary, not as proof of a deployed AWS SAM backend.
- Treat endpoint paths in those documents as placeholders until the actual SAM/API Gateway base URL, stage, auth/environment configuration, and DB readiness are verified.
- The current implemented path is frontend-only and the DB is under construction; do not implement live API calls unless backend readiness is confirmed by an approved Spec, deployment output, or user instruction.
- Lovv database work defaults to Amazon Aurora MySQL-Compatible on Amazon RDS. Do not infer Neo4j, another graph database, PostgreSQL, or EC2 unless an approved Spec says so.
- Lovv RAG chatbot work defaults to HTTP REST and Lambda/API Gateway response streaming when streaming is needed. Do not infer WebSocket unless an approved Spec requires it.
- Lovv persistence defaults to confirmed or final itineraries only. Do not infer server-side in-progress chat or draft persistence without a Spec update.
- Frontend-domain agents must load `docs/agents/frontend-agent-rules.md` before planning, implementation, or review.
- Do not create a Frontend Implementation Agent without target files or folders, UI states, API/data assumptions, verification, and out-of-scope behavior.
- If Execution Mode is not specified, use Hybrid Mode for ordinary feature work and Sequential Mode for security-sensitive, database, authentication, authorization, payment, migration, irreversible, or ambiguous work.
- Use Parallel Mode only when the user explicitly asks for parallel agents or when write scopes are clearly separated and Main Codex can integrate the results safely.
- Crawl-focused agents must load `docs/prompts/crawl-task-prompt.md` before planning, implementation, or review.
- Crawl-focused implementation must use Python 3.12 files or scripts and the default crawl tools: BeautifulSoup, Selenium, and Scrapling. Additional crawler frameworks require explicit user or Task approval.
- Deep crawl requests require seed URLs, domain allowlist, max depth, max pages, rate limit, output columns, and stop condition.
- Follow the role permission matrix in `docs/agents/agent-creation-guidelines.md` when present.
- Parallel Implementation Agents must not have overlapping write scopes.
- Review Agents are read-only by default unless the user explicitly asks them to edit review documentation.
- If a subagent becomes unresponsive or produces no meaningful progress within the root No-Progress Limit, preserve useful handoff output and terminate or delete that context before spawning a replacement.
- After a subagent completes its assigned work, close, archive, terminate, or delete the unused context unless the user explicitly asks to keep it.
- Agent cleanup applies only to agent contexts, threads, or harness-managed agent records. It must not delete project files, specs, reports, commits, branches, or user data unless explicitly requested.
- Use an agent run log for substantial or multi-agent work when the project provides `docs/reports/agent-runs/RUN_TEMPLATE.md`.
- Require subagent final reports to include Agent Name, Task/Subtask, Scope, Changed Files, Commands Run, Verification Result, Blockers, Assumptions, and Next Recommended Action.

## Context Loading

Always keep context small:

- Do not load `AGENTS.ko.md` unless the user asks for Korean explanation or Korean docs are being edited.
- Do not load all `docs/agents/*`.
- Do not load all `docs/agents/modes/*`; load only the selected execution mode file.
- Read `docs/agents/context-loading.md` when the task is context-heavy or token usage matters.
- Read `docs/projects/lovv-project-context.md` before role/domain/mode/stack routing in this project.
- Read `docs/agents/review-format.md` only for Review Agent work.
- Read `docs/agents/security-review-checklist.md` only for Security focus or security-sensitive work.
- Read `docs/agents/frontend-agent-rules.md` only for Frontend domain work.
- Read `docs/prompts/crawl-task-prompt.md` only for Crawl focus.

## Token Management

Baseline context is root `AGENTS.md` plus `docs/projects/lovv-project-context.md`.

When creating subagents, pass compact context packets instead of broad documents:

- Role, domain, focus, and execution mode.
- Source of truth paths and required sections.
- Allowed scope and forbidden scope.
- Acceptance criteria.
- Verification commands.
- Stop condition.
- Short relevant decision summary.

Do not pass full Specs, full reports, all prompts, all mode files, full logs, broad source folders, or `AGENTS.ko.md` to subagents by default.

If the subagent needs more context, require it to ask for specific files, sections, or command output.

## Subagent Prompt

When spawning a subagent, make the prompt bounded:

- State the display name and parsed role/domain/focus.
- State the selected execution mode and the mode file to load.
- Include the Source of Truth and allowed scope.
- List required docs to read.
- State forbidden scope and stop conditions.
- Require a concise final report with changed files, verification, blockers, and assumptions.

For reusable prompt patterns, read `references/spawn-prompt-template.md` only when needed.
