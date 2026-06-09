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

팀 제안은 에이전트 생성과 별개입니다.

- "팀 제안해줘", "team proposal", "agent team proposal"은 제안만 생성한다는 의미입니다.
- 제안을 준비하는 동안 실제 subagent를 생성하지 않습니다.
- "제안 승인. 시작해줘", "agent team 실행해줘", "실제 subagent로 생성해줘"는 승인된 제안을 기준으로 필요한 입력이 충분할 때 tool-backed subagent 생성을 진행하라는 의미입니다.

에이전트는 한글 요청을 영어 실행 의도로 정규화한 뒤 처리합니다.

| 한글 요청 패턴 | 영어 실행 의도 |
| --- | --- |
| `에이전트 생성해줘` | `Create a real tool-backed subagent.` |
| `<Role> Agent 생성해줘` | `Create a real tool-backed <Role> Agent subagent.` |
| `<Role> Agent 생성해서 <task> 해줘` | `Create a real tool-backed <Role> Agent subagent and assign it the bounded task.` |
| `<Role>로 동작해줘` | `Act as <Role> in the current Codex session. Do not create a subagent.` |
| `팀 제안해줘` | `Prepare an agent team proposal only. Do not create subagents.` |
| `제안 승인. 시작해줘` | `Start the approved proposal by creating real tool-backed subagents when scope is sufficient.` |

## Task-Based Creation Gate

사용자가 `Task`와 `Agent`와 생성 명령을 함께 제공하면, Main Codex는 이를 기획 프롬프트가 아니라 실행 가능한 subagent 생성 요청으로 처리해야 합니다.

즉시 생성에 필요한 필드는 다음과 같습니다.

- Task 또는 Goal
- Agent 이름 또는 역할
- Source of Truth
- Scope 또는 target files
- Verification, review focus, 또는 expected output
- `생성해줘`, `만들어줘`, `spawn`, `launch`, `delegate` 같은 생성 명령

이 필드들이 있고 지원되는 subagent 하네스가 있다면, 추가 승인을 다시 묻지 않고 즉시 subagent를 생성합니다. role activation으로 조용히 대체하지 않습니다.

생성 직전에는 다음 요약만 짧게 보여줍니다.

```md
Creating Subagent:
- Agent:
- Display Name:
- Core Role:
- Harness Agent Type:
- Harness Nickname: auto-assigned by harness
- Task:
- Source of Truth:
- Scope:
- Verification / Output:
```

하네스 닉네임 규칙은 다음과 같습니다.

- `Agent Name`, `Display Name`, `Core Role`은 프로젝트에서 정의하는 이름이며, Main Codex가 subagent prompt와 최종 보고 형식에 명시해야 합니다.
- `Harness Nickname`은 subagent 하네스가 런타임에 반환하는 자동 닉네임입니다.
- 하네스가 명시적인 이름 지정 필드를 제공하지 않는 한 `Harness Nickname`을 수동으로 지정했다고 말하면 안 됩니다.
- 생성 후에는 `Agent ID`, `Harness Nickname`, `Harness Agent Type`, `Agent Name`, `Core Role`을 보고합니다.
- subagent 최종 보고는 프로젝트에서 정의한 `Agent Name`으로 시작하도록 요구합니다.

하네스 agent type 기준은 다음과 같습니다.

- `worker`: 구현, 파일 수정, 테스트 수정, 문서 작성처럼 파일 변경 가능성이 있는 작업입니다.
- `explorer`: 읽기 전용 리뷰, 코드베이스 조사, 이슈 분석, 검증 질문입니다.
- default: worker나 explorer로 명확히 나뉘지 않을 때만 사용합니다.

필수 필드가 한두 개만 부족하면 그 항목만 질문합니다. 안전상 중요한 필드가 세 개 이상 부족하면 bounded Task/Agent/Scope 입력 블록을 요청합니다.

## Initial Work Intake Rule

사용자가 새 기능, 버그, 제품 작업, GitHub Issue, 구현 목표를 제공했지만 승인된 Spec을 제공하지 않은 경우, Main Codex는 기본적으로 직접 Spec을 작성하지 않습니다.

