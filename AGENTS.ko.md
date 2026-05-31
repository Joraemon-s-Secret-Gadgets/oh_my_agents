# AGENTS.md 한국어 설명서

이 문서는 [AGENTS.md](./AGENTS.md)의 내용을 팀원이 이해하기 쉽게 풀어쓴 한국어 설명서입니다.

`AGENTS.md`는 에이전트가 직접 따르는 실행 지침입니다. 이 파일은 그 지침이 왜 필요한지, 각 섹션이 어떤 역할을 하는지, 실제 작업에서 어떻게 적용해야 하는지를 설명합니다.

## 왜 원본은 영어로 두는가

`AGENTS.md`의 필드명과 지시문을 영어 중심으로 유지하는 이유는 다음과 같습니다.

- 에이전트가 구조화된 지시를 더 안정적으로 인식합니다.
- `Severity`, `Area`, `Evidence` 같은 리뷰 필드를 자동화나 검색에 활용하기 쉽습니다.
- 폴더별 `AGENTS.md`를 추가해도 형식을 일관되게 유지할 수 있습니다.
- 실제 설명은 한국어로 충분히 자세히 작성할 수 있으므로 팀원 이해도도 유지됩니다.

따라서 원칙은 다음과 같습니다.

- 실행 지침: `AGENTS.md`
- 팀원용 해설: `AGENTS.ko.md`
- 리뷰 결과: 필드명은 영어, 콜론 뒤 설명은 한국어

에이전트는 `AGENTS.ko.md`를 기본으로 읽을 필요가 없습니다. 한국어 설명을 요청받았거나, 한국어 문서를 수정하거나, `AGENTS.md`와 `AGENTS.ko.md`의 동기화를 확인할 때만 읽습니다. 단, 에이전트 문서를 수정하는 작업에서는 이 제한이 `File Synchronization Rule`보다 우선하지 않습니다.

## 전체 방향

이 프로젝트의 에이전트 운영 방식은 "바로 구현"이 아니라 "명확히 쪼개고, 하나씩 구현하고, 매번 리뷰하는 흐름"을 기준으로 합니다.

핵심 흐름은 다음과 같습니다.

```md
Spec 작성
-> 기능별 Task 분해
-> Task를 더 작은 Subtask로 분해
-> 하나씩 구현
-> 리뷰
-> 수정
-> 재리뷰
-> 승인
-> 다음 작업 진행
```

이 방식은 작업 규모가 커졌을 때도 사용자가 현재 진행 상황을 따라가기 쉽게 만들고, 큰 기능을 한 번에 만들어서 리뷰가 어려워지는 문제를 줄입니다.

## Execution Mode Rule

`Execution Mode Rule`은 작업을 어떤 방식으로 진행할지 정하는 규칙입니다.

복잡한 작업을 시작하기 전에는 반드시 하나의 실행 모드만 선택하고, 선택한 모드 문서만 읽습니다.

- Sequential Mode: [docs/agents/ko/modes/sequential.md](./docs/agents/ko/modes/sequential.md)
- Hybrid Mode: [docs/agents/ko/modes/hybrid.md](./docs/agents/ko/modes/hybrid.md)
- Parallel Mode: [docs/agents/ko/modes/parallel.md](./docs/agents/ko/modes/parallel.md)

에이전트가 실제로 따르는 영어 기준 문서는 다음과 같습니다.

- Sequential Mode: [docs/agents/modes/sequential.md](./docs/agents/modes/sequential.md)
- Hybrid Mode: [docs/agents/modes/hybrid.md](./docs/agents/modes/hybrid.md)
- Parallel Mode: [docs/agents/modes/parallel.md](./docs/agents/modes/parallel.md)

사용자가 별도로 지정하지 않으면 일반 기능 개발에는 `Hybrid Mode`를 사용합니다.

보안, DB, 인증, 인가, 결제, 마이그레이션, 되돌리기 어려운 작업, 요구사항이 모호한 작업에는 `Sequential Mode`를 사용합니다.

`Parallel Mode`는 사용자가 명시적으로 병렬 에이전트를 요청했거나, write scope가 명확히 분리되어 Main Codex가 결과를 안전하게 통합할 수 있을 때만 사용합니다.

토큰 비용을 줄이기 위해 모든 mode 파일을 기본으로 읽지 않습니다. 모드 비교나 모드 전환을 요청받은 경우에만 다른 mode 파일을 읽습니다.

