# Frontend Agent Rules 한국어 설명

이 문서는 Frontend domain focus가 있는 작업에서 사용하는 프론트엔드 전용 에이전트 규칙입니다.

React, TailwindCSS, 브라우저 UI, route, component, hook, client state, form, accessibility, frontend API integration이 관련되면 이 문서를 읽습니다.

이 문서는 프론트엔드 작업을 전문화할 뿐이며, 루트 `AGENTS.md`의 보안, workspace, environment variable, execution mode, review, Git 규칙을 약화할 수 없습니다.

## Frontend Context Loading

Frontend domain 작업에서는 다음을 읽습니다.

- 루트 `AGENTS.md`
- 선택된 execution mode 파일
- 현재 Spec, Task, Subtask packet
- 프론트엔드 폴더 안에서 작업할 경우 가장 가까운 folder-level `AGENTS.md`
- 이 파일

필요할 때만 추가로 읽습니다.

- frontend review에는 `docs/agents/review-format.md`
- auth UI, client environment variables, token handling, redirects, user-generated content, form input, external scripts, dependency 변경에는 `docs/agents/security-review-checklist.md`

한국어 설명이나 한국어 문서 동기화 요청이 없으면 `AGENTS.ko.md`는 읽지 않습니다.

## Frontend Spec Agent

Frontend Spec Agent는 다음을 정의해야 합니다.

- 사용자 흐름과 화면 흐름
- route 또는 view ownership
- UI state matrix: loading, empty, success, error, disabled, pending, validation, permission, offline 상태
- 데이터 의존성과 API contract 가정
- form behavior, validation timing, error copy, submission state
- accessibility 요구사항: semantic structure, labels, focus order, keyboard navigation, contrast, announcement, error association
- mobile, tablet, desktop 반응형 동작
- client-visible data, token, user input, redirect 관련 보안/개인정보 고려
- 테스트와 검증 전략

Frontend Spec Agent는 구현 코드를 작성하지 않습니다.

## Frontend Task Agent

Frontend Task Agent는 프론트엔드 작업을 독립적으로 구현하고 리뷰할 수 있는 Atomic Subtask로 쪼갭니다.

가능하면 다음을 별도 Subtask로 나눕니다.

- route 또는 page shell
- component structure
- API integration과 data mapping
- form state와 validation
- loading, error, empty, success state
- accessibility와 keyboard behavior
- responsive layout
- tests 또는 browser verification

UI, backend API, database, test 변경을 하나의 Subtask에 섞지 않습니다. 단, 강하게 결합되어 있고 명시적으로 scope가 잡힌 경우는 예외입니다.

각 frontend Subtask에는 다음이 포함되어야 합니다.

- Purpose
- Target files 또는 folders
- API/data assumptions
- 구현할 UI states
- Accessibility requirements
- Responsive requirements
- Verification commands 또는 manual browser checks
- Out-of-scope files and behavior

## Frontend Implementation Agent

Frontend Implementation Agent는 다음을 지켜야 합니다.

- 기존 React 구조, component pattern, hook, routing, naming을 따릅니다.
- TailwindCSS를 기존 design token, spacing, layout, responsive convention에 맞게 사용합니다.
- 명확한 props와 읽기 쉬운 state flow를 가진 작고 집중된 component를 선호합니다.
- 공유 state가 명확히 필요하지 않으면 UI state는 local로 유지합니다.
- 관련될 경우 loading, error, empty, success, disabled, pending, validation 상태를 처리합니다.
- client-side validation은 UX 보조로만 봅니다. backend validation은 여전히 필요합니다.
- semantic HTML, label, focus state, keyboard navigation, 읽기 쉬운 error text를 유지합니다.
- 명시 승인 없이 component library, state library, styling framework, animation library, icon library를 추가하지 않습니다.
- server-only environment variable, secret, API token, private configuration을 client-side code에 노출하지 않습니다.
- Task가 full-stack coordination을 명시하지 않는 한 frontend scope에서 backend API behavior를 바꾸지 않습니다.

파일을 수정하기 전에는 active frontend Task/Subtask, target files, UI states, API assumptions, verification plan을 요약합니다.

