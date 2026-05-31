# MAX Parallel Execution Mode

This is the MAX full-context version of Parallel Mode.

Use this file when Pro/MAX users want a standalone, no-token-saving execution mode document instead of relying only on the token-optimized `docs/agents/modes/parallel.md`.

## Purpose

Parallel Mode is the fastest but highest-risk operating mode.

It should be used only when the user explicitly asks for parallel agents or when Main Codex can prove that the work is independently scoped.

## When To Use

Use this mode for:

- Read-heavy exploration, repository audits, log analysis, test analysis, and summarization.
- Independent review tracks such as security, QA, accessibility, performance, and maintainability.
- Independent implementation units with non-overlapping file ownership and stable shared contracts.
- Large documentation or planning work split by clearly independent sections.

Prefer Sequential or Hybrid Mode for security-sensitive, database, auth, payment, migration, or unclear implementation work.

## Required Preconditions

Parallel Mode requires:

- A clear Source of Truth.
- A written Task/Subtask breakdown.
- A scope ownership table.
- Non-overlapping write scopes.
- Explicit out-of-scope boundaries.
- Verification commands for each agent.
- Stop conditions for each agent.
- A final integration and review step owned by Main Codex.

If any precondition is missing, ask the user for the missing input or fall back to Hybrid Mode.

## Scope Ownership Table

Before spawning parallel agents, Main Codex must define a table with:

| Agent | Role | Task/Subtask | Write Scope | Read Scope | Forbidden Scope | Verification | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |

Every writeable file or directory may have only one owner.

## Operating Rules

- Parallel agents must not modify overlapping files, directories, migrations, contracts, or generated outputs.
- Review agents are read-only by default.
- Implementation agents must not commit, push, pull, merge, rebase, or create pull requests.
- Main Codex must wait for all required parallel outputs before reporting completion.
- Main Codex must reconcile conflicts, summarize tradeoffs, and run final verification.
- If a parallel agent reports a blocker, Main Codex must pause integration and decide whether to continue, narrow scope, or ask the user.

## Recommended Parallel Patterns

Read-heavy:

- Security Review Agent checks security risks.
- QA Review Agent checks user flows, acceptance criteria, and test gaps.
- Maintainability Review Agent checks structure, duplication, and complexity.

Split implementation:

- Frontend Implementation Agent owns only frontend files.
- Backend Implementation Agent owns only backend files.
- Review Agent reviews the integrated diff after both finish.

Exploration:

- One agent maps existing frontend structure.
- One agent maps existing backend/API structure.
- One agent maps data model or documentation context.

## Forbidden Parallel Patterns

Do not run parallel implementation when:

- Agents need to edit the same file.
- Agents need to change the same API contract from different sides without a single owner.
- Agents need to create or reorder database migrations.
- Agents need to change authentication, authorization, secret handling, or permission logic without a single owner.
- Verification requires one agent's unfinished work.

## Run Log

Parallel Mode requires an agent run log under `docs/reports/agent-runs/` when the project provides the template.

The run log must include the scope ownership table, agents used, files touched, commands run, verification results, blockers, and integration outcome.

## Final Integration Gate

Parallel Mode is not complete until Main Codex:

- Confirms no write scopes overlapped.
- Reviews every subagent final report.
- Reconciles conflicts or reports unresolved conflicts.
- Runs relevant final verification.
- Requests Review Agent approval for the integrated result when implementation changed files.
- Reports remaining risks and user decisions.

## Stop Conditions

Stop and escalate to the user when:

- Any write scope overlaps.
- A shared contract changes without a single owner.
- Two agents produce incompatible results.
- Verification fails three consecutive times.
- Final integration cannot be reviewed safely.
