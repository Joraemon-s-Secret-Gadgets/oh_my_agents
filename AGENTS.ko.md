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

## Git Commit Convention Details

`Git Commit Convention Details`는 커밋 메시지를 작성할 때 따르는 세부 규칙입니다.

공식 기준은 Conventional Commits 1.0.0입니다.

공식 문서: https://www.conventionalcommits.org/en/v1.0.0/

기본 구조는 다음과 같습니다.

```md
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

작성 규칙은 다음과 같습니다.

- 각 커밋은 가능하면 하나의 완료된 `Subtask`에 대응해야 합니다.
- 커밋 메시지는 반드시 `type`으로 시작합니다.
- `feat`는 새로운 기능 추가에 사용하며 Semantic Versioning의 MINOR 변경과 연결됩니다.
- `fix`는 버그 수정에 사용하며 Semantic Versioning의 PATCH 변경과 연결됩니다.
- 그 외에 `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build` 등을 변경 성격에 맞게 사용할 수 있습니다.
- `scope`는 선택 사항이며 변경이 일어난 모듈이나 위치를 소괄호 안에 적습니다. 예: `feat(auth):`, `fix(api):`
- `description`은 type 또는 scope 뒤의 콜론과 공백 다음에 바로 작성합니다.
- `description`은 간결한 한 줄 요약이어야 하며, 대문자로 시작하지 않고 마침표로 끝나지 않아야 합니다.
- 추가 설명이 필요하면 한 줄을 비운 뒤 body를 작성할 수 있습니다.
- footer는 한 줄을 비운 뒤 git trailer 형식으로 작성합니다.
- 하위 호환성이 깨지는 변경은 `feat!:` 또는 `feat(api)!:`처럼 type 또는 scope 뒤에 `!`를 붙이거나, footer에 `BREAKING CHANGE:`를 반드시 명시합니다.
- footer token으로 사용할 때 `BREAKING CHANGE`는 반드시 대문자로 작성합니다.

예시는 다음과 같습니다.

```md
feat(auth): add session refresh flow
fix(api): handle missing project id
docs(agents): document folder-level inheritance
refactor(tasks): split handover template generation
test(auth): add expired token coverage
feat(api)!: change project response format

