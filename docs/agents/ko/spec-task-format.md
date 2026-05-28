## Task Decomposition Rule

`Task Decomposition Rule`은 작업을 얼마나 잘게 나눌지에 대한 기준입니다.

Context loading, Spec Summary, Subtask context packet 규칙은 [context-loading.md](./context-loading.md)도 함께 따릅니다.

권장 구조는 다음과 같습니다.

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

예를 들어 "로그인 기능"이라는 큰 기능이 있다면 한 번에 만들지 않고 다음처럼 나눌 수 있습니다.

```md
Feature Task: 로그인 기능
-> Subtask: 로그인 UI 작성
-> Subtask: 로그인 API 연결
-> Subtask: 세션 저장 처리
-> Subtask: 에러 메시지 처리
-> Subtask: 로그인 상태 테스트
```

각 Subtask는 독립적으로 설명, 구현, 리뷰할 수 있어야 합니다.

Subtask가 몇 문장으로 설명하기 어렵다면 아직 너무 큰 작업일 가능성이 높습니다.

## Spec Format

`Spec Format`은 Spec 문서에 들어가야 하는 권장 섹션입니다.

각 항목의 의미는 다음과 같습니다.

- Summary: 무엇을 왜 만드는지 설명합니다.
- Goals: 반드시 달성해야 하는 목표를 적습니다.
- Non-Goals: 이번 작업에서 하지 않을 것을 명확히 적습니다.
- User Flow: 사용자나 시스템이 어떤 순서로 움직이는지 설명합니다.
- Requirements: 기능 요구사항을 적습니다.
- Acceptance Criteria: 완료로 인정할 기준을 적습니다.
- Constraints: 기술, 제품, 보안, 작업 공간 제한을 적습니다.
- Risks: 알려진 위험과 가정을 적습니다.
- Task Breakdown: 기능별 Task와 Subtask를 적습니다.
- Verification: 테스트, 점검, 수동 확인 방법을 적습니다.

Spec은 구현자를 위한 문서이기도 하지만, 사용자가 현재 범위를 이해하기 위한 문서이기도 합니다.

## Task Format

`Task Format`은 각 Task와 Subtask를 작성할 때 사용할 형식입니다.

각 필드의 의미는 다음과 같습니다.

- Purpose: 이 작업이 왜 필요한지 설명합니다.
- Scope: 어디까지 수정하고 어디부터는 제외하는지 설명합니다.
- Dependencies: 먼저 완료되어야 하는 작업을 적습니다.
- Context Budget: 반드시 읽을 문서, 읽지 말아야 할 문서, 조건부로 읽을 문서를 적습니다.
- Acceptance Criteria: 완료로 판단할 수 있는 구체적 기준을 적습니다.
- Verification: 어떤 테스트나 확인을 실행해야 하는지 적습니다.

이 형식을 사용하면 작업이 막연해지는 것을 줄일 수 있습니다.

구현용 Subtask에는 [context-loading.md](./context-loading.md)에 정의된 `Required Context`, `Context Budget`, `Source of Truth`, `Required Sections`, `Must Read Before Implementation`, `Target Files`, `Out of Scope`도 함께 포함하는 것이 좋습니다.
