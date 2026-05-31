# Parallel Execution Mode 한국어 설명

Parallel Mode는 사용자가 명시적으로 병렬 에이전트를 요청했거나, Main Codex가 작업 범위가 독립적임을 확인할 수 있을 때만 사용합니다.

Parallel Mode는 전체 소요 시간을 줄일 수 있지만, 조율 비용과 충돌 위험이 증가합니다.

## 언제 사용하는가

다음 작업에는 이 모드를 사용할 수 있습니다.

- read-heavy 탐색, 저장소 감사, 로그 분석, 테스트 분석, 요약.
- security, QA, accessibility, performance, maintainability처럼 독립적인 리뷰 트랙.
- 파일 소유권이 겹치지 않고 shared contract가 안정적인 독립 구현 단위.
- 명확히 독립된 섹션으로 나눌 수 있는 대형 문서 또는 기획 작업.

보안 민감, DB, 인증, 결제, 마이그레이션, 불명확한 구현 작업에는 Sequential 또는 Hybrid Mode를 우선합니다.

## 필수 선행 조건

Parallel Mode에는 다음이 필요합니다.

- 명확한 Source of Truth.
- 작성된 Task/Subtask breakdown.
- Scope ownership table.
- 겹치지 않는 write scope.
- 명시적인 out-of-scope 경계.
- 각 에이전트의 verification command.
- 각 에이전트의 stop condition.
- Main Codex가 담당하는 최종 통합 및 리뷰 단계.

하나라도 부족하면 사용자에게 필요한 입력을 요청하거나 Hybrid Mode로 낮춥니다.

## Scope Ownership Table

병렬 에이전트를 생성하기 전에 Main Codex는 다음 표를 정의해야 합니다.

| Agent | Role | Task/Subtask | Write Scope | Read Scope | Forbidden Scope | Verification | Output |
| --- | --- | --- | --- | --- | --- | --- | --- |

write 가능한 파일 또는 디렉터리는 하나의 owner만 가져야 합니다.

## 운영 규칙

- 병렬 에이전트는 겹치는 파일, 디렉터리, migration, contract, generated output을 수정하면 안 됩니다.
- Review Agent는 기본적으로 read-only입니다.
- Implementation Agent는 commit, push, pull, merge, rebase, pull request 생성을 하면 안 됩니다.
- Main Codex는 필요한 모든 병렬 결과를 기다린 뒤 완료를 보고합니다.
- Main Codex는 conflict를 조정하고 tradeoff를 요약하며 최종 검증을 실행합니다.
- 병렬 에이전트가 blocker를 보고하면 Main Codex는 통합을 멈추고 계속 진행, scope 축소, 사용자 질문 중 하나를 결정합니다.

## 추천 병렬 패턴

Read-heavy:

- Security Review Agent가 보안 리스크를 확인합니다.
- QA Review Agent가 사용자 흐름, acceptance criteria, test gap을 확인합니다.
- Maintainability Review Agent가 구조, 중복, 복잡도를 확인합니다.

Split implementation:

- Frontend Implementation Agent가 frontend 파일만 담당합니다.
- Backend Implementation Agent가 backend 파일만 담당합니다.
- 둘 다 끝난 뒤 Review Agent가 통합 diff를 리뷰합니다.

Exploration:

- 한 에이전트가 frontend 구조를 파악합니다.
- 한 에이전트가 backend/API 구조를 파악합니다.
- 한 에이전트가 data model 또는 문서 맥락을 파악합니다.

## 금지되는 병렬 패턴

다음 경우에는 병렬 구현을 실행하지 않습니다.

- 에이전트가 같은 파일을 수정해야 합니다.
- 단일 owner 없이 여러 쪽에서 같은 API contract를 바꿔야 합니다.
- database migration을 생성하거나 순서를 바꿔야 합니다.
- 단일 owner 없이 인증, 인가, Secret 처리, 권한 로직을 바꿔야 합니다.
- 한 에이전트의 미완성 작업이 있어야 다른 에이전트 검증이 가능합니다.

## Context Loading

- Parallel Mode가 선택된 경우에만 이 파일을 읽습니다.
- 각 subagent에게 배정된 context packet만 읽힙니다.
- raw log, 전체 Spec, 관련 없는 문서를 모든 subagent에게 넘기지 않습니다.
- raw 중간 출력 대신 정제된 요약을 Main Codex에 반환합니다.

## Run Log

Parallel Mode는 프로젝트에 template이 있으면 `docs/reports/agent-runs/` 아래 agent run log가 필수입니다.

run log에는 scope ownership table, 사용된 agents, 수정 파일, 실행 명령, 검증 결과, blocker, 통합 결과를 포함해야 합니다.

## Final Integration Gate

Parallel Mode는 Main Codex가 다음을 완료하기 전까지 끝난 것이 아닙니다.

- write scope가 겹치지 않았는지 확인합니다.
- 모든 subagent 최종 보고를 검토합니다.
- conflict를 조정하거나 unresolved conflict를 보고합니다.
- 관련 최종 검증을 실행합니다.
- 구현 파일이 변경된 경우 통합 결과에 대해 Review Agent 승인을 요청합니다.
- 남은 risk와 사용자 결정 사항을 보고합니다.

## 중단 조건

다음 경우에는 작업을 중단하고 사용자에게 에스컬레이션합니다.

- write scope가 겹칩니다.
- 단일 owner 없이 shared contract가 변경됩니다.
- 두 에이전트 결과가 서로 호환되지 않습니다.
- 검증이 3회 연속 실패합니다.
- 최종 통합을 안전하게 리뷰할 수 없습니다.
