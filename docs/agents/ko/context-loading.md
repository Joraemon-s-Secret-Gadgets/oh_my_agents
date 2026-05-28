## Context Loading & Token Budget Rule

에이전트는 현재 역할과 Task/Subtask에 필요한 문맥만 읽어서 토큰 비용을 줄여야 합니다.

기본 로딩 규칙은 다음과 같습니다.

- 루트 `AGENTS.md`와 현재 작업 파일에 가장 가까운 관련 하위 `AGENTS.md`만 읽습니다.
- `AGENTS.ko.md`는 기본으로 읽지 않습니다. 사용자가 한국어 설명을 요청하거나, 한국어 문서를 수정하거나, `AGENTS.md`와 `AGENTS.ko.md`의 동기화를 확인하는 작업일 때만 읽습니다. 단, 에이전트 문서를 수정하는 작업에서는 이 제한이 `File Synchronization Rule`보다 우선하지 않습니다.
- 시작할 때 `docs/agents` 전체를 한 번에 읽지 않습니다.
- 현재 작업이 프롬프트 템플릿을 명시적으로 요청하지 않으면 `docs/prompts` 파일을 읽지 않습니다.
- 긴 파일을 열기 전에 `rg` 또는 섹션 단위 읽기로 필요한 부분을 먼저 찾습니다.
- 전체 문서를 통째로 읽기보다 참조된 섹션, 짧은 Subtask packet, 현재 변경 파일을 우선합니다.

## Role-Based Loading

`Spec Agent`가 읽어야 하는 것은 다음과 같습니다.

- 루트 `AGENTS.md`
- 사용자 요청과 관련 제품 맥락
- 현재 Spec 작성에 필요한 기존 Spec 또는 소스 섹션
- Spec 또는 Task 관련 섹션을 작성할 때 `docs/agents/spec-task-format.md`

`Task Agent`가 읽어야 하는 것은 다음과 같습니다.

- 루트 `AGENTS.md`
- 승인된 Full Spec 또는 필요한 Full Spec 섹션
- 기존 Spec Summary가 있으면 해당 Summary
- `docs/agents/spec-task-format.md`
- Implementation Agent에게 넘길 Subtask를 작성할 때 이 파일

`Implementation Agent`가 읽어야 하는 것은 다음과 같습니다.

- 루트 `AGENTS.md`
- 대상 파일에 관련된 하위 `AGENTS.md`가 있으면 해당 파일
- 현재 Subtask 지시서
- `Must Read Before Implementation`에 명시된 Full Spec 섹션
- Subtask 문맥이 부족할 때만 추가로 참조된 Full Spec 섹션

`Review Agent`가 읽어야 하는 것은 다음과 같습니다.

- 루트 `AGENTS.md`
- 현재 Subtask 지시서
- 변경된 파일
- 동작 검증에 필요한 acceptance criteria와 관련 Full Spec 섹션
- `docs/agents/review-format.md`
- 루트 보안 규칙상 보안 민감 변경일 때만 `docs/agents/security-review-checklist.md`

## Spec Summary Rule

Spec Summary는 색인이지 Full Spec의 대체본이 아닙니다.

- Spec Summary를 authoritative한 기준으로 취급하지 않습니다.
- 요구사항, acceptance criteria, API contract, data model, 보안 규칙, 사용자에게 보이는 동작의 기준은 Full Spec입니다.
- Spec Summary는 에이전트가 관련 Full Spec 섹션을 빨리 찾도록 돕는 용도로 사용합니다.
- Spec Summary에는 topic별로 full, partial, not covered 같은 coverage 상태를 표시하는 것이 좋습니다.

권장 Spec Summary 형식은 다음과 같습니다.

```md
# Spec Summary: [feature name]

This summary is not authoritative. Use it only to find relevant Full Spec sections.

## Source of Truth

- Full Spec: `docs/specs/[FEATURE]_SPEC.md`

## Section Map

- User flow: `#user-flow`
- Theme selection: `#theme-selection`
- API contract: `#api-contract`
- Security requirements: `#security`
- Acceptance criteria: `#acceptance-criteria`

## Coverage

- Theme selection: full
- Recommendation ranking: partial
- Community review: not covered
```

## Subtask Context Packet Rule

`Task Agent`는 `Implementation Agent`가 Full Spec 전체를 읽지 않아도 현재 Subtask를 이해할 수 있도록 각 Subtask를 작성해야 합니다.

각 Subtask에는 다음 항목을 포함하는 것이 좋습니다.

- Purpose
- Required Context
- Context Budget
- Source of Truth
- Required Sections
- Must Read Before Implementation
- Target Files
- Out of Scope
- Acceptance Criteria
- Verification

권장 Subtask 형식은 다음과 같습니다.

```md
### Subtask [number]: [title]

- Purpose: 이 작업이 필요한 이유를 한글로 설명합니다.
- Required Context:
  - 이 Subtask 구현에 반드시 필요한 Spec 맥락만 적습니다.
- Context Budget:
  - Must read:
  - Do not read:
  - Optional read:
- Source of Truth:
  - Full Spec: `docs/specs/[FEATURE]_SPEC.md`
- Required Sections:
  - `#relevant-section`
  - `#acceptance-criteria`
- Must Read Before Implementation:
  - `#relevant-section`
  - `#acceptance-criteria`
- Target Files:
  - `path/to/file`
- Out of Scope:
  - 이번 Subtask에서 구현하지 않을 범위를 적습니다.
- Acceptance Criteria:
  - 완료로 판단할 수 있는 기준을 원문 의미가 손상되지 않게 적습니다.
- Verification:
  - 실행할 테스트, 빌드, 린트, 수동 확인 방법을 적습니다.
```

## Implementation Spec Reading Rule

`Implementation Agent`는 기본적으로 Full Spec 전체를 읽지 않습니다.

`Implementation Agent`는 다음 순서를 따릅니다.

1. 현재 Subtask 지시서를 먼저 읽습니다.
2. `Must Read Before Implementation`에 적힌 모든 섹션을 읽습니다.
3. Subtask 문맥이 부족할 때만 추가로 참조된 Full Spec 섹션을 읽습니다.
4. Subtask, 참조된 Spec 섹션, acceptance criteria가 충돌하면 작업을 멈추고 사용자에게 질문합니다.

다음 변경을 할 때는 관련 Full Spec 섹션을 반드시 읽어야 합니다.

- 사용자에게 보이는 동작
- Acceptance criteria
- API contract
- Data model 또는 migration
- Authentication 또는 authorization
- Security, privacy, sensitive data
- External API 또는 file handling

## Review Spec Reading Rule

`Review Agent`는 Spec Summary만 기준으로 삼지 않고 관련 Full Spec 섹션과 대조해야 합니다.

`Review Agent`는 다음을 수행해야 합니다.

- 구현 결과를 현재 Subtask의 acceptance criteria와 비교합니다.
- 사용자에게 보이는 동작, API contract, data model, 보안 민감 변경, acceptance criteria에 대해서는 참조된 Full Spec 섹션을 읽습니다.
- Spec reference가 빠져 있거나 모호하면 review finding 또는 escalation point로 처리합니다.