대신 지원되는 subagent 하네스가 있으면 실제 tool-backed Spec Agent를 생성합니다.

다음 요청에 이 규칙을 적용합니다.

- `이 기능 작업 시작해줘`
- `Lovv #123 작업 시작해줘`
- `회원가입 기능 만들어야 해`
- `이 이슈 기반으로 작업해줘`
- `Task 시작하자`
- `새 기능 구현 플로우 잡아줘`

Spec Agent가 Spec을 작성하거나 수정해야 합니다. Spec이 승인된 뒤에는 Task Agent를 생성하거나 요청해 Tasks와 Subtasks로 쪼갭니다. Main Codex는 조율과 통합을 담당하며, 사용자가 현재 세션 role activation을 명시적으로 요청했거나 subagent 하네스가 없는 경우가 아니라면 Spec Agent나 Task Agent의 작업을 대신하지 않습니다.

초기 작업 라우팅은 다음과 같습니다.

1. 승인된 Spec이 없음 -> Spec Agent 생성
2. 승인된 Spec은 있지만 Tasks/Subtasks가 없음 -> Task Agent 생성
3. 승인된 Subtask가 있고 구현 요청이 있음 -> Implementation Agent 생성
4. 완료된 작업 또는 diff가 있고 리뷰 요청이 있음 -> Review Agent 생성

## Default Interpretation

- "Review Agent 생성해서 리뷰해줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "Spec Agent 생성해서 스펙 작성해줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "Task Agent 생성해서 Task를 쪼개줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "Implementation Agent 생성해서 Subtask 2.1 구현해줘"는 지원되는 하네스가 있을 때 Tool-Backed Role Subagent Creation입니다.
- "현재 Codex가 Review Agent 역할로 리뷰해줘"는 사용자의 명시적 요청에 따른 Role Activation Fallback입니다.
- "Review Agent로 동작해서 리뷰해줘"는 실제 subagent 생성이 아니라 현재 세션의 Role Activation입니다.
- "Lovv #123 팀 제안해줘"는 제안만 생성한다는 의미이며 실제 subagent를 만들면 안 됩니다.
- "Lovv #123 제안 승인. 하이브리드로 시작해줘"는 제안과 scope가 명확할 때 승인된 tool-backed subagent를 생성하라는 의미입니다.
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
- Frontend Domain: target files 또는 folders, UI states, API/data assumptions, responsive requirements, accessibility requirements, verification command 또는 browser check, out-of-scope behavior입니다.

## Role Permission Matrix

사용자가 특정 run에 대해 더 좁거나 넓은 권한을 명시하지 않는 한 다음 권한표를 따릅니다.

| Role | May Do | Must Not Do |
| --- | --- | --- |
| Main Codex | 사용자 의도 해석, subagent 생성, scope 배정, 결과 통합, clarification 요청, 요청받은 최종 Git 작업 수행 | 모호성 숨기기, root rule 우회, 겹치는 scope를 가진 subagent를 조율 없이 실행 |
| Spec Agent | Spec, requirements, design, acceptance criteria, risks, planning context 작성 또는 수정 | 구현 코드 수정, Git history/remote 작업, 승인 없이 Task breakdown으로 진행 |
| Task Agent | 승인된 Spec을 Task/Subtask로 분해, 순서/scope/acceptance criteria/verification/handoff packet 정의 | 구현 코드 수정, Git history/remote 작업, 모호하거나 과도한 Subtask 생성 |
| Implementation Agent | 승인된 write scope 안에서만 파일 수정, 범위 내 검증 실행, 변경 파일과 blocker 보고 | scope 밖 파일 수정, commit/push/pull, 리뷰와 확인 없이 다음 Subtask 진행 |
| Review Agent | 변경 파일 리뷰, finding 보고, readiness 검증, 수정 방향 또는 commit message 제안 | 기본적으로 구현 파일 수정, commit/push/pull, Blocker가 남은 작업 승인 |

Review Agent는 기본적으로 read-only입니다. 사용자가 Review Agent에게 리뷰 문서 수정을 맡기려면 write scope를 명시해야 합니다.

## Agent Invocation Contract

