---
name: oh-my-agents
description: Use when the user asks to create, launch, spawn, delegate to, or coordinate project role subagents such as Spec Agent, Task Agent, Implementation Agent, Review Agent, Frontend QA Review Agent, Backend Security Review Agent, or Crawl Implementation Agent according to a project's AGENTS.md.
---

# Oh My Agents

Use this skill as a lightweight router for project-defined role subagents.

The root `AGENTS.md` is the source of truth. This skill must never bypass, weaken, or replace project rules. It only helps interpret abstract user requests and coordinate tool-backed subagent creation.

## Core Flow

When the user asks to create or run an agent:

1. Read the root `AGENTS.md`.
2. If present, read `docs/agents/agent-creation-guidelines.md`.
3. Parse the request into:
   - Display Name
   - Core Role
   - Domain Focus
   - Work Focus
   - Goal
   - Source of Truth
   - Scope
4. If required inputs are missing, ask at most three questions.
5. Load only the docs required for the parsed role and focus.
6. If a supported subagent harness is available, create a tool-backed subagent.
7. If no harness is available, tell the user and ask whether to continue by current-session role activation.
8. Pass only the minimum required context to the subagent.
9. Collect the result, check it against the user's request, and summarize it.

## Routing Defaults

Use these defaults for abstract Korean or English requests:

- "스펙", "기획", "requirements", "design" -> Spec Agent.
- "작업 쪼개", "Task", "Subtask", "breakdown" -> Task Agent.
- "구현", "수정", "fix", "implement" -> Implementation Agent.
- "리뷰", "검토", "review" -> Review Agent.
- "프론트", "화면", "UI", "React", "Tailwind" -> Frontend domain.
- "백엔드", "API", "Django", "DB", "migration" -> Backend domain.
- "전체 흐름", "E2E", "full-stack" -> Full-stack domain.
- "QA", "검증", "시나리오" -> QA focus.
- "보안", "취약점", "secret", "auth" -> Security focus.
- "크롤링", "수집", "crawl", "scrape" -> Crawl focus.

For detailed naming and prompt examples, read `references/role-routing.md` only when needed.

## Required Input Gate

Do not spawn vague or over-scoped subagents.

Ask only for missing required inputs that materially affect safety, scope, or output quality. Ask at most three questions at once.

Typical missing inputs:

- Implementation Agent: Task/Subtask ID, Source of Truth, allowed write scope, verification command.
- Review Agent: review target, Source of Truth, review focus.
- Spec Agent: feature idea or goal, target user when not obvious, constraints when known.
- Task Agent: approved Spec path or approved Spec content.
- Crawl Focus: URLs, columns, output path, output format.

For question templates, read `references/missing-input-questions.md` only when needed.

## Context Loading

Always keep context small:

- Do not load `AGENTS.ko.md` unless the user asks for Korean explanation or Korean docs are being edited.
- Do not load all `docs/agents/*`.
- Read `docs/agents/context-loading.md` when the task is context-heavy or token usage matters.
- Read `docs/agents/review-format.md` only for Review Agent work.
- Read `docs/agents/security-review-checklist.md` only for Security focus or security-sensitive work.
- Read `docs/prompts/crawl-task-prompt.md` only for Crawl focus.

## Subagent Prompt

When spawning a subagent, make the prompt bounded:

- State the display name and parsed role/domain/focus.
- Include the Source of Truth and allowed scope.
- List required docs to read.
- State forbidden scope and stop conditions.
- Require a concise final report with changed files, verification, blockers, and assumptions.

For reusable prompt patterns, read `references/spawn-prompt-template.md` only when needed.