## Instruction Priority

`Instruction Priority`는 여러 지시가 충돌할 때 무엇을 우선해야 하는지 정합니다.

우선순위는 다음과 같습니다.

1. 사용자가 직접 말한 지시
2. 보안, 워크플로우, 리뷰, Workspace Boundary 같은 프로젝트 공통 규칙은 루트 `AGENTS.md`
3. 루트 규칙을 약화하지 않는 도메인별 로컬 규칙은 현재 작업 폴더에서 가장 가까운 `AGENTS.md`
4. 에이전트의 일반 기본 동작

예를 들어 특정 기능 폴더의 `AGENTS.md`가 별도 테스트 명령을 지정할 수는 있습니다. 하지만 그 지시가 루트의 보안 규칙, 작업 흐름, 리뷰 규칙, Workspace Boundary를 약화하거나 우회할 수는 없습니다.

## Top-Level Principles

`Top-Level Principles`는 모든 역할에 공통으로 적용되는 최상위 원칙입니다.

중요한 의미는 다음과 같습니다.

- 현재 프로젝트 작업 공간 안에서만 작업합니다.
- Spec 없이 바로 구현하지 않습니다.
- 기능을 Task로 쪼개고, 큰 Task는 다시 Subtask로 쪼갭니다.
- 한 번에 하나의 Task 또는 Subtask만 구현합니다.
- 구현이 끝나면 반드시 리뷰를 거칩니다.
- 리뷰에서 문제가 나오면 수정하고 다시 리뷰합니다.
- 관련 없는 파일이나 동작을 바꾸지 않습니다.
- 속도보다 보안성, 정확성, 유지보수성을 우선합니다.
- `Implementation Agent`와 `Review Agent` 사이의 수정 및 재검토 루프가 연속 3회 이상 반복되면 즉시 중단하고 사용자에게 상황을 보고합니다.
- 기술적 한계로 더 진행하기 어렵다면 억지로 반복하지 않고 사용자 개입을 요청합니다.
- 커밋은 가능하면 `Subtask` 단위로 쪼개고, 공식 Conventional Commits 1.0.0 규격과 아래 커밋 세부 규칙을 엄격히 따릅니다.
- `.env`, `.env.local` 같은 환경 변수 파일에 있는 실제 Secret Key나 API token을 소스 코드에 하드코딩하거나 Git에 커밋하지 않습니다.
- 환경 변수 구조를 공유해야 할 때는 `.env.example`에 더미 값만 넣어 필요한 키 이름과 형식만 공유합니다.

이 원칙은 기능 개발뿐 아니라 문서, 테스트, 설정 변경에도 적용됩니다.

## Agent Progress & Handoff Rule

`Agent Progress & Handoff Rule`은 에이전트가 오래 작업하거나 막혔을 때 조용히 멈춰 있는 상황을 방지하기 위한 규칙입니다.

- Progress Update Interval: 작업이 4분 이상 이어지면 현재 역할, 진행 중인 Task/Subtask, 현재 작업, 초반 확인 내용을 짧게 보고합니다.
- No-Progress Limit: 5분 동안 의미 있는 진전이 없으면 조용히 계속 시도하지 않고 작업을 중단합니다.
- Stalled Work Handover: 무진전으로 중단하기 전에는 현재 역할, Task/Subtask, 목표, 수정한 파일, 실행한 명령, 성공한 것, 실패한 것, 현재 blocker, 계속 진행할 때의 위험, 추천 다음 행동을 요약합니다.
- Handoff Options: 사용자에게 Main Codex로 넘길지, 같은 역할의 새 에이전트를 만들지, 현재 에이전트가 제한된 범위에서 한 번 더 시도할지 선택을 요청합니다.
- Main Codex Handoff: 방향성, 요구사항, 아키텍처, 역할 간 조율, 사용자 의도 확인이 필요할 때 우선합니다.
- Same-Role Fresh Agent Handoff: Task/Subtask 범위는 명확하지만 현재 에이전트가 같은 구현, 디버깅, 리뷰 실패를 반복할 때 우선합니다.
- No Silent Retry: 같은 실패 명령, 테스트, 구현, 리뷰 루프를 보고 없이 반복하지 않습니다.

## Context Loading & Token Budget Rule

`Context Loading & Token Budget Rule`은 에이전트가 현재 역할과 Task/Subtask에 필요한 문서만 읽도록 해서 토큰 비용을 줄이기 위한 규칙입니다.