tool-backed subagent를 생성하기 전에 가능한 경우 다음 계약을 명시해야 합니다.

```md
- User Request Original:
- Structured Agent Contract:
- Display Name:
- Core Role:
- Domain Focus:
- Work Focus:
- Execution Mode:
- Goal:
- Source of Truth:
- Scope:
- Out of Scope:
- Required Context:
- Output Format:
- Verification:
- Stop Condition:
```

규칙은 다음과 같습니다.

- 사용자가 한글 또는 영어가 아닌 언어로 작업을 지시했다면 `User Request Original`에는 원문을 그대로 보존합니다.
- `Structured Agent Contract`는 실행 필드를 정규화한 영어 계약으로 작성합니다.
- 영어 구조화 계약은 실행 안정성을 위한 것이며, 사용자의 원래 요청은 의도와 성공 기준의 최종 기준으로 남습니다.
- Implementation Agent는 제한된 write scope 없이 생성하지 않습니다.
- Review Agent는 review target 없이 생성하지 않습니다.
- Frontend-domain agent는 계획, 구현, 리뷰 전에 `docs/agents/frontend-agent-rules.md`를 읽어야 합니다.
- Frontend Implementation Agent는 target files 또는 folders, UI states, API/data assumptions, verification, out-of-scope behavior 없이 생성하지 않습니다.
- Crawl focus agent는 승인된 URL과 컬럼 없이 생성하지 않습니다.
- Crawl focus agent는 계획, 구현, 리뷰 전에 `docs/prompts/crawl-task-prompt.md`를 읽어야 합니다.
- Crawl focus 구현은 Python 3.12 파일 또는 스크립트와 기본 크롤링 도구인 BeautifulSoup, Selenium, Scrapling을 사용합니다. 추가 크롤러 프레임워크는 사용자 또는 승인된 Task의 명시 허용이 필요합니다.
- Deep crawl 요청은 seed URL, domain allowlist, max depth, max pages, rate limit, output columns, stop condition이 필요합니다.
- 추론한 계약 값이 있다면 subagent 생성 전에 사용자에게 밝힙니다.
- Execution Mode가 지정되지 않았으면 일반 기능 개발에는 Hybrid Mode를 사용하고, 보안 민감, DB, 인증, 인가, 결제, 마이그레이션, 되돌리기 어려운 작업, 모호한 작업에는 Sequential Mode를 사용합니다.
- Parallel Mode는 사용자가 명시적으로 병렬 에이전트를 요청했거나 write scope가 명확히 분리되어 Main Codex가 결과를 안전하게 통합할 수 있을 때만 사용합니다.
- 안전에 중요한 필드가 부족하면 생성하지 말고 최대 3개 질문으로 보충합니다.

## Agent Lifecycle & Cleanup

tool-backed subagent는 범위가 정해진 일회성 실행 컨텍스트로 취급합니다.

- subagent가 응답하지 않거나 루트 `No-Progress Limit` 안에 의미 있는 진전을 내지 못하면, 계속 기다리지 않습니다. 가능한 handoff 산출물만 보존한 뒤 해당 subagent context를 종료하거나 삭제하고, 필요한 경우 대체 subagent를 생성합니다.
- subagent가 맡은 Task, Subtask, review, handoff를 완료하면, 사용자가 명시적으로 유지하라고 하지 않는 한 사용이 끝난 subagent context를 닫기, 보관, 종료, 삭제 중 현재 하네스가 지원하는 방식으로 정리합니다.
- 역할이 겹치거나, 오래된 context를 들고 있거나, 소유 범위가 불명확한 유휴 subagent를 남겨두지 않습니다.
- cleanup은 agent context, thread, harness가 관리하는 agent record에만 적용합니다. 사용자가 별도로 명시하지 않는 한 프로젝트 파일, spec, report, branch, commit, 사용자 데이터는 삭제하지 않습니다.

## Subagent Output Contract

모든 subagent 최종 보고는 간결해야 하며, Main Codex가 결과를 통합하거나 handoff할 수 있을 만큼 충분한 정보를 포함해야 합니다.

공통 출력 필드는 다음과 같습니다.

