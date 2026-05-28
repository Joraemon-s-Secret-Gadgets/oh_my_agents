## Agent Creation Guidelines

사용자가 에이전트를 생성해 달라고 하거나, 특정 역할을 활성화해 달라고 하거나, 폴더별 `AGENTS.md` 파일 생성을 요청할 때 이 문서를 참고합니다.

## Agent Creation Semantics

사용자가 "Review Agent 생성해줘", "Spec Agent 생성해줘"처럼 말하면, Main Codex는 먼저 지원되는 subagent 하네스를 통해 실제 tool-backed subagent를 생성하는 요청으로 해석해야 합니다.

Agent creation은 세 가지 의미일 수 있습니다.

1. Tool-Backed Role Subagent Creation
   - Main Codex가 사용 가능한 subagent 하네스를 통해 별도 subagent를 생성하거나 위임합니다.
   - 사용자가 Spec Agent, Task Agent, Implementation Agent, Review Agent를 생성, 실행, spawn, 위임, 구동해 달라고 요청하면 기본적으로 이 의미로 해석합니다.
   - 하나의 역할, 하나의 제한된 Task 또는 Subtask, 최소한의 필요 컨텍스트, 요구 출력 형식만 전달합니다.
   - 실제 도구나 하네스가 생성하지 않았다면 별도 에이전트를 생성했다고 말하면 안 됩니다.

2. Role Activation Fallback
   - 현재 에이전트가 요청받은 역할로 현재 작업을 수행합니다.
   - 새 파일, 새 프로세스, 독립 에이전트는 생성되지 않습니다.
   - 지원되는 subagent 하네스가 없거나, 사용자가 현재 Codex 세션에서 해당 역할로 수행하라고 명시했거나, subagent 생성 불가 후 사용자가 fallback을 승인한 경우에만 사용합니다.

3. Folder-Level `AGENTS.md` Creation
   - 특정 폴더 안에 로컬 `AGENTS.md` 파일을 생성합니다.
   - 사용자가 폴더 경로를 제공하거나 폴더별 지침 생성을 요청한 경우에만 사용합니다.
   - `docs/agents/templates` 안의 적절한 템플릿을 사용합니다.

## Default Interpretation

- "Review Agent 생성해서 리뷰해줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "Spec Agent 생성해서 스펙 작성해줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "Task Agent 생성해서 Task를 쪼개줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "Implementation Agent 생성해서 Subtask 2.1 구현해줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "현재 Codex가 Review Agent 역할로 리뷰해줘"는 사용자의 명시적 요청에 따른 Role Activation Fallback입니다.
- "`frontend/AGENTS.md` 생성해줘"는 Folder-Level `AGENTS.md` Creation입니다.
- "`backend/AGENTS.md` 생성해줘"는 Folder-Level `AGENTS.md` Creation입니다.
- "별도 에이전트/서브에이전트를 생성해서 맡겨줘"는 지원되는 도구나 하네스가 있을 때만 Tool-Backed Role Subagent Creation입니다.

subagent 생성을 요청받았지만 현재 환경에서 사용할 수 없다면, Main Codex는 실제 subagent 생성이 불가능하다고 보고하고 Role Activation Fallback으로 계속 진행할지 사용자에게 확인해야 합니다.

## Current Role Agents

현재 프로젝트의 역할 에이전트는 다음 4가지입니다.

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

이들은 지원되는 subagent 하네스가 있을 때 실제 tool-backed subagent로 생성되는 것을 기본으로 합니다. 현재 Codex 세션의 역할 활성화는 fallback일 때만 사용합니다.

## Role Agent Creation Criteria

역할 에이전트는 작업 단계에 맞춰 생성하거나 활성화합니다.

