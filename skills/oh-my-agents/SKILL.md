---
name: oh-my-agents
description: Use when the user asks to create, launch, spawn, delegate to, or coordinate project role subagents such as Spec Agent, Task Agent, Implementation Agent, Review Agent, Frontend QA Review Agent, Backend Security Review Agent, or Crawl Implementation Agent according to a project's AGENTS.md.
metadata:
  version: "0.6.2"
---

# Oh My Agents

Use this skill as a lightweight router for project-defined role subagents.

The root `AGENTS.md` is the source of truth. This skill must never bypass, weaken, or replace project rules. It only helps interpret abstract user requests and coordinate tool-backed subagent creation.

Version: 0.6.2

## Core Flow

When the user asks to create or run an agent:

1. Read the root `AGENTS.md`.
2. If present, read `docs/agents/agent-creation-guidelines.md`.
3. Parse the request into:
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
4. If required inputs are missing, ask at most three questions.
5. Load only the docs required for the parsed role, focus, and execution mode.
6. If a supported subagent harness is available, create a tool-backed subagent.
7. If no harness is available, tell the user and ask whether to continue by current-session role activation.
8. Pass only the minimum required context to the subagent.
9. Collect the result, check it against the user's request, and summarize it.
10. After completion, close, archive, terminate, or delete unused subagent contexts unless the user explicitly asks to keep them.

## Routing Defaults

Use these defaults for abstract Korean or English requests:

- "스펙", "기획", "requirements", "design" -> Spec Agent.
- "작업 쪼개", "Task", "Subtask", "breakdown" -> Task Agent.
- "구현", "수정", "fix", "implement" -> Implementation Agent.
- "리뷰", "검토", "review" -> Review Agent.
- "프론트", "화면", "UI", "React", "Tailwind" -> Frontend domain.
- "접근성", "반응형", "폼", "컴포넌트", "라우트", "hook", "client state" -> Frontend domain.
- "백엔드", "API", "Django", "DB", "migration" -> Backend domain.
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
- Read `docs/agents/review-format.md` only for Review Agent work.
- Read `docs/agents/security-review-checklist.md` only for Security focus or security-sensitive work.
- Read `docs/agents/frontend-agent-rules.md` only for Frontend domain work.
- Read `docs/prompts/crawl-task-prompt.md` only for Crawl focus.

## Subagent Prompt

When spawning a subagent, make the prompt bounded:

- State the display name and parsed role/domain/focus.
- State the selected execution mode and the mode file to load.
- Include the Source of Truth and allowed scope.
- List required docs to read.
- State forbidden scope and stop conditions.
- Require a concise final report with changed files, verification, blockers, and assumptions.

For reusable prompt patterns, read `references/spawn-prompt-template.md` only when needed.
