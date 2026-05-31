# MAX Sequential Execution Mode

This is the MAX full-context version of Sequential Mode.

Use this file when Pro/MAX users want a standalone, no-token-saving execution mode document instead of relying only on the token-optimized `docs/agents/modes/sequential.md`.

## Purpose

Sequential Mode is the safest operating mode. It keeps every step ordered and reviewable.

Use it when safety, clarity, or user confirmation is more important than speed.

## When To Use

Use this mode for:

- New projects or unclear requirements.
- Authentication, authorization, permissions, payments, security, privacy, or secrets.
- Database schema changes, migrations, data deletion, or irreversible operations.
- Cross-cutting refactors that can affect many modules.
- Any Task where write scope, dependency order, or acceptance criteria are unclear.

## Operating Rules

- Run one role at a time.
- Run one Task or Subtask at a time.
- Do not run parallel Implementation Agents.
- Do not start Review Agent until the Implementation Agent has finished its bounded Task/Subtask and reported verification.
- Do not start the next Task/Subtask until the current one is reviewed, approved, and confirmed when confirmation is required.
- Main Codex remains responsible for sequencing, escalation, user communication, final integration, and any requested Git operation.

## Required Sequence

1. Spec Agent creates or updates the Spec.
2. User or Main Codex reviews the Spec for scope, clarity, missing requirements, and contradictions.
3. Task Agent breaks the approved Spec into Tasks and Atomic Subtasks.
4. Implementation Agent implements exactly one approved Task/Subtask.
5. Implementation Agent runs the defined local verification.
6. Review Agent reviews the completed work.
7. Implementation Agent fixes findings when required.
8. Review Agent re-reviews the fix.
9. Main Codex reports completion and waits for approval before moving forward.

## Context Loading

MAX users may keep this full document available, but the selected active work should still load only the current Spec, Task/Subtask, local `AGENTS.md`, and role-specific format files needed for the task.

Do not load Hybrid or Parallel mode files during Sequential Mode unless the user asks to compare modes.

## Stop Conditions

Stop and escalate to the user when:

- The Task/Subtask boundary is unclear.
- Required acceptance criteria are missing.
- Verification fails three consecutive times.
- Fix & Re-review repeats three consecutive times.
- The work appears to require access outside the workspace.