- Spec Agent: 요구사항, 설계, 목표, 제외 범위, 사용자 흐름, 성공 기준, 제약, 리스크, 구현 전 계획이 필요하고 아직 Task가 확정되지 않았을 때 생성합니다.
- Task Agent: 승인된 Spec이 있고, 이를 기능 Task, 순서가 있는 Subtask, 의존성, 성공 기준, 검증 명령, 다음 에이전트 전달 지시서로 쪼개야 할 때 생성합니다.
- Implementation Agent: 승인된 Task 또는 Subtask가 있고, 사용자가 해당 범위의 구현, 수정, 리팩터링, 테스트, 문서화를 요청할 때 생성합니다.
- Review Agent: 완료된 작업을 Spec, 사용자 의도, 성공 기준, 정확성, 보안, 유지보수성, 테스트, workspace safety 기준으로 검증해야 할 때 생성합니다.

역할 경계는 다음과 같습니다.

- Spec Agent와 Task Agent는 사용자가 명시적으로 역할과 승인 범위를 바꾸지 않는 한 구현 코드를 작성하지 않습니다.
- Implementation Agent는 필요한 리뷰, 검증, 사용자 확인 규칙 없이 다음 Subtask로 넘어가지 않습니다.
- "Frontend Agent"나 "Backend Agent"는 기본적으로 새로운 핵심 역할로 보지 않습니다. Implementation Agent 또는 Review Agent에 도메인 초점을 더한 것으로 해석하거나, 사용자가 폴더 경로 또는 로컬 폴더 지침 생성을 요청한 경우에만 folder-level `AGENTS.md`를 생성합니다.
- 요청된 역할이 불명확하면 실행 전에 어떤 역할로 해석했는지 먼저 밝힙니다.

## Agent Naming Convention

핵심 역할은 다음 4개로 제한합니다.

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

subagent는 작업 범위를 명확히 하기 위해 표시 이름에 domain과 focus label을 붙일 수 있습니다.

표시 이름 형식은 다음과 같습니다.

```md
[Domain] [Focus] [Core Role]
```

허용되는 domain label은 다음과 같습니다.

- General: shared utility, docs, scripts, 설정 인접 작업, ownership이 불명확한 작업입니다.
- Frontend: React, TailwindCSS, route, component, hook, client state, accessibility, 브라우저에서 동작하는 기능입니다.
- Backend: Django, API, model, migration, serializer/form, auth, permission, validation, data integrity입니다.
- Full-stack: frontend와 backend 동작이 강하게 연결된 사용자 흐름입니다.

허용되는 focus label은 다음과 같습니다.

- Code: 코드 품질, 구조, 유지보수성, 로컬 convention입니다.
- QA: 사용자 흐름, acceptance criteria, success/error/empty state, 회귀 리스크, test coverage입니다.
- Security: authentication, authorization, secret, input validation, injection, XSS, file access, external API, dependency, workspace safety입니다.
- UX: 사용성, 접근성, 문구, form behavior, responsive behavior, 사용자-facing error state입니다.
- Performance: rendering, query, bundle size, API call, memory, costly operation입니다.

예시는 다음과 같습니다.

- Frontend Spec Agent
- Backend Task Agent
- Frontend Implementation Agent
- Backend Implementation Agent
- QA Review Agent
- Frontend QA Review Agent
- Backend Security Review Agent
- Full-stack QA Review Agent

domain과 focus label은 새로운 root role을 만들지 않습니다. subagent의 scope, required context, output expectation을 좁히는 역할만 합니다.

해석 예시는 다음과 같습니다.

- Frontend QA Review Agent = Core Role: Review Agent; Domain: Frontend; Focus: QA.
- Backend Security Review Agent = Core Role: Review Agent; Domain: Backend; Focus: Security.
- Frontend Implementation Agent = Core Role: Implementation Agent; Domain: Frontend; Focus: Code unless another focus is specified.

QA Review Agent는 다음을 확인해야 합니다.

- 승인된 Spec과 acceptance criteria 기준의 사용자 흐름입니다.
- success, error, empty, loading, permission, edge state입니다.
- 회귀 리스크와 누락된 test coverage입니다.
- 관련될 경우 frontend accessibility, responsive behavior, form UX, client-side error handling입니다.
- 관련될 경우 backend API validation, error response, permission behavior, data integrity입니다.

## Agent Creation Request Inputs

