# TASK2 Subtasks

## Task 2 Overview

Task 2 establishes repository safety and handover scaffolding that supports the root `AGENTS.md` rules before application code grows.

The first priority is preventing accidental secret tracking and making future Task reports/specs repeatable.

## Context and Dependencies

- Previous Task Report: `docs/reports/TASK1_COMPLETION.md`
- Base Branch: `main`
- Root Instructions: `AGENTS.md`
- Korean Explanation: `AGENTS.ko.md`
- Workspace: `/Users/jeonjonghyeok/Documents/Final`

Dependencies:

- Task 1 must be treated as the current workflow baseline.
- Root `AGENTS.md` security, Workspace Boundary, environment variable safety, and Task Startup rules must remain in force.
- Do not access files outside the workspace.
- Do not read or create real `.env` files.
- Do not start the next Subtask until the current Subtask is implemented, verified, reported, and confirmed by the user.

## Deadlock Escape Conditions

Stop immediately and escalate to the user when any of the following happens:

- The same test or verification step fails three consecutive times.
- Review and fix cycles repeat three consecutive times without convergence.
- The requested direction becomes ambiguous.
- A Subtask appears to require access outside the workspace.
- A Subtask appears to require reading or committing real secrets.

## Subtask 2.1: Add Environment File Safety Baseline

- Purpose: Prevent accidental tracking of real environment files and provide a safe dummy example file for future developers.
- Target Files:
  - `.gitignore`
  - `.env.example`
- Local Rules:
  - Do not create `.env` or `.env.local`.
  - Do not include real secrets, real API tokens, or production values.
  - Keep `.env.example` limited to dummy values and comments.
  - Ensure `.env.example` is not ignored by Git.
- Acceptance Criteria:
  - `.gitignore` exists.
  - `.env`, `.env.local`, and other real `.env.*` files are ignored.
  - `.env.example` remains trackable.
  - `.env.example` contains only dummy values.
  - No real secret is introduced.
- Verification Commands:
  - `git check-ignore .env .env.local .env.production`
  - `git check-ignore .env.example`
  - `git status --short`

## Subtask 2.2: Add Documentation Directory Overview

- Purpose: Make the `docs/` structure understandable for future agents and teammates.
- Target Files:
  - `docs/README.md`
- Local Rules:
  - Keep the document concise.
  - Explain `docs/reports/` and `docs/specs/`.
  - Reference root `AGENTS.md` as the source of workflow truth.
- Acceptance Criteria:
  - `docs/README.md` describes where reports and specs belong.
  - The README explains that new top-level Tasks should start from `docs/specs/TASK[number]_SUBTASKS.md`.
  - The README does not duplicate the full root `AGENTS.md`.
- Verification Commands:
  - `sed -n '1,220p' docs/README.md`
  - `git status --short`

## Subtask 2.3: Add Reusable Handover Templates

- Purpose: Make future Task completion and Subtask planning documents consistent.
- Target Files:
  - `docs/templates/TASK_COMPLETION_TEMPLATE.md`
  - `docs/templates/TASK_SUBTASKS_TEMPLATE.md`
- Local Rules:
  - Templates must match the fields required by root `AGENTS.md`.
  - Review field names should remain English where structured output is needed.
  - Explanatory placeholder text may be Korean.
- Acceptance Criteria:
  - Completion report template includes timestamp, responsible agent, Spec Alignment, changed files, verification results, and user confirmation items.
  - Subtask template includes context, dependencies, atomic Subtasks, verification commands, and deadlock escape conditions.
  - Templates do not contain real project secrets or fake production credentials.
- Verification Commands:
  - `sed -n '1,240p' docs/templates/TASK_COMPLETION_TEMPLATE.md`
  - `sed -n '1,260p' docs/templates/TASK_SUBTASKS_TEMPLATE.md`
  - `git status --short`

## Subtask 2.4: Review Documentation Synchronization

- Purpose: Confirm that root English instructions and Korean explanations still describe the same workflow after Task 2 documentation changes.
- Target Files:
  - `AGENTS.md`
  - `AGENTS.ko.md`
  - `docs/README.md`
  - `docs/templates/TASK_COMPLETION_TEMPLATE.md`
  - `docs/templates/TASK_SUBTASKS_TEMPLATE.md`
- Local Rules:
  - Do not rewrite sections that do not need changes.
  - If `AGENTS.md` changes, update `AGENTS.ko.md` in the same Subtask.
  - Keep changes scoped to documentation consistency.
- Acceptance Criteria:
  - `AGENTS.md` and `AGENTS.ko.md` remain synchronized.
  - No root security, workflow, or Workspace Boundary rule is weakened.
  - Folder-level inheritance remains clearly documented.
- Verification Commands:
  - `rg -n 'Task Startup Rule|Task Completion & Handover Rule|Environment Variable Safety|File Synchronization Rule' AGENTS.md AGENTS.ko.md`
  - `rg -n 'T[O]DO|T[B]D|F[I]XME' AGENTS.md AGENTS.ko.md docs`
  - `git status --short`

## Subtask 2.5: Complete Task 2 Handover

- Purpose: Close Task 2 using the same handover protocol defined by root `AGENTS.md`.
- Target Files:
  - `docs/reports/TASK2_COMPLETION.md`
  - `docs/specs/TASK3_SUBTASKS.md`
- Local Rules:
  - Do not invent Task 3 implementation details beyond the agreed next scope.
  - Ask the user if Task 3 scope is unclear.
  - Do not start Task 3 after creating these files.
- Acceptance Criteria:
  - Task 2 completion report summarizes completed Subtasks, changed files, and verification results.
  - Task 3 Subtask sheet is created only from confirmed user direction.
  - Agent stops after handover files are created.
- Verification Commands:
  - `sed -n '1,260p' docs/reports/TASK2_COMPLETION.md`
  - `sed -n '1,260p' docs/specs/TASK3_SUBTASKS.md`
  - `git status --short`