핵심은 다음과 같습니다.

- 시작할 때 `docs/agents` 전체를 읽지 않습니다.
- 현재 작업이 프롬프트 템플릿을 명시적으로 요청하지 않으면 `docs/prompts` 파일을 읽지 않습니다.
- 긴 파일은 먼저 검색하거나 필요한 섹션만 읽습니다.
- `AGENTS.ko.md`는 팀원용 설명서이므로 기본 로딩 대상이 아닙니다.
- Spec Summary는 원본이 아니라 색인으로만 사용합니다.
- Full Spec이 요구사항, acceptance criteria, API contract, data model, 보안 규칙, 사용자에게 보이는 동작의 기준입니다.
- `Implementation Agent`는 현재 Subtask 지시서를 먼저 읽고, Full Spec 전체를 기본으로 읽지 않습니다.

자세한 기준은 [docs/agents/ko/context-loading.md](./docs/agents/ko/context-loading.md)에 분리되어 있습니다.

에이전트가 실제로 따라야 하는 영어 기준 원문은 [docs/agents/context-loading.md](./docs/agents/context-loading.md)를 사용합니다.

## Git Commit Convention Details

커밋 컨벤션의 상세 설명은 [docs/agents/ko/commit-convention.md](./docs/agents/ko/commit-convention.md)에 분리되어 있습니다.

에이전트가 실제로 따라야 하는 영어 기준 원문은 [docs/agents/commit-convention.md](./docs/agents/commit-convention.md)를 사용합니다.

## Workspace Boundary

`Workspace Boundary`는 에이전트가 접근할 수 있는 파일 범위를 제한하는 규칙입니다.

허용되는 작업은 현재 프로젝트 내부에서만 가능합니다.

- 프로젝트 파일 읽기
- 승인된 작업에 필요한 파일 생성, 수정, 이동, 삭제
- 프로젝트 내부 명령 실행
- 프로젝트 내부 임시 파일, 캐시, 빌드 결과 생성

금지되는 작업은 다음과 같습니다.

- 작업 공간 밖의 파일 읽기 또는 수정
- 다른 저장소 수정
- 상위 폴더나 홈 디렉터리 접근
- 전역 설정, 셸 설정, IDE 설정, OS 설정 변경
- 승인 없이 전역 dependency 설치 또는 변경
- 프로젝트 내부에 있더라도 `.git` 내부 파일, 대용량 `.log` 파일, 빌드 결과물, 수십 MB 이상의 데이터 파일을 사용자 요청 없이 통째로 읽지 않기
- `.env`, `.env.local` 같은 실제 환경 변수 파일이 `.gitignore`에 등록되어 있는지 확인하고, `git add`나 커밋 대상에 포함되지 않도록 차단하기

이 규칙은 특히 보안과 사고 방지를 위해 중요합니다. 에이전트가 실수로 다른 프로젝트 파일이나 개인 설정 파일을 건드리지 못하게 합니다.

대용량 파일이나 관리되지 않는 파일을 확인해야 할 때는 전체 내용을 읽기보다 검색, 파일 크기 확인, 일부 구간 읽기, 요약 가능한 범위 확인을 우선합니다. 이 규칙은 토큰 초과나 프로세스 지연으로 에이전트가 먹통이 되는 상황을 줄이기 위한 것입니다.

## File-Level Agent Instructions

하위 폴더 `AGENTS.md` 작성 방식과 템플릿 설명은 [docs/agents/ko/folder-agent-templates.md](./docs/agents/ko/folder-agent-templates.md)에 분리되어 있습니다.

에이전트가 실제로 사용할 템플릿 원문은 다음 파일에 있습니다.

- General folder: [docs/agents/templates/folder-level.md](./docs/agents/templates/folder-level.md)
- Frontend React + Tailwind folder: [docs/agents/templates/frontend-react-tailwind.md](./docs/agents/templates/frontend-react-tailwind.md)
- Backend Django folder: [docs/agents/templates/backend-django.md](./docs/agents/templates/backend-django.md)

사용자가 에이전트 생성, 역할 활성화, 또는 하위 폴더 `AGENTS.md` 생성을 요청하면 [docs/agents/ko/agent-creation-guidelines.md](./docs/agents/ko/agent-creation-guidelines.md)를 참고해 생성, 이름, 도메인, focus 기준을 확인합니다. 실제 에이전트가 따르는 영어 기준 문서는 [docs/agents/agent-creation-guidelines.md](./docs/agents/agent-creation-guidelines.md)입니다.