역할 subagent를 생성하기 전에 Main Codex는 요청에 안전하게 제한된 작업을 맡길 수 있을 만큼 충분한 정보가 있는지 확인해야 합니다.

공통 입력값은 다음과 같습니다.

- Display Name: Frontend QA Review Agent 같은 요청된 subagent 이름입니다.
- Role: Spec Agent, Task Agent, Implementation Agent, Review Agent 중 하나입니다.
- Domain Focus: 필요할 경우 General, Frontend, Backend, Full-stack 중 하나입니다.
- Work Focus: 필요할 경우 Code, QA, Security, UX, Performance, 또는 명시된 다른 focus입니다.
- Goal: subagent가 달성해야 하는 목표입니다.
- Source of Truth: subagent가 따라야 하는 승인된 Spec, Task, Subtask, issue, PR, diff, branch, changed files입니다.
- Scope: subagent가 읽거나 수정할 수 있는 파일, 폴더, 모듈, 동작 범위입니다.
- Out of Scope: subagent가 건드리면 안 되는 파일, 폴더, 모듈, 동작 범위입니다.
- Required Context: subagent가 반드시 읽어야 하는 문서나 섹션입니다.
- Output Format: subagent가 반환해야 하는 리포트, Spec, Task list, patch summary, review format입니다.
- Verification: subagent가 실행하거나 해당 없음으로 보고해야 하는 test, check, build, lint, manual validation입니다.
- Stop Condition: subagent가 계속 진행하지 말고 중단 후 에스컬레이션해야 하는 조건입니다.

역할별 최소 입력값은 다음과 같습니다.

- Spec Agent: 목표 또는 기능 아이디어, 명확하지 않을 경우 대상 사용자나 시스템 행위자, 알려진 제약, 가능하다면 예상 사용자 흐름입니다.
- Task Agent: 승인된 Spec 경로 또는 승인된 Spec 내용, 기본값과 다른 세분화 수준이 필요할 경우 원하는 Task granularity, 의존성, workflow에서 요구될 경우 다음 Task 번호입니다.
- Implementation Agent: Task 또는 Subtask ID, Source of Truth, 허용된 write scope, acceptance criteria, verification command 또는 프로젝트 script에서 추론해도 된다는 허용입니다.
- Review Agent: changed files, branch, PR, diff 같은 리뷰 대상, Source of Truth, correctness, security, UX, performance, all 같은 review focus입니다.

## Missing Input Handling

필수 입력값이 부족하면 Main Codex는 모호하거나 범위가 과도한 subagent를 생성하면 안 됩니다.

처리 순서는 다음과 같습니다.

1. 누락된 값이 기존 맥락에서 명확하면 안전하게 추론합니다.
2. 추론을 사용했다면 subagent 생성 전에 추론한 값을 사용자에게 밝힙니다.
3. 안전한 추론이 불가능하면 누락된 필수 정보만 사용자에게 질문합니다.
4. 질문은 한 번에 최대 3개까지만 합니다.
5. 안전성, 범위, 출력 품질에 실질적 영향이 없는 선택 입력값은 질문하지 않습니다.

질문 예시는 다음과 같습니다.

```md
Implementation Agent를 생성하려면 범위를 안전하게 제한해야 합니다.

1. 구현할 Task/Subtask ID는 무엇인가요?
2. 수정 가능한 파일 또는 폴더 범위는 어디까지인가요?
3. 완료 후 실행해야 할 검증 명령이 있나요?
```

```md
Review Agent를 생성하려면 리뷰 대상을 확정해야 합니다.

1. 리뷰할 변경 파일, 브랜치, PR, 또는 diff는 무엇인가요?
2. 기준이 되는 Spec/Task 문서는 어디인가요?
3. 리뷰 초점은 전체 검토인가요, 보안 중심인가요?
```

## Current Folder-Level Templates

폴더별 `AGENTS.md` 파일을 만들 때만 다음 템플릿을 사용합니다.

