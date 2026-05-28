## Task Decomposition Rule

Feature work should be decomposed so the user can follow progress without needing to understand a large implementation all at once.

For context-loading, Spec Summary, and Subtask context-packet rules, also follow `docs/agents/context-loading.md`.

Use this hierarchy:

```md
Spec
-> Feature Task
-> Subtask
-> Implementation Step
-> Review
-> Fix
-> Re-review
-> Approval
```

Guidelines:

- A Feature Task should represent one user-visible capability or one clear technical capability.
- A Subtask should be small enough to implement, explain, and review independently.
- A Subtask should have clear inputs, outputs, and completion criteria.
- A Subtask should avoid mixing UI, API, database, and test changes unless they are tightly coupled.
- If a Subtask feels hard to explain in a few sentences, split it again.
- Do not start implementation until the current Task or Subtask is clear.

## Spec Format

Specs should be written clearly enough for both the user and agents to follow.

Recommended Spec sections:

- Summary: What is being built and why.
- Goals: What this work must accomplish.
- Non-Goals: What this work intentionally does not include.
- User Flow: How the user or system moves through the feature.
- Requirements: Functional requirements.
- Acceptance Criteria: Conditions that must be true for approval.
- Constraints: Technical, product, security, or workspace limits.
- Risks: Known risks and assumptions.
- Task Breakdown: Feature Tasks and Subtasks.
- Verification: Tests, checks, or manual validation required.

## Task Format

Tasks and Subtasks should use this format:

```md
### Task: [short English or Korean title]

- Purpose: 이 작업이 필요한 이유를 한글로 설명합니다.
- Scope: 이 작업에서 수정할 범위와 제외할 범위를 한글로 설명합니다.
- Dependencies: 먼저 완료되어야 하는 작업을 적습니다.
- Context Budget: 반드시 읽을 문서, 읽지 말아야 할 문서, 조건부로 읽을 문서를 적습니다.
- Acceptance Criteria: 완료로 판단할 수 있는 기준을 한글로 구체적으로 적습니다.
- Verification: 실행할 테스트, 빌드, 린트, 수동 확인 방법을 적습니다.
```

For implementation-ready Subtasks, include `Required Context`, `Context Budget`, `Source of Truth`, `Required Sections`, `Must Read Before Implementation`, `Target Files`, and `Out of Scope` as defined in `docs/agents/context-loading.md`.