BREAKING CHANGE: project responses now wrap data in a result object
```

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

프로젝트가 커지면 기능 폴더마다 별도 `AGENTS.md`를 둘 수 있습니다.

다만 모든 폴더에 무조건 만들 필요는 없습니다. 책임이 분명한 기능, 모듈, 도메인 폴더에만 추가하는 것이 좋습니다.

폴더별 `AGENTS.md`에는 다음처럼 해당 폴더에만 적용되는 내용을 적습니다.

- 이 폴더의 목적
- 이 폴더가 소유하는 파일과 책임
- 이 폴더에서 허용되는 변경
- 이 폴더에서 금지되는 변경
- 로컬 아키텍처 규칙
- 로컬 테스트 방식
- 이 폴더의 주요 Agent 역할

공통 규칙을 폴더마다 복사하지 않는 것이 중요합니다. 공통 규칙은 루트 `AGENTS.md`에만 두고, 폴더별 문서에는 차이점만 적어야 나중에 규칙이 어긋나지 않습니다.

상속 원칙은 다음과 같습니다.

- 하위 폴더의 `AGENTS.md`는 해당 도메인의 특화된 로컬 규칙만 다룹니다.
- 하위 폴더 규칙은 루트의 보안, 계획, 리뷰, 환경 변수, Workspace Boundary 규칙을 약화하거나 무력화할 수 없습니다.
- 하위 폴더 규칙과 루트 규칙이 충돌하면 루트 규칙이 우선합니다.

실행 경로 기준은 다음과 같습니다.

- 에이전트는 원칙적으로 프로젝트 최상위 루트에서 실행됩니다.
- 하위 폴더로 이동해서 명령을 실행하더라도 루트의 보안 및 Workspace Boundary 규칙을 지켜야 합니다.
- 하위 폴더 실행을 workspace boundary 밖 파일, 명령, dependency에 접근하는 방식으로 사용해서는 안 됩니다.

하위 폴더용 `AGENTS.md` 템플릿은 다음과 같습니다.

````md
# AGENTS.md

This file defines local agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, or Workspace Boundary rules.

## Folder Purpose

- Describe the domain, feature, or module owned by this folder.

## Ownership Scope

- Owned files:
- Related files outside this folder:
- Explicitly out of scope:

## Local Rules

- Add folder-specific architecture, naming, dependency, or design rules.
- Do not repeat root-level rules unless a short reminder prevents misuse.

## Allowed Changes

- List changes agents may make in this folder.

## Forbidden Changes

- List folder-specific changes agents must not make.
- Do not weaken root-level forbidden actions.

## Local Verification

- List tests, checks, or manual verification required for this folder.

## Primary Agent Roles

- Primary:
- Review:
- Security-sensitive areas:

## Handover Notes

- Note local assumptions, known risks, or follow-up requirements for the next agent.
````

### Frontend React + Tailwind Folder-Level `AGENTS.md` Template

프론트엔드 루트 폴더인 `frontend/AGENTS.md` 또는 프론트엔드 기능 폴더용 `AGENTS.md`를 만들 때 사용하는 템플릿입니다.

````md
# AGENTS.md

This file defines local frontend agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

## Agent Focus

This folder is frontend-focused.
Agents working here must prioritize React component structure, user-facing behavior, UI state, accessibility, API integration, and TailwindCSS consistency.

## Project Stack

- Framework: React
- Styling: TailwindCSS
- Language: Use the project's existing JavaScript or TypeScript choice.
- Package Manager: Detect from lockfile before running commands.

## Folder Purpose

- Describe the frontend domain, feature, route, or UI module owned by this folder.

## Ownership Scope

- Owned files:
- Related backend/API contracts:
- Explicitly out of scope:

## Local Rules

- Follow existing React component patterns.
- Prefer small, focused components with clear props.
- Keep UI state local unless shared state is clearly required.
- Handle loading, error, empty, and success states.
- Treat client-side validation as UX support only; backend validation remains required.
- Do not expose server-only environment variables or secrets to client-side code.
- Use Tailwind utility classes consistently with existing design tokens and layout patterns.
- Avoid introducing a component library, state library, or styling framework unless explicitly approved.
- Preserve accessibility with semantic HTML, labels, focus states, keyboard navigation, and readable error text.

## Allowed Changes

- React components, hooks, client utilities, route/view files, styles, tests, and frontend documentation within this folder's scope.

## Forbidden Changes

- Do not change backend API behavior from frontend folders.
- Do not hardcode API secrets, tokens, or server-only environment variables.
- Do not bypass root security, environment, or Workspace Boundary rules.
- Do not introduce new global styling conventions without approval.

## Local Verification

- Use project-defined frontend commands when available.
- If commands are unknown, inspect package scripts before running tests.
- Suggested checks once configured:
  - frontend lint
  - frontend unit/component tests
  - frontend build
  - manual UI state and accessibility check

## Primary Agent Roles

- Primary: Implementation Agent for frontend Tasks and Subtasks.
- Review: Review Agent with frontend UX, accessibility, state, and API-integration focus.
- Security-sensitive areas: client environment variables, auth UI, token handling, forms, redirects, user-generated content.

## Handover Notes

- Document API assumptions, unverified UI states, accessibility gaps, and any required backend coordination.
````

### Backend Django Folder-Level `AGENTS.md` Template

백엔드 루트 폴더인 `backend/AGENTS.md` 또는 Django app/module 폴더용 `AGENTS.md`를 만들 때 사용하는 템플릿입니다.

````md
# AGENTS.md

This file defines local backend agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

## Agent Focus

This folder is backend-focused.
Agents working here must prioritize Django app boundaries, API contracts, validation, authentication, authorization, data integrity, error handling, observability, and server-side security.

## Project Stack

- Framework: Django
- API Layer: Use the project's existing Django API pattern, such as Django REST Framework if already present.
- Database: Use the configured project database.
- Package Manager: Detect from project files before running commands.

## Folder Purpose

- Describe the backend domain, Django app, API area, or service module owned by this folder.

## Ownership Scope

- Owned files:
- Related frontend/API consumers:
- Explicitly out of scope:

## Local Rules

- Follow Django app boundaries and existing project structure.
- Keep business logic out of views when it grows; prefer services, selectors, forms, serializers, managers, or existing local patterns.
- Validate all user input server-side.
- Enforce authentication and authorization server-side.
- Never log passwords, tokens, API keys, secrets, or sensitive user data.
- Use Django migrations for model changes and review migrations before applying them.
- Use Django settings and environment variables safely; never hardcode secrets in settings or source code.
- Use Django's built-in password hashing and security mechanisms.
- Consider rate limiting or abuse protection for authentication-sensitive or costly endpoints.
- Return consistent error responses without leaking stack traces or internal details.

## Allowed Changes

- Django apps, models, migrations, views, serializers/forms, services, selectors, permissions, tests, and backend documentation within this folder's scope.

## Forbidden Changes

- Do not change frontend behavior from backend folders unless explicitly scoped.
- Do not bypass authentication, authorization, validation, or migration review.
- Do not commit real `.env` files, credentials, local databases, or generated secrets.
- Do not weaken root security, environment, or Workspace Boundary rules.

## Local Verification

- Use project-defined backend commands when available.
- If commands are unknown, inspect project scripts or Django management configuration before running tests.
- Suggested checks once configured:
  - backend lint
  - Django system checks
  - migrations check
  - backend unit/API tests
  - security-sensitive manual checks for auth, permissions, and validation

## Primary Agent Roles

- Primary: Implementation Agent for backend Tasks and Subtasks.
- Review: Review Agent with backend correctness, API contract, data integrity, and security focus.
- Security-sensitive areas: settings, environment variables, authentication, authorization, permissions, password handling, tokens, sessions, migrations, file access, external APIs.

## Handover Notes

- Document API contracts, migration status, auth/permission assumptions, unverified edge cases, and required frontend coordination.
````

역할별 하위 `AGENTS.md` 생성은 이렇게 요청하면 됩니다.

```md
frontend/AGENTS.md를 생성해줘.
루트 AGENTS.md의 Frontend React + Tailwind Folder-Level Template을 기반으로 작성하고,
frontend 영역의 로컬 규칙만 포함해줘.
루트 보안, 워크플로우, 환경 변수, Workspace Boundary 규칙은 약화하지 마.
```

```md
backend/AGENTS.md를 생성해줘.
루트 AGENTS.md의 Backend Django Folder-Level Template을 기반으로 작성하고,
backend 영역의 로컬 규칙만 포함해줘.
루트 보안, 워크플로우, 환경 변수, Workspace Boundary 규칙은 약화하지 마.
```

기능별로 더 내려갈 때는 이렇게 요청합니다.

```md
frontend/src/features/auth/AGENTS.md를 생성해줘.
Frontend React + Tailwind 템플릿을 기반으로 auth 프론트엔드 규칙만 작성해줘.
```

```md
backend/src/modules/auth/AGENTS.md를 생성해줘.
Backend Django 템플릿을 기반으로 auth 백엔드 규칙만 작성해줘.
```

## File Synchronization Rule

`File Synchronization Rule`은 루트 실행 지침인 `AGENTS.md`와 한국어 설명서인 `AGENTS.ko.md`의 내용이 서로 어긋나지 않도록 관리하는 규칙입니다.

루트 `AGENTS.md`에 규칙을 추가, 수정, 삭제할 때는 같은 변경 사항을 `AGENTS.ko.md`에도 한국어 설명으로 함께 반영해야 합니다.

즉, `AGENTS.md`는 에이전트가 따르는 원본 지침이고, `AGENTS.ko.md`는 팀원이 이해하기 위한 설명서입니다. 두 파일은 표현 방식은 달라도 항상 같은 버전의 운영 규칙을 공유해야 합니다.

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
- 성공 기준이 충족됐는지 확인
- 관련 없는 동작이 바뀌지 않았는지 확인
- 테스트나 예외 처리가 부족하지 않은지 확인
- 보안에 영향을 주는 변경이 있는지 확인
- 차단 이슈가 있으면 승인하지 않고 수정을 요구

리뷰는 취향을 말하는 단계가 아니라, 요구사항과 위험을 기준으로 다음 단계 진행 가능 여부를 판단하는 단계입니다.

## Planning Workflow

`Planning Workflow`는 작업의 전체 순서를 정의합니다.

핵심은 다음과 같습니다.

1. 먼저 Spec을 작성하거나 수정합니다.
2. Spec의 범위, 명확성, 누락, 모순을 확인합니다.
3. Spec을 기능별 Task로 나눕니다.
4. 큰 Task는 더 작은 Subtask로 나눕니다.
5. 하나의 Task 또는 Subtask만 구현합니다.
6. 구현된 작업을 리뷰합니다.
7. 문제가 있으면 수정하고 다시 리뷰합니다.
8. 승인된 후에만 완료 처리합니다.
9. 다음 Task 또는 Subtask로 이동합니다.

이 흐름은 작업을 작게 유지하고, 리뷰 가능한 단위로 진행하기 위한 규칙입니다.

## Task Decomposition Rule

`Task Decomposition Rule`은 작업을 얼마나 잘게 나눌지에 대한 기준입니다.

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
- Acceptance Criteria: 완료로 판단할 수 있는 구체적 기준을 적습니다.
- Verification: 어떤 테스트나 확인을 실행해야 하는지 적습니다.

이 형식을 사용하면 작업이 막연해지는 것을 줄일 수 있습니다.

## Review Input Requirements

리뷰 전에 `Implementation Agent`는 `Review Agent`에게 충분한 정보를 제공해야 합니다.

필요한 정보는 다음과 같습니다.

- 승인된 Spec
- 현재 Task 또는 Subtask 설명
- 성공 기준
- 변경된 파일 목록
- 구현 판단 요약
- 실행한 테스트나 확인
- 알려진 한계나 가정
- 보안, 데이터, 인증, 권한, 파일, dependency, 외부 API 영향 여부

리뷰어가 코드를 처음부터 추측하지 않도록, 구현자가 맥락을 먼저 제공하는 것이 목적입니다.

## Review Output Format

리뷰 결과는 구조를 고정합니다.

필드명과 카테고리는 영어로 작성합니다.
콜론 뒤 설명은 한국어로 자세히 작성합니다.

예시는 다음과 같습니다.

```md
- Severity: Major
- Area: Access Control
- Evidence: `src/api/projects/[id]/route.ts`에서 요청 사용자가 해당 프로젝트의 멤버인지 확인하지 않고 데이터를 반환하고 있습니다.
- Risk: 로그인한 사용자가 프로젝트 ID만 바꿔 다른 사용자의 프로젝트 정보를 조회할 수 있습니다.
- Required Fix: 프로젝트 조회 전에 현재 사용자 ID와 프로젝트 멤버십을 서버에서 검증해야 합니다.
- Retest: 권한이 없는 프로젝트 ID로 요청했을 때 403이 반환되고, 정상 멤버 요청은 성공하는지 확인합니다.
```

이 방식은 사람이 읽기 쉽고, 나중에 자동화나 검색에도 유리합니다.

## Severity 기준

`Severity`는 리뷰 이슈의 심각도를 나타냅니다.

- Blocker: 반드시 수정해야 하며, 수정 전에는 완료할 수 없습니다.
- Major: 수정하는 것이 원칙이며, 미수정 시 명확한 이유가 필요합니다.
- Minor: 완료를 막지는 않지만 개선하는 것이 좋습니다.
- Approved: 차단 이슈가 없어 다음 단계로 넘어갈 수 있습니다.

보안 문제, 데이터 노출, 권한 우회, workspace 밖 접근은 보통 `Blocker`로 봐야 합니다.

## Security Review Checklist

보안 리뷰는 모든 작업에 같은 강도로 적용할 필요는 없습니다.

하지만 다음 영역을 건드리는 작업이면 반드시 세부 보안 점검을 해야 합니다.

- 인증
- 권한
- 사용자 입력
- 파일 처리
- 외부 API
- dependency
- 설정
- 데이터 저장
- 로그
- workspace 작업

주요 점검 영역은 다음과 같습니다.

### Secrets / Credentials

API key, token, password, private key 같은 값이 코드, 로그, 설정, 테스트 데이터에 들어가지 않았는지 확인합니다.

또한 `.env` 관련 파일이 `.gitignore`에서 누락되어 커밋 대상에 포함될 위험이 없는지 확인합니다. 실제 secret은 Git에 올리지 않고, 공유가 필요한 경우 `.env.example`에 더미 값으로 구조만 남깁니다.

### Authentication

로그인, 세션, 토큰 검증이 누락되지 않았는지 확인합니다.

### Authorization / Access Control

로그인 여부와 리소스 접근 권한을 구분해서 확인합니다. 가장 중요한 보안 점검 영역입니다.

### Input Validation

사용자 입력, URL parameter, request body, header, 파일명, 외부 API 응답을 검증하는지 확인합니다.

### Injection

SQL, shell command, dynamic code execution, template 생성 등에 외부 입력이 안전하지 않게 들어가지 않는지 확인합니다.

### XSS / Client-Side Safety

사용자 입력을 HTML, markdown, iframe, URL 등으로 렌더링할 때 안전한지 확인합니다.

### Session / Cookie / CSRF / CORS

쿠키 보안 설정, CSRF 방어, CORS 범위, 세션 만료 정책이 약해지지 않았는지 확인합니다.

### Sensitive Data Exposure

개인정보, 토큰, 내부 ID, stack trace, DB 정보, 내부 경로가 응답이나 로그에 노출되지 않는지 확인합니다.

### File Handling

파일 업로드, 다운로드, 경로 조합에서 path traversal, 권한 누락, public 노출 위험이 없는지 확인합니다.

### External API / Network

외부 URL 호출, webhook, timeout, retry, rate limit, SSRF 위험을 확인합니다.

### Dependency / Supply Chain

새 dependency가 꼭 필요한지, 신뢰 가능한지, lockfile 변경이 의도된 것인지 확인합니다.

### Abuse / Rate Limit

로그인, 회원가입, 업로드, 검색, AI 호출 등 남용 가능성이 있는 기능에 제한이 필요한지 확인합니다.

### Workspace Safety

현재 프로젝트 밖 파일을 읽거나 쓰지 않는지, `../` 또는 absolute path로 workspace boundary를 우회하지 않는지 확인합니다.

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
