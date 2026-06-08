# oh_my_agents Project Guide

This repository contains project agent instructions, role rules, execution modes, and reusable prompts for working with `AGENTS.md`.

## Important: AGENTS.md Is Not a Harness

`AGENTS.md` is a rulebook. It defines how agents should plan, implement, review, secure, and hand off work.

`AGENTS.md` does not automatically create, run, or manage independent subagents by itself.

To actually create or delegate work to role agents such as `Spec Agent`, `Task Agent`, `Implementation Agent`, `Review Agent`, `Frontend QA Review Agent`, or `Backend Security Review Agent`, you need a supported agent harness.

Examples of a harness include:

- A Codex Skill such as `oh-my-agents` that can parse the user request and prepare a bounded agent invocation.
- A tool-backed subagent system that can create separate agent contexts, pass scoped instructions, collect final reports, and clean up unused agents.
- A custom orchestration script or service that reads these rules and enforces role, scope, verification, and handoff contracts.

If no supported harness is available, the current Codex session can still follow the role rules through role activation, but it is not the same as spawning an independent subagent.

## Default Execution Mode

Using `oh-my-agents` does not mean work defaults to Sequential Mode.

The default mode rules are:

- `Hybrid Mode`: default for ordinary feature work.
- `Sequential Mode`: use for security-sensitive, database, authentication, authorization, payment, migration, irreversible, or ambiguous work.
- `Parallel Mode`: use only when explicitly requested or when write scopes are clearly separated and the results can be safely integrated.

## Recommended Flow

1. Read the root `AGENTS.md`.
2. If creating or activating an agent role, read `docs/agents/agent-creation-guidelines.md`.
3. Preserve the user's original request as `User Request Original`.
4. Convert executable instructions into an English `Structured Agent Contract`.
5. Select one execution mode.
6. Run only the selected role, domain, and focus rules.
7. Collect the agent's final report.
8. Clean up unused or unresponsive agent contexts when the harness supports it.

## Key Files

- `AGENTS.md`: root project agent rules.
- `AGENTS.ko.md`: Korean teammate-facing explanation.
- `PRO20x/AGENTS.md`: full-context version for PRO20x users.
- `docs/agents/`: split, token-optimized agent rule files.
- `docs/agents/modes/`: Sequential, Hybrid, and Parallel execution modes.
- `docs/prompts/`: task-specific prompt templates such as crawl prompts.
- `skills/oh-my-agents/`: shared Skill package for agent routing and invocation support.

## Codex Skill Installation

Team members can install the shared Skill into their local Codex Skill folder.

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

If it is already installed, replace the local copy when updating.

```bash
rm -rf ~/.codex/skills/oh-my-agents
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

In a new Codex session, use `$oh-my-agents` to standardize Spec, Task, Implementation, and Review agent routing based on the project `AGENTS.md`.

## Team Usage Note

When asking for an agent, include the role, goal, source of truth, scope, out-of-scope behavior, verification command, and expected output format whenever possible.

If those fields are missing, the agent or harness should ask concise clarification questions instead of guessing.