## File Synchronization Rule

`File Synchronization Rule`은 루트 실행 지침인 `AGENTS.md`, 한국어 설명서인 `AGENTS.ko.md`, Pro/MAX용 전체 컨텍스트 파일인 `MAX/AGENTS.md`, 공유 Skill인 `skills/oh-my-agents`의 운영 규칙이 서로 어긋나지 않도록 관리하는 규칙입니다.

루트 `AGENTS.md`에 규칙을 추가, 수정, 삭제할 때는 같은 변경 사항을 `AGENTS.ko.md`에도 한국어 설명으로 함께 반영해야 합니다.

특히 에이전트 생성, 이름 규칙, 호출 입력값, handoff, context-loading, subagent orchestration 규칙이 바뀌면 `MAX/AGENTS.md`와 `skills/oh-my-agents`도 같은 방향으로 수정이 필요한지 확인해야 합니다.

즉, `AGENTS.md`는 에이전트가 따르는 원본 지침이고, `AGENTS.ko.md`는 팀원이 이해하기 위한 설명서입니다. `MAX/AGENTS.md`는 Pro/MAX 사용자가 토큰 부담 없이 한 파일로 전체 규칙을 볼 수 있는 풀 버전입니다. 표현 방식은 달라도 항상 같은 버전의 운영 규칙을 공유해야 합니다.

## Agent Roles

이 프로젝트는 4가지 역할을 사용합니다.

### Spec Agent

`Spec Agent`는 구현 전에 Kiro식 기획 자료를 준비하는 역할입니다.

주요 책임은 다음과 같습니다.

1. Requirements
   - 목표와 제외 범위를 정의합니다.
   - 사용자 또는 행위자를 식별합니다.
   - 사용자 스토리와 기대 동작을 작성합니다.
   - 성공 기준을 작성합니다.
   - 제약 조건, 엣지 케이스, 보안, 개인정보, 접근성 우려 사항을 정리합니다.

2. Design
   - 기존 시스템 맥락을 요약합니다.
   - 선택한 접근 방식을 제안합니다.
   - 영향을 받을 파일, 폴더, 모듈, API, 데이터 모델, UI 흐름을 식별합니다.
   - 에러 처리, 호환성, 마이그레이션, 테스트 전략을 정의합니다.

3. Task Preparation
   - 기능 경계를 식별합니다.
   - 의존성, 리스크, 가정, 검증 필요 사항을 정리합니다.
   - `Task Agent`가 작업을 Task와 Subtask로 나눌 수 있을 만큼 충분한 정보를 준비합니다.
   - 사용자가 검토하고 승인할 수 있도록 Spec을 이해하기 쉽게 유지합니다.
   - 구현 코드는 작성하지 않습니다.

### Task Agent

`Task Agent`는 승인된 Spec을 실제 작업 단위로 쪼개는 역할입니다.

주요 책임은 다음과 같습니다.

- Spec을 기능별 Task로 분해
- 큰 Task를 더 작은 Subtask로 분해
- 작업 순서와 의존성 정리
- 각 Task와 Subtask의 완료 기준 작성
- 각 작업이 workspace boundary를 넘지 않는지 확인

사용자가 흐름을 따라가기 쉽게 하려면 이 역할이 중요합니다. 큰 기능을 한 번에 구현하지 않고, 설명 가능한 작은 단위로 나눕니다.

### Implementation Agent

`Implementation Agent`는 승인된 Task 또는 Subtask를 구현하는 역할입니다.

주요 책임은 다음과 같습니다.

- 현재 Task 또는 Subtask만 구현
- 기존 프로젝트 구조와 패턴 준수
- 관련 없는 리팩터링 금지
- 구현 후 필요한 테스트나 확인 실행
- 리뷰 전에 변경 파일, 구현 판단, 실행한 검증, 알려진 한계 공유

이 역할은 "많이 고치는 것"보다 "정확히 필요한 만큼만 고치는 것"을 우선합니다.

### Review Agent

`Review Agent`는 구현이 다음 단계로 넘어갈 수 있는지 확인하는 역할입니다.

주요 책임은 다음과 같습니다.

