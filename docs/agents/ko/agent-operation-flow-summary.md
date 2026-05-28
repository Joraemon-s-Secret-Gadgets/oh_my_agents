# Agent Operation Flow Summary

팀원 공유용으로 에이전트 운영 방식과 전체 흐름만 짧게 정리합니다.

## 1. 핵심 구조

```md
Codex = Main Agent / Orchestrator

Core Role = Spec Agent | Task Agent | Implementation Agent | Review Agent
Domain Focus = General | Frontend | Backend | Full-stack
Work Focus = Code | QA | Security | UX | Performance | Crawl

AGENTS.md = 전체 운영 규칙
folder/AGENTS.md = 특정 폴더의 로컬 규칙
docs/prompts/crawl-task-prompt.md = 크롤링 작업용 프롬프트
```

`AGENTS.md`는 하네스가 아닙니다. 실제 subagent 생성은 Codex의 subagent harness가 담당합니다.

## 2. 에이전트 이름 규칙

핵심 역할은 4개만 유지하고, 실제 생성 이름은 필요하면 domain/focus를 붙입니다.

```md
[Domain] [Focus] [Core Role]
```

예시:

```md
Frontend Spec Agent
Backend Implementation Agent
Frontend QA Review Agent
Backend Security Review Agent
Crawl Implementation Agent
```

해석 예시:

```md
Frontend QA Review Agent
= Review Agent + Frontend Domain + QA Focus

Crawl Implementation Agent
= Implementation Agent + Crawl Focus
```

## 3. 전체 운영 흐름

```md
사용자 요청
↓
Main Codex가 요청 해석
↓
Role / Domain / Focus / Scope 확인
↓
입력이 부족하면 최대 3개 질문
↓
subagent 생성
↓
subagent가 필요한 최소 문서만 읽고 작업
↓
Main Codex가 결과 취합
↓
사용자에게 보고
↓
승인 후 다음 단계 진행
```

입력이 부족하면 모호한 에이전트를 만들지 않습니다. 안전하게 추론 가능하면 추론값을 밝히고 진행하고, 위험하면 필요한 정보만 질문합니다.

## 4. 역할별 흐름

### Spec Agent

```md
아이디어 / 요청
↓
목표, 제외 범위, 사용자 흐름, 요구사항 정리
↓
Acceptance Criteria, 제약, 리스크 작성
↓
Spec 초안 반환
↓
사용자 승인 대기
```

Spec Agent는 구현하지 않습니다.

### Task Agent

```md
승인된 Spec
↓
Feature Task로 분해
↓
Subtask로 세분화
↓
우선순위, 의존성, 완료 기준, 검증 명령 작성
↓
다음 에이전트용 지시서 반환
```

Task Agent도 구현하지 않습니다.

### Implementation Agent

```md
승인된 Task/Subtask
↓
Source of Truth와 수정 가능 Scope 확인
↓
필요한 파일만 읽고 구현
↓
test / lint / build 실행
↓
변경 파일과 검증 결과 보고
```

하나의 Task 또는 Subtask만 처리하고 다음 작업으로 임의 진행하지 않습니다.

### Review Agent

```md
구현 완료 보고
↓
변경 파일 / diff 확인
↓
Spec, 사용자 의도, Acceptance Criteria 부합성 확인
↓
정확성, 테스트, 유지보수성, 보안 확인
↓
Approved 또는 수정 요청 반환
```

`QA Review Agent`, `Security Review Agent`는 `Review Agent`에 focus를 붙인 형태입니다.

## 5. Domain별 기준

```md
Frontend
- React, TailwindCSS, route, component, hook, client state
- API integration, loading/error/empty/success state
- accessibility, responsive UI, client-side secret 노출 방지

Backend
- Django, API, model, migration, serializer/form
- server-side validation, authentication, authorization
- permission, error response, data integrity, settings, secrets

Full-stack
- frontend와 backend가 강하게 연결된 사용자 흐름

General
- docs, scripts, shared, config, common
```

`frontend/AGENTS.md`와 `backend/AGENTS.md`는 에이전트 생성 파일이 아니라, 해당 도메인 subagent가 읽는 로컬 규칙 파일입니다.

## 6. Review Focus 기준

```md
Code = 코드 품질, 구조, 유지보수성, 기존 패턴
QA = 사용자 흐름, 상태 처리, 회귀 위험, 테스트 커버리지
Security = 인증, 권한, secret, 입력 검증, XSS, injection, dependency
UX = 접근성, 폼 UX, 반응형, 사용자-facing error state
Performance = 렌더링, 쿼리, bundle size, API call, costly operation
```

## 7. Crawl 흐름

크롤링은 5번째 핵심 역할이 아니라 `Crawl Focus`입니다.

```md
Crawl Implementation Agent = Implementation Agent + Crawl Focus
Crawl QA Review Agent = Review Agent + Crawl Focus + QA
Crawl Security Review Agent = Review Agent + Crawl Focus + Security
```

크롤링 작업 필수 입력:

```md
URLs
Columns
Output Format
Output Path
Allowed Tools
Verification
Stop Condition
```

기본 규칙:

```md
- Python 3.12 사용
- 정적 HTML은 BeautifulSoup 우선
- 렌더링/상호작용 필요 시 Selenium 사용
- 추출 보조가 유용할 때 Scrapling 사용
- 사용자 제공 또는 Task 승인 URL만 수집
- 사용자 지정 또는 Task 승인 컬럼만 수집
- 임의 컬럼 추가 금지
- robots.txt, 약관, rate limit, copyright, privacy 준수
- source_url, retrieved_at, failure_reason 기록
```

상세 기준은 크롤링 작업일 때만 `docs/prompts/crawl-task-prompt.md`를 읽습니다.

## 8. 토큰 절감 원칙

```md
- AGENTS.ko.md는 팀원 설명용이며 기본 로딩하지 않음
- docs/agents/* 전체를 한 번에 읽지 않음
- 현재 역할과 작업에 필요한 문서만 읽음
- Full Spec 전체보다 현재 Subtask 지시서를 우선 읽음
- docs/prompts/*는 해당 prompt 작업일 때만 읽음
- 대용량 로그, .git 내부, 빌드 산출물, 큰 데이터 파일은 통째로 읽지 않음
```

## 9. 요청 예시

```md
Backend Implementation Agent 생성해서 Subtask 1.1 구현해줘.

- Source of Truth: docs/specs/TASK1_SUBTASKS.md
- Scope: backend/accounts/
- Verification: python manage.py test accounts
- Stop Condition: 테스트 3회 연속 실패 시 중단
```

```md
Frontend QA Review Agent 생성해서 회원가입 UI를 검증해줘.

- Source of Truth: docs/specs/signup_SPEC.md
- Review Target: frontend/src/pages/signup
- Work Focus: QA, UX
- Verification: npm run test, npm run build
```

```md
Crawl Implementation Agent 생성해서 지정 URL에서 드라마 촬영지 데이터를 수집해줘.

- URLs: [사용자 제공 URL]
- Columns: drama_title, location_name, address, source_url, retrieved_at, failure_reason
- Output Path: data/drama_locations.csv
```

## 10. 한 줄 요약

```md
Codex가 조율하고, 4개 핵심 역할 subagent가 작은 단위로 작업하며,
Domain/Focus로 범위를 좁히고, 필요한 문서만 읽어 토큰을 줄입니다.
```
