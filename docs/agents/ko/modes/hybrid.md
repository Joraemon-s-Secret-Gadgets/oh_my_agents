# Hybrid Execution Mode 한국어 설명

Hybrid Mode는 일반적인 기능 개발의 기본 운영 방식입니다.

기획과 Task 분해는 순차로 유지하고, 범위가 독립적인 경우에만 제한적으로 병렬 작업을 허용합니다.

## 언제 사용하는가

다음 작업에는 이 모드를 사용합니다.

- 명확한 Spec과 Task breakdown이 있는 일반 기능 개발.
- 파일 소유권을 분리할 수 있는 frontend/backend 작업.
- QA review, security review, accessibility review, maintainability review처럼 독립적인 리뷰 트랙.
- 공유 파일을 수정하지 않는 탐색 또는 검증 작업.

요구사항, write scope, 보안 영향이 불명확하면 Sequential Mode를 사용합니다.

## 운영 규칙

- Spec Workflow는 항상 순차로 진행합니다.
- Task Breakdown Workflow는 항상 순차로 진행합니다.
- Implementation은 각 Implementation Agent의 write scope가 명확히 분리된 경우에만 병렬로 진행할 수 있습니다.
- Review는 read-only이거나 명시적으로 승인된 리뷰 문서만 수정하는 경우 병렬로 진행할 수 있습니다.
- Main Codex가 조율, 충돌 방지, 결과 통합, 사용자 커뮤니케이션, 요청받은 Git 작업을 책임집니다.
- 두 에이전트가 같은 파일, 경로, migration, API contract, data model, shared component를 건드려야 한다면 순차로 실행합니다.

## 허용되는 병렬 작업

병렬로 진행할 수 있는 작업은 다음과 같습니다.

- 파일 범위가 겹치지 않는 frontend 구현과 backend 구현.
- read-only 코드 탐색.
- test, lint, build, log 분석.
- read-only인 QA Review Agent, Security Review Agent, UX/Accessibility Review Agent, Maintainability Review Agent.

병렬로 진행하면 안 되는 작업은 다음과 같습니다.

- 여러 Implementation Agent가 같은 파일 또는 shared contract를 수정하는 작업.
- 여러 에이전트가 database migration을 변경하는 작업.
- 단일 owner 없이 인증, 인가, 권한, Secret 처리 코드를 여러 에이전트가 바꾸는 작업.
- 최종 통합 결과를 명확히 리뷰할 수 없는 작업.

## 필수 순서

1. Spec Agent가 Spec을 작성하거나 수정합니다.
2. Task Agent가 승인된 Spec을 Task와 Atomic Subtask로 나눕니다.
3. Main Codex가 병렬화 가능한 Subtask를 선택합니다.
4. Main Codex가 각 에이전트에 scope, out-of-scope, source of truth, verification command, stop condition을 명시합니다.
5. 각 에이전트는 배정된 scope 안에서만 독립적으로 작업합니다.
6. Main Codex가 필요한 모든 에이전트 결과를 기다립니다.
7. Main Codex가 결과를 통합하고 충돌을 해결합니다.
8. Review Agent 또는 병렬 read-only reviewer가 통합 결과를 리뷰합니다.
9. Main Codex가 검증 결과, finding, risk, 사용자 결정 필요 사항을 보고합니다.

## Scope Ownership

병렬 작업 전에 Main Codex는 다음을 정의해야 합니다.

- Agent name.
- Task/Subtask.
- Owned files or directories.
- Forbidden files or directories.
- 승인 없이 변경하면 안 되는 shared contracts.
- Verification command.
- Expected output.

## Context Loading

- Hybrid Mode가 선택된 경우에만 이 파일을 읽습니다.
- Subtask context packet을 만들 때는 `docs/agents/context-loading.md`를 읽습니다.
- 사용자가 모드 비교를 요청하지 않는 한 Sequential 또는 Parallel mode 파일은 읽지 않습니다.

## Run Log

Hybrid Mode에서 같은 사용자 요청에 2개 이상의 subagent를 사용하면 agent run log를 생성하거나 업데이트합니다.

## 중단 조건

다음 경우에는 작업을 중단하고 사용자에게 에스컬레이션합니다.

- 에이전트 scope가 겹칩니다.
- owner 없이 shared contract가 변경됩니다.
- 검증이 3회 연속 실패합니다.
- Fix & Re-review가 3회 연속 반복됩니다.
- Main Codex가 subagent 결과를 안전하게 통합할 수 없습니다.