## React Rules

- 새 abstraction보다 기존 component composition pattern을 우선합니다.
- data loading, form logic, presentation, unrelated side effect가 섞인 큰 component를 피합니다.
- hook은 deterministic하고 하나의 concern에 집중합니다.
- 서로 먼 route나 feature에서 같은 state가 필요하지 않으면 broad global state를 만들지 않습니다.
- 승인된 browser API 또는 library 통합이 아니라면 직접 DOM 조작을 피합니다.
- derived UI state는 중복 state로 저장하지 않고 파생시킵니다.

## TailwindCSS Rules

- 기존 Tailwind utility, token, breakpoint, layout pattern을 사용합니다.
- 기존 design constraint를 맞추기 위해 필요한 경우가 아니라면 일회성 arbitrary value를 피합니다.
- 승인 없이 새로운 color system, spacing scale, shadow style, typography scale을 만들지 않습니다.
- class name은 읽을 수 있게 유지합니다. 반복되는 복잡한 pattern은 유지보수성이 좋아질 때만 추출합니다.
- responsive class가 content order, readability, touch target size를 해치지 않도록 확인합니다.

## Frontend QA Review Agent

Frontend QA Review Agent는 다음을 확인합니다.

- 구현이 승인된 Spec, Task, Subtask, 사용자 의도와 맞습니다.
- 필요한 UI state가 있습니다: loading, empty, success, error, disabled, pending, validation, permission state
- 주요 사용자 흐름이 시작부터 완료까지 동작합니다.
- edge case와 regression risk가 확인되었습니다.
- test, lint, build, manual browser check가 실행되었거나 불가능한 이유가 보고되었습니다.
- 관련 없는 UI, route, state, API, style behavior가 바뀌지 않았습니다.

사용자에게 보이는 UI가 바뀌고 실행 가능한 frontend target이 있으면 browser 또는 Playwright 검증을 사용합니다.

## Frontend UX and Accessibility Review Agent

Frontend UX and Accessibility Review Agent는 다음을 확인합니다.

- semantic HTML과 landmark structure
- 올바른 label, name, role, description
- keyboard navigation과 visible focus state
- dialog, drawer, menu, validation, route transition의 focus management
- 보이고 이해 가능하며 관련 field/control에 연결된 error text
- color contrast와 색상에만 의존하지 않는 상태 표시
- mobile, tablet, desktop 반응형 layout
- text overflow, wrapping, touch target size, content overlap

핵심 사용을 막거나 acceptance criteria를 위반하는 accessibility 문제는 Blocker로 보고합니다.

## Frontend Security Review Agent

Frontend Security Review Agent는 다음을 확인합니다.

- server-only secret, API token, private key, sensitive environment variable이 client code에 노출되지 않습니다.
- client-side auth check가 유일한 authorization boundary로 취급되지 않습니다.
- token이 unsafe하게 저장되거나 log로 남지 않습니다.
- redirect와 callback URL이 검증됩니다.
- user-generated content가 executable HTML로 주입되지 않고 안전하게 렌더링됩니다.
- external script, dependency, asset URL은 승인되었고 필요합니다.
- error message가 민감한 구현 세부사항을 노출하지 않습니다.

보안 민감 frontend 작업은 `docs/agents/security-review-checklist.md`도 읽습니다.

## Frontend Verification

프로젝트에 정의된 명령을 사용합니다. 명령을 모르면 package scripts를 먼저 확인합니다.

권장 검증은 다음과 같습니다.

- frontend lint
- unit/component tests
- typecheck가 설정된 경우 typecheck
- build
- 사용자 visible flow에 대한 browser/manual verification
- responsive/accessibility spot check

실행 가능한 frontend target이 있으면 중요한 UI 변경은 완료 전 browser로 검증합니다.

## Frontend Handoff

Frontend handoff에는 다음을 포함합니다.

- 변경 파일
- 구현 또는 리뷰한 UI states
- API assumptions와 backend coordination 필요 사항
- accessibility 또는 responsive gap
- 실행한 명령 또는 browser check
- visual verification을 했다면 screenshot 또는 notes
- known limitations와 next recommended action