- General folder: `docs/agents/templates/folder-level.md`
- Frontend React + Tailwind folder: `docs/agents/templates/frontend-react-tailwind.md`
- Backend Django folder: `docs/agents/templates/backend-django.md`

## Folder-Level Template Creation Criteria

폴더가 안정적으로 담당하는 범위에 맞춰 템플릿을 선택합니다.

- General: shared utility, common module, 문서 영역, script, 설정 인접 폴더, 또는 frontend/backend ownership이 명확하지 않은 폴더에 사용합니다.
- Frontend React + Tailwind: `frontend/`, React route 폴더, UI feature 폴더, component library, hook, client utility, Tailwind styling 영역, 브라우저에서 동작하는 기능에 사용합니다.
- Backend Django: `backend/`, Django app, API module, model, migration, serializer/form, permission, service, selector, server-side validation, data integrity 영역에 사용합니다.

폴더가 존재한다는 이유만으로 folder-level `AGENTS.md`를 만들지 않습니다. 앞으로의 에이전트 작업에서 안정적인 로컬 규칙이 실제로 모호성을 줄여줄 때만 생성합니다.

## When To Create A Folder-Level `AGENTS.md`

다음 경우에만 폴더별 `AGENTS.md`를 생성합니다.

- 해당 폴더가 명확한 도메인, 기능, 모듈, 책임을 가집니다.
- 로컬 규칙이 루트 `AGENTS.md`와 다릅니다.
- 해당 폴더에 특별한 검증, 보안, 기술 스택, ownership, handoff 규칙이 필요합니다.
- 해당 폴더에서 반복 작업이 많아 안정적인 로컬 지침이 도움이 됩니다.

다음 경우에는 생성하지 않습니다.

- 임시 폴더입니다.
- 명확한 ownership이 없습니다.
- 루트 `AGENTS.md`를 반복하는 내용뿐입니다.
- 일회성 프롬프트로 충분한 작업입니다.

## Template Selection

- General 템플릿은 shared utility, docs 영역, common module, frontend/backend에 특화되지 않은 폴더에 사용합니다.
- Frontend React + Tailwind 템플릿은 `frontend/` 또는 frontend feature 폴더에 사용합니다.
- Backend Django 템플릿은 `backend/` 또는 Django app/module 폴더에 사용합니다.

어떤 템플릿이 맞는지 불명확하면 파일을 생성하기 전에 사용자에게 질문합니다.

## Required Checks Before Creating

- 루트 `AGENTS.md`를 읽습니다.
- 가장 가까운 상위 folder-level `AGENTS.md`가 있으면 읽습니다.
- 폴더 목적과 소유 파일을 확인합니다.
- 로컬 규칙이 루트 규칙을 약화하지 않는지 확인합니다.
- 새 folder-level `AGENTS.md`는 짧게 유지합니다.

## What To Include

- Folder purpose
- Ownership scope
- Local rules
- Allowed changes
- Forbidden changes
- Local verification
- Primary agent roles
- Handover notes

## What Not To Include

- 루트 보안 규칙을 중복 복사하지 않습니다.
- 긴 템플릿을 무작정 복사하지 않습니다.
- 프로젝트 전체 workflow 규칙을 넣지 않습니다.
- 관련 없는 폴더 규칙을 넣지 않습니다.
- secret, 환경 변수 값, credential, 로컬 머신 경로를 넣지 않습니다.

## Token Budget

- folder-level `AGENTS.md`는 가능하면 20-60줄로 짧게 유지합니다.
- 긴 공통 규칙은 복사하지 말고 루트나 `docs/agents` 문서로 링크합니다.
- 한국어 문서 수정, 동기화 확인, 한국어 설명 요청이 아니면 `AGENTS.ko.md`를 읽지 않습니다.
- 모든 템플릿을 읽지 말고 선택한 템플릿만 읽습니다.

## Creation Output

folder-level `AGENTS.md`를 만든 뒤에는 다음을 보고합니다.

- 생성된 경로
- 선택한 템플릿
- 폴더 목적
- 추가한 로컬 규칙
- 검증 명령
- 남은 가정이나 미해결 사항