```md
- Agent Name:
- Task/Subtask:
- Scope:
- Changed Files:
- Commands Run:
- Verification Result:
- Blockers:
- Assumptions:
- Next Recommended Action:
```

역할별 출력 요구사항은 다음과 같습니다.

- Spec Agent: Spec 경로 또는 초안 내용, unresolved questions, assumptions, approval needs를 포함합니다.
- Task Agent: Task/Subtask list, execution order, dependencies, acceptance criteria, verification commands를 포함합니다.
- Implementation Agent: changed files, implementation summary, verification results, blockers, known limitations를 포함합니다.
- Review Agent: Severity, Area, Evidence, Risk, Required Fix, Retest를 포함하는 Review Output Format을 사용합니다.
- Review Agent: `User Request Original`과 `Structured Agent Contract`가 모두 제공되면 구현 결과를 두 기준 모두와 비교합니다.
- Security Review Agent: 보안 민감 영역이 관련되면 Security Review Output Format을 사용합니다.
- Crawl-focused agent: input URLs, approved columns, output path, row count 또는 sample result, failures, `source_url`, `retrieved_at`, `failure_reason` 처리 여부를 포함합니다.

subagent가 작업을 완료할 수 없다면 조용히 계속하지 말고 blocker summary를 반환해야 합니다.

## Parallel Subagent Safety

병렬 subagent는 책임 범위가 독립적일 때만 허용합니다.

규칙은 다음과 같습니다.

- Implementation Agent는 명시적인 write scope를 가져야 합니다.
- 병렬 Implementation Agent의 write scope는 겹치면 안 됩니다.
- Review Agent는 사용자가 리뷰 문서 수정을 명시하지 않는 한 기본적으로 read-only입니다.
- 두 subagent가 같은 파일을 수정해야 하면 순차 실행합니다.
- Main Codex는 완료 보고 전에 subagent 결과를 통합하거나 충돌을 정리해야 합니다.
- 여러 subagent가 같은 실패 영역을 반복 수정하게 하지 말고, handoff summary와 사용자에게 보이는 escalation을 사용합니다.

## Agent Run Log

큰 작업이나 multi-agent 작업에서는 Main Codex가 `docs/reports/agent-runs/` 아래에 agent run log를 생성하거나 갱신하는 것이 좋습니다.

권장 파일명은 다음과 같습니다.

```md
docs/reports/agent-runs/RUN_[YYYYMMDD]_[short-task-name].md
```

run log에는 다음을 포함합니다.

- Run ID.
- Timestamp.
- Agent Name.
- Core Role / Domain Focus / Work Focus.
- Source of Truth.
- Scope and Out of Scope.
- Commands run.
- Changed files.
- Result.
- Blockers.
- Follow-up or handoff notes.

가능하면 `docs/reports/agent-runs/RUN_TEMPLATE.md`를 사용합니다.

다음 경우에는 run log가 필수입니다.

- 같은 사용자 요청에 2개 이상의 subagent가 사용됩니다.
- subagent가 병렬로 실행됩니다.
- Security Review Agent가 사용됩니다.
- Crawl Focus가 사용됩니다.
- Fix & Re-review가 2회 이상 반복됩니다.
- 작업이 여러 세션에 걸치거나 handoff가 필요합니다.
- 사용자가 traceability를 명시적으로 요청합니다.

## Review Gate Policy

구현 후에는 위험도에 맞는 리뷰 게이트를 사용합니다.

- Code Review Agent: 의미 있는 코드 변경에 사용합니다.
- QA Review Agent: 사용자 흐름, acceptance criteria, UI/API 동작, 데이터 출력, 회귀 위험이 있는 변경에 사용합니다.
- Security Review Agent: 인증, 권한, 사용자 입력, 파일 접근, 외부 API, dependency, configuration, data storage, logging, crawl behavior, workspace operation을 건드릴 때 사용합니다.

모든 작은 문서 변경에 모든 리뷰 게이트를 강제하지는 않습니다. Main Codex는 정확성, 보안, 사용자 의도를 보호할 수 있는 가장 작은 리뷰 조합을 선택합니다.

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
