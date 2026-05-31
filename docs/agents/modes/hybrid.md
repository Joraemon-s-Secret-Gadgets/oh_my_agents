# Hybrid Execution Mode

Use Hybrid Mode as the default operating mode for ordinary feature work.

Hybrid Mode keeps planning sequential while allowing limited parallel work only where scopes are independent.

## When To Use

Use this mode for:

- Standard feature work with a clear Spec and Task breakdown.
- Frontend and backend work that can be separated by file ownership.
- Independent review tracks such as QA review, security review, accessibility review, and maintainability review.
- Exploration or verification work that can run without modifying shared files.

Use Sequential Mode instead when requirements, write scope, or security impact are unclear.

## Operating Rules

- Spec Workflow is always sequential.
- Task Breakdown Workflow is always sequential.
- Implementation may run in parallel only when each Implementation Agent has a clearly separated write scope.
- Review may run in parallel when reviewers are read-only or write only to explicitly approved review documentation.
- Main Codex owns coordination, conflict prevention, result integration, user communication, and requested Git operations.
- If two agents need to touch the same file, path, migration, API contract, data model, or shared component, run those agents sequentially.

## Allowed Parallel Work

Parallel work is allowed for:

- Frontend implementation and backend implementation with non-overlapping file scopes.
- Read-only codebase exploration.
- Test, lint, build, or log analysis.
- QA Review Agent, Security Review Agent, UX/Accessibility Review Agent, and Maintainability Review Agent when they are read-only.

Parallel work is not allowed for:

- Multiple Implementation Agents editing the same files or shared contracts.
- Multiple agents changing database migrations.
- Multiple agents changing authentication, authorization, permission, or secret-handling code without a single owner.
- Any work where final integration cannot be clearly reviewed.

## Required Sequence

1. Spec Agent prepares or updates the Spec.
2. Task Agent breaks the approved Spec into Tasks and Atomic Subtasks.
3. Main Codex selects which Subtasks can be parallelized.
4. Main Codex assigns each agent an explicit scope, out-of-scope list, source of truth, verification command, and stop condition.
5. Agents run independently only inside their assigned scope.
6. Main Codex waits for all required agent outputs.
7. Main Codex integrates results and resolves conflicts.
8. Review Agent or parallel read-only reviewers review the integrated result.
9. Main Codex reports verification, findings, risks, and required user decisions.

## Scope Ownership

Before starting parallel work, Main Codex must define:

- Agent name.
- Task/Subtask.
- Owned files or directories.
- Forbidden files or directories.
- Shared contracts that must not be changed without approval.
- Verification command.
- Expected output.

## Context Loading

- Load this file only when Hybrid Mode is selected.
- Load `docs/agents/context-loading.md` when creating subtask context packets.
- Do not load Sequential or Parallel mode files during Hybrid Mode unless the user asks to compare modes.

## Run Log

Create or update an agent run log when Hybrid Mode uses two or more subagents for the same user request.

## Stop Conditions

Stop and escalate to the user when:

- Agent scopes overlap.
- A shared contract changes without an assigned owner.
- Verification fails three consecutive times.
- Fix & Re-review repeats three consecutive times.
- Main Codex cannot integrate subagent results safely.
