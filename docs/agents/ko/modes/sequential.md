# Sequential Execution Mode 한국어 설명

Sequential Mode는 속도보다 안전성, 명확성, 사용자 확인이 더 중요한 작업에서 사용합니다.

## 언제 사용하는가

다음 작업에는 이 모드를 사용합니다.

- 새 프로젝트이거나 요구사항이 불명확한 작업.
- 인증, 인가, 권한, 결제, 보안, 개인정보, Secret 관련 작업.
- DB 스키마 변경, 마이그레이션, 데이터 삭제, 되돌리기 어려운 작업.
- 여러 모듈에 영향을 줄 수 있는 큰 refactor.
- write scope, 의존성 순서, acceptance criteria가 불명확한 작업.

## 운영 규칙

- 한 번에 하나의 역할만 실행합니다.
- 한 번에 하나의 Task 또는 Subtask만 진행합니다.
- 병렬 Implementation Agent를 실행하지 않습니다.
- Implementation Agent가 제한된 Task/Subtask를 완료하고 검증 결과를 보고하기 전에는 Review Agent를 시작하지 않습니다.
- 현재 Task/Subtask가 리뷰, 승인, 필요한 사용자 확인을 끝내기 전에는 다음 작업으로 이동하지 않습니다.
- Main Codex가 순서 관리, 에스컬레이션, 사용자 커뮤니케이션, 요청받은 Git 작업을 책임집니다.

## 필수 순서

1. Spec Agent가 Spec을 작성하거나 수정합니다.
2. 사용자 또는 Main Codex가 Spec의 범위, 명확성, 누락, 모순을 검토합니다.
3. Task Agent가 승인된 Spec을 Task와 Atomic Subtask로 나눕니다.
4. Implementation Agent가 승인된 Task/Subtask 하나만 구현합니다.
5. Implementation Agent가 정의된 로컬 검증을 실행합니다.
6. Review Agent가 완료된 작업을 리뷰합니다.
7. 문제가 있으면 Implementation Agent가 수정합니다.
8. Review Agent가 수정 결과를 재리뷰합니다.
9. Main Codex가 완료 결과를 보고하고 다음 진행 전 승인을 기다립니다.

## Context Loading

- Sequential Mode가 선택된 경우에만 이 파일을 읽습니다.
- 활성 Spec, Task/Subtask, 로컬 `AGENTS.md`, 필요한 역할별 format 파일만 읽습니다.
- 사용자가 모드 비교를 요청하지 않는 한 Hybrid 또는 Parallel mode 파일은 읽지 않습니다.

## 중단 조건

다음 경우에는 작업을 중단하고 사용자에게 에스컬레이션합니다.

- Task/Subtask 경계가 불명확합니다.
- 필요한 acceptance criteria가 없습니다.
- 검증이 3회 연속 실패합니다.
- Fix & Re-review가 3회 연속 반복됩니다.
- 작업이 workspace 밖 접근을 요구하는 것으로 보입니다.