- 구현이 Spec, Task, Subtask와 맞는지 확인
- 구현이 사용자의 원래 요구 목적, 의도, 성공 기준에 들어맞는지 확인
- 성공 기준이 충족됐는지 확인
- 관련 없는 동작이 바뀌지 않았는지 확인
- 테스트나 예외 처리가 부족하지 않은지 확인
- 보안에 영향을 주는 변경이 있는지 확인
- 차단 이슈가 있으면 승인하지 않고 수정을 요구

리뷰는 취향을 말하는 단계가 아니라, 요구사항과 위험을 기준으로 다음 단계 진행 가능 여부를 판단하는 단계입니다.

## End-to-End Workflow

`End-to-End Workflow`는 모든 역할을 가로지르는 전체 작업 순서만 정의합니다.

이 섹션은 의도적으로 큰 흐름만 다룹니다. Spec 작성, Task 분해, 구현, 리뷰의 세부 규칙은 아래의 역할별 Workflow에서 나누어 설명합니다.

아래 순서는 표준 lifecycle입니다. 선택된 execution mode가 이 lifecycle을 완전 순차로 실행할지, 순차-병렬 혼합으로 실행할지, 병렬 실행 후 최종 통합 게이트를 둘지 결정합니다.

핵심 순서는 다음과 같습니다.

1. 구현 전에 Spec을 작성하거나 수정합니다.
2. Spec의 범위, 명확성, 누락, 모순을 확인합니다.
3. 승인된 Spec을 기능별 Task로 변환합니다.
4. 큰 Task는 더 작은 Subtask로 나눕니다.
5. 하나의 Task 또는 Subtask만 구현합니다.
6. 완료된 Task 또는 Subtask에 필요한 로컬 검증을 실행합니다.
7. 구현 결과를 Spec, Task, 사용자 의도, 프로젝트 규칙 기준으로 리뷰합니다.
8. 문제가 있으면 수정하고 다시 리뷰합니다.
9. 리뷰 승인과 필요한 검증이 끝난 뒤에만 완료 처리합니다.
10. 필요한 승인 또는 사용자 확인 후에만 다음 Task 또는 Subtask로 이동합니다.

이렇게 나누면 전체 흐름은 유지하면서도, 특정 역할이 모든 계획을 담당하는 것처럼 보이는 문제를 줄일 수 있습니다.

## Spec Workflow

`Spec Workflow`는 `Spec Agent`가 담당합니다.

목적은 구현 전에 사용자의 의도, 제품 동작, 제약 조건, 리뷰 기준을 명확하게 만드는 것입니다.

`Spec Agent`는 이 단계에서 다음을 담당합니다.

1. 루트 `AGENTS.md`, 기존 Spec, README, 관련 코드, 사용자 지시처럼 승인된 자료를 기준으로 프로젝트 맥락을 파악합니다.
2. Requirements를 작성합니다. 여기에는 목표, 비목표, 사용자 또는 actor, 사용자 스토리, acceptance criteria, 제약 조건, edge case, 보안, 개인정보, 접근성 고려사항이 포함됩니다.
3. Design을 작성합니다. 여기에는 기존 시스템 맥락, 선택한 접근 방식, 영향을 받는 파일이나 모듈, API 또는 UI 흐름 변경, 데이터 모델 변경, 에러 처리, 호환성, 마이그레이션 필요 여부, 테스트 전략이 포함됩니다.
4. Task로 나누기 위한 준비 정보를 정리합니다. 기능 경계, 의존성, 리스크, 가정, 검증 필요 사항을 명확히 합니다.
5. 사용자가 검토하고 승인할 수 있을 정도로 Spec을 이해하기 쉽게 작성합니다.
6. `Spec Workflow` 단계에서는 구현 코드를 작성하지 않습니다.
7. 요구사항이 바뀌면 Task 분해나 구현을 계속하기 전에 Spec을 먼저 업데이트합니다.

## Task Breakdown Workflow

`Task Breakdown Workflow`는 `Task Agent`가 담당합니다.

`Task Agent`는 전체 계획을 모두 담당하는 역할이 아닙니다. 이미 승인된 Spec을 작고, 순서가 있으며, 독립적으로 리뷰 가능한 작업 단위로 바꾸는 역할입니다.

`Task Agent`는 이 단계에서 다음을 담당합니다.

