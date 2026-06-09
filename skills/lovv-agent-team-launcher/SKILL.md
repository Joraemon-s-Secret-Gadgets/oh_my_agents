---
name: lovv-agent-team-launcher
description: Use when the user asks to launch, create, run, coordinate, or propose a Lovv agent team from a GitHub Issue, including short Korean invocations such as "Lovv #123 팀 제안해줘", "Lovv #123 제안 승인. 순차형으로 시작해줘", or "Owner Auto Team: Lovv #123 하이브리드로 실행해줘". Use this after or with the Lovv Issue Router proposal when the user explicitly wants real subagents or team execution.
metadata:
  version: "0.1.1"
---

# Lovv Agent Team Launcher

Use this skill to coordinate an on-demand Lovv agent team from a GitHub Issue.

This skill is a launcher workflow, not a permanent background service. It must follow the project root `AGENTS.md`, the `oh-my-agents` routing rules, and the Level 1 Issue Router safety model.

## Short Invocation Contract

Users should be able to trigger this skill with short natural-language commands. Treat the command as a trigger, not as the source of truth.

Recognized commands:

- `Lovv #<issue-number> 팀 제안해줘`: read the Lovv GitHub Issue and propose an agent team only. Do not launch agents.
- `Lovv #<issue-number> 제안 승인. 순차형으로 시작해줘`: launch the approved proposal in Sequential Mode. If there is no prior proposal for the same issue in the current context, show the proposal first and ask for approval.
- `Lovv #<issue-number> 제안 승인. 하이브리드로 시작해줘`: launch the approved proposal in Hybrid Mode. If there is no prior proposal for the same issue in the current context, show the proposal first and ask for approval.
- `Owner Auto Team: Lovv #<issue-number> <mode>로 실행해줘`: use Owner Auto Team Pilot for the issue and mode, then continue only within the Owner Auto Team safety limits.

Do not require users to name the exact team preset or agent roles. Infer the proposal from the GitHub Issue title, body, labels, template fields, `Layer`, `Priority`, acceptance criteria, and completion conditions.

If the user asks to create or run an agent team after approving a proposal, treat it as a real tool-backed subagent creation request when a supported harness is available. If no supported harness is available, say so clearly and continue only by current-session role activation after user approval.

## Safety Defaults

- Do not launch a team unless the user explicitly asks for agent team execution.
- For standard users, always show a team proposal and ask for approval before spawning subagents.
- Owner Auto Team Pilot is allowed only when the user explicitly says `Owner Auto Team`.
- Do not create branches, commits, PRs, or close issues automatically.
- Do not spawn agents with overlapping write scopes.
- Do not keep agents alive after final reports are collected.
- If no tool-backed subagent harness is available, fall back to current-session role activation and say so clearly.

## Core Workflow

1. Read the root `AGENTS.md`.
2. Read `docs/harnesses/lovv-issue-router-level1.md` when issue routing context is needed.
3. Run or request the Level 1 proposal:
   - `python3 scripts/lovv_issue_router.py <issue-number-or-url>`
4. Choose an agent team preset from `references/team-presets.md`.
5. Present the team proposal:
   - Team Name
   - Execution Mode
   - Coordinator
   - Team Members
   - Scope and Out of Scope
   - Execution Order
   - Stop Conditions
6. Ask for user approval before launching, unless the user explicitly requested Owner Auto Team.
7. If a supported tool-backed subagent harness is available, spawn only the approved team members.
8. If no supported harness is available, continue by current-session role activation.
9. Collect each agent final report and summarize integration status.
10. Close, archive, terminate, or delete unused subagent contexts when the harness supports cleanup.

## Team Selection

Load `references/team-presets.md` when selecting team members.

Quick defaults:

- New idea, unclear requirements, or product planning -> Planning Team.
- Frontend UI, React, Tailwind, routing, state, accessibility -> Frontend Feature Team.
- Django, API, DB, migrations, backend validation -> Backend API Team.
- Auth, token, secret, env, permissions, external API security -> Security Review Team.
- Crawl, scrape, BeautifulSoup, Selenium, Scrapling, data extraction -> Crawl Data Team.
- Merge readiness, final QA, release review -> Release Gate Team.

## Launch Rules

When launching actual subagents:

- Use worker agents for bounded implementation work.
- Use explorer agents for read-only codebase questions.
- Give each worker a disjoint write scope.
- Tell each agent it is not alone in the codebase and must not revert others' changes.
- Include `User Request Original` and `Structured Agent Contract`.
- Include source issue URL and issue number.
- Include required context files only.
- Require final reports with Agent Name, Scope, Changed Files, Commands Run, Verification Result, Blockers, Assumptions, and Next Recommended Action.

## Approval Prompt

Before launching for standard users, ask:

```md
Agent Team Proposal:
- Team Name:
- Execution Mode:
- Coordinator:
- Members:
- Scope:
- Out of Scope:
- Execution Order:
- Missing Inputs:

Approval Required:
- Reply `Lovv #<issue-number> 제안 승인. 순차형으로 시작해줘` to launch sequentially.
- Reply `Lovv #<issue-number> 제안 승인. 하이브리드로 시작해줘` to launch in hybrid mode.
- Reply with edits to change team, scope, mode, or order.
```

## Owner Auto Team Pilot

Use Owner Auto Team only when explicitly requested.

Owner Auto Team may skip the second approval prompt after showing the proposal, but it must still:

- Use only a GitHub Issue as source of truth.
- Limit to 2 or 3 subagents.
- Refuse overlapping write scopes.
- Refuse automatic commits, pushes, PRs, and issue close.
- Create or request an agent run summary.
- Clean up subagents after collecting reports.