1. Task를 만들기 전에 승인된 Spec을 먼저 읽습니다.
2. Spec을 기능별 Task로 나눕니다. 각 Task는 하나의 사용자 가시 기능 또는 하나의 명확한 기술 기능을 나타내야 합니다.
3. 사용자 가치, 의존성 순서, 보안 또는 정확성 리스크, 리뷰 가능성을 기준으로 Task 우선순위를 정합니다.
4. 큰 Task는 구현, 설명, 검증, 리뷰가 독립적으로 가능한 Atomic Subtask로 나눕니다.
5. 각 Subtask마다 목적, 범위, 의존성, 대상 파일, 로컬 규칙, acceptance criteria, 검증 명령어를 정의합니다.
6. UI, API, 데이터베이스, 테스트 변경을 하나의 Subtask에 섞지 않습니다. 단, 서로 강하게 결합되어 있을 때는 예외로 둘 수 있습니다.
7. 모든 Task와 Subtask가 Workspace Boundary 안에 있고 루트 보안 규칙을 약화하지 않는지 확인합니다.
8. Task 경계, 우선순위, 의존성 순서가 불명확하면 자의적으로 정하지 않고 사용자에게 질문합니다.

## Implementation & Review Workflow

`Implementation & Review Workflow`는 현재 Task 또는 Subtask가 실행 대상으로 승인된 뒤 `Implementation Agent`와 `Review Agent`가 담당합니다.

`Implementation Agent`는 이 단계에서 다음을 담당합니다.

1. 파일을 수정하기 전에 현재 진행할 Task 또는 Subtask를 요약합니다.
2. 승인된 Task 또는 Subtask만 구현합니다.
3. 변경 범위를 좁게 유지하고 관련 없는 refactor를 피합니다.
4. Task 또는 Subtask에 정의된 검증 명령이나 확인 절차를 실행합니다.
5. 변경된 파일, 구현 판단, 검증 결과, 알려진 한계를 리뷰 전에 보고합니다.

`Review Agent`는 이 단계에서 다음을 담당합니다.

1. 구현 결과가 승인된 Spec, Task, Subtask, 사용자 의도, 프로젝트 규칙에 맞는지 확인합니다.
2. 필요에 따라 정확성, edge case, 테스트 범위, 유지보수성, 접근성, 보안, Workspace Safety를 검토합니다.
3. Blocker finding이 있으면 승인하지 않고 수정을 요구합니다.
4. 수정이 필요하면 `Implementation Agent`가 수정 후 다시 리뷰를 요청해야 합니다.
5. 수정 및 재리뷰 루프가 연속 3회 반복되면 `Escalation on Deadlock` 규칙을 따릅니다.
6. Blocker finding이 없고 필요한 검증이 완료되었거나 불가능한 이유가 명확히 보고된 경우에만 Task 또는 Subtask를 승인합니다.

## Task Decomposition Rule

Task 분해 기준과 Spec/Task 작성 형식 설명은 [docs/agents/ko/spec-task-format.md](./docs/agents/ko/spec-task-format.md)에 분리되어 있습니다.

에이전트가 실제로 따라야 하는 영어 기준 원문은 [docs/agents/spec-task-format.md](./docs/agents/spec-task-format.md)를 사용합니다.

Subtask를 구현용 문맥 packet으로 작성하는 방식과 Spec Summary를 색인으로만 사용하는 방식은 [docs/agents/ko/context-loading.md](./docs/agents/ko/context-loading.md)에 분리되어 있습니다.

## Task Completion & Handover Rule

`Task Completion & Handover Rule`은 큰 틀의 Task가 끝났을 때 에이전트가 자의적으로 다음 작업으로 넘어가지 않도록 막는 규칙입니다.

상위 Task가 완료되면 에이전트는 다음 Task를 바로 시작하지 않고, 먼저 두 가지 산출물을 만들어야 합니다.

- 사용자 보고용: `docs/reports/TASK[번호]_COMPLETION.md`
- 에이전트 전달용 다음 작업 지시서: `docs/specs/TASK[다음번호]_SUBTASKS.md`

사용자 보고용 문서에는 완료된 내용, 변경된 내용, 실행한 검증, 남은 위험, 사용자 판단이 필요한 사항을 정리합니다.

사용자 보고용 문서에는 다음 항목을 포함합니다.

- 완료 일시
- 담당 에이전트
- 기획 대비 달성도, 즉 Spec Alignment 체크리스트
- 변경된 파일 및 핵심 구현 요약
- Lint, Unit Test 등 실행한 테스트와 검증 결과 또는 해당 없음의 사유
- 사용자 확인 필요 사항

다음 작업 지시서에는 다음 Task를 Subtask 단위로 나누고, 각 Subtask의 목적, 범위, 의존성, 완료 기준, 검증 방법을 적습니다.

다음 작업 지시서에는 다음 항목을 포함합니다.

- 이전 Task 리포트와 베이스 브랜치를 포함한 컨텍스트 및 의존성
- 실행 순서대로 정리된 Atomic Subtask 목록
- 각 Subtask별 목적, 대상 파일, 로컬 규칙, 완료 조건, 검증 명령어
- 테스트 3회 연속 실패 또는 리뷰 교착 반복 시 즉시 중단하고 사용자에게 에스컬레이션하는 탈출 조건

이 두 산출물을 만든 뒤에는 사용자의 검토 또는 승인을 기다리고, 승인 없이 다음 상위 Task를 시작하지 않습니다.

## Task Startup Rule

`Task Startup Rule`은 새로운 상위 Task를 시작할 때 따라야 하는 규칙입니다.

에이전트는 새 상위 Task를 시작하기 전에 먼저 `docs/specs/TASK[번호]_SUBTASKS.md` 파일을 읽고, 첫 번째 Subtask의 목적과 변경 대상 파일을 사용자에게 요약해야 합니다.

Subtask는 문서에 적힌 순서대로 진행합니다.

각 Subtask를 구현하고 로컬 검증을 마친 뒤에는 검증 결과를 보고하고, 사용자의 컨펌을 받은 후에만 다음 Subtask로 넘어갑니다.

테스트가 3회 연속 실패하거나, 방향성이 모호해지거나, 리뷰 교착 상태가 반복되면 즉시 중단하고 사용자에게 질문해야 합니다.

## Spec Format

Spec 작성 형식은 [docs/agents/ko/spec-task-format.md](./docs/agents/ko/spec-task-format.md)에 분리되어 있습니다.

## Task Format

Task와 Subtask 작성 형식은 [docs/agents/ko/spec-task-format.md](./docs/agents/ko/spec-task-format.md)에 분리되어 있습니다.

## Review Input Requirements

리뷰 입력 요구사항은 [docs/agents/ko/review-format.md](./docs/agents/ko/review-format.md)에 분리되어 있습니다.

에이전트가 실제로 따라야 하는 영어 기준 원문은 [docs/agents/review-format.md](./docs/agents/review-format.md)를 사용합니다.

## Review Output Format

리뷰 결과 형식은 [docs/agents/ko/review-format.md](./docs/agents/ko/review-format.md)에 분리되어 있습니다.

## Severity 기준

Severity 기준은 [docs/agents/ko/review-format.md](./docs/agents/ko/review-format.md)에 분리되어 있습니다.

## Security Review Checklist

보안 리뷰 체크리스트 설명은 [docs/agents/ko/security-review-checklist.md](./docs/agents/ko/security-review-checklist.md)에 분리되어 있습니다.

에이전트가 실제로 따라야 하는 영어 기준 원문은 [docs/agents/security-review-checklist.md](./docs/agents/security-review-checklist.md)를 사용합니다.

## Completion Rules

작업 완료는 코드 작성이 끝났다는 뜻이 아닙니다.

완료로 인정하려면 다음 조건을 만족해야 합니다.

- 구현이 승인된 Spec과 일치합니다.
- Acceptance Criteria가 충족됐습니다.
- Review Agent가 `Blocker` 이슈를 발견하지 않았습니다.
- 필요한 경우 보안 리뷰가 완료됐습니다.
- 관련 테스트, 점검, 수동 확인이 실행됐습니다.
- 사용자가 무엇이 바뀌었고 왜 바뀌었는지 이해할 수 있습니다.

이 기준을 두면 "일단 만들었다"가 아니라 "검증 가능한 단위로 완료했다"는 흐름을 유지할 수 있습니다.

## 팀 운영 팁

새 기능을 시작할 때는 먼저 Spec을 짧게라도 작성합니다.

기능이 커 보이면 바로 구현하지 말고 Task와 Subtask로 나눕니다.

리뷰 결과는 항상 같은 형식을 사용합니다.

```md
- Severity:
- Area:
- Evidence:
- Risk:
- Required Fix:
- Retest:
```

폴더가 커져서 책임이 분명해지면 그때 해당 폴더에 별도 `AGENTS.md`를 추가합니다.

루트 `AGENTS.md`는 공통 원칙, 폴더별 `AGENTS.md`는 로컬 규칙만 담당하게 유지합니다.
