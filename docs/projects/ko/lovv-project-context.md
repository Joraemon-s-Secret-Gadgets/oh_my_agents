# Lovv 프로젝트 컨텍스트

이 문서는 Lovv 프로젝트에서 에이전트가 사용할 제품 맥락, 기술 스택, 라우팅, 데이터 저장 범위를 정리한 한국어 설명서입니다.

Lovv 작업에서 에이전트 역할, 도메인, 실행 모드, 하네스를 고르기 전에 이 문서를 기준으로 봅니다. 이 문서는 프로젝트 맥락만 구체화하며, 루트 `AGENTS.md`의 보안, 워크플로우, Workspace Boundary 규칙을 약화하지 않습니다.

## 기준

- 사용자는 제품 기능, 목표, 사용자에게 보이는 동작, 제외 범위, MVP 우선순위를 정의합니다.
- Main Codex는 이 프로젝트 컨텍스트, 루트 `AGENTS.md`, 승인된 Spec/Task, GitHub Issue, 기존 프로젝트 파일을 기준으로 기술 라우팅을 추론합니다.
- 사용자가 요청하지 않았거나 승인된 Spec에 없는 기능, 데이터 컬럼, API, 저장 정책을 임의로 만들지 않습니다.
- 승인된 Spec 없이 새 기능이나 구현 목표가 들어오면, 지원되는 subagent 하네스가 있을 때 Spec Agent를 생성합니다.

## 기본 기술 스택

- Frontend: React.
- Styling: TailwindCSS.
- API Runtime: AWS SAM + AWS Lambda.
- API Gateway: Amazon API Gateway.
- Backend Mode: 기본은 Serverless입니다.
- Database: Amazon Aurora MySQL-Compatible on Amazon RDS.
- Graph Database: 현재 범위에 포함하지 않습니다. 사용자가 새 Spec으로 명시 승인하지 않으면 Neo4j나 Graph DB를 사용하지 않습니다.
- Compute Exclusion: EC2는 기본 전제가 아닙니다. 승인된 미래 Spec에서 추가하기 전까지는 기본 범위에서 제외합니다.
- AI: 필요할 경우 RAG 기반 챗봇, 추천, 일정 생성 기능을 사용합니다.
- Crawl: 승인된 크롤링 작업은 Python 3.12, BeautifulSoup, Selenium, Scrapling을 기준으로 합니다.

## Backend API 라우팅

Lovv의 API 작업은 사용자가 명시적으로 스택을 바꾸지 않는 한 Backend AWS SAM 도메인으로 봅니다.

라우팅 기준은 다음과 같습니다.

- "API", "endpoint", "Lambda", "SAM", "API Gateway", "serverless", "backend" -> Backend AWS SAM domain.
- "DB", "database", "schema", "migration", "data model" -> Aurora MySQL-compatible data/API domain.
- 승인된 API Spec이 없음 -> Backend AWS SAM Spec Agent 생성.
- 승인된 API Spec은 있지만 Tasks/Subtasks가 없음 -> Backend AWS SAM Task Agent 생성.
- 승인된 API Subtask가 있고 구현 요청이 있음 -> Backend AWS SAM Implementation Agent 생성.
- 완료된 API diff, 변경 파일, PR, 리뷰 요청이 있음 -> 위험도에 따라 Backend AWS SAM Review Agent 또는 Security Review Agent 생성.

Backend AWS SAM 에이전트는 관련될 경우 Lambda handler 경계, `template.yaml` 또는 SAM template 변경, API Gateway route, event/request schema, response contract, 환경 변수, IAM 권한, observability, Aurora MySQL 데이터 접근을 고려해야 합니다.

## 기존 API Source Of Truth

Lovv에는 AWS SAM/backend 구조 검토와 Task 9/10 API scaffolding 작업에서 남긴 API 및 data-boundary 문서가 이미 있습니다. Backend AWS SAM 에이전트는 같은 도메인의 API contract, Lambda handler, API Gateway route, SAM template, frontend API adapter를 새로 만들거나 바꾸기 전에 이 문서들을 먼저 읽어야 합니다.

주요 API source-of-truth 문서는 다음과 같습니다.

- Small City API Contract: `docs/specs/LOVV_SMALL_CITY_API_CONTRACT.md`
- City Data Contract: `docs/specs/LOVV_CITY_DATA_CONTRACT.md`
- Task 9 API Contract Scope: `docs/specs/TASK9_API_CONTRACT_SCOPE.md`
- Task 9 Completion Report: `docs/reports/TASK9_COMPLETION.md`
- Task 10 Data Loading Scope: `docs/specs/TASK10_DATA_LOADING_SCOPE.md`
- Task 10 Completion Report: `docs/reports/TASK10_COMPLETION.md`
- Earlier backend integration packet: `docs/specs/TASK6_MAP_PROVIDER_BACKEND_INTEGRATION_SUBTASKS.md`

현재 해석은 다음과 같습니다.

- Task 9는 미래의 `GET /api/small-cities`, `GET /api/small-cities/:cityId` contract placeholder를 정의합니다.
- Task 10은 실제 backend 호출 없이, 정적 도시 데이터를 Task 9의 API-shaped adapter boundary를 통과하도록 만든 상태입니다.
- 이 영역의 현재 구현은 FE 중심이며, DB는 아직 구축 중입니다.
- 이 문서들은 기존 contract와 adapter boundary의 근거이지, 실제 AWS SAM backend endpoint가 이미 배포되었다는 증거가 아닙니다.
- 이 문서에 적힌 endpoint path는 SAM/API Gateway 배포 상태, stage/base URL, auth/environment configuration, DB readiness가 확인되기 전까지 production 또는 staging API 주소로 확정하지 않습니다.
- 기존 문서와 충돌하는 endpoint, filter, pagination, response field, metadata 노출 규칙, frontend adapter 동작을 임의로 만들지 않습니다.
- 승인된 Spec, deployment output, 사용자 지시로 실제 API 주소와 backend readiness가 확인되기 전까지 이 path를 대상으로 live fetch call을 구현하지 않습니다.
- 실제 API 주소, 배포 상태, DB readiness가 모호하면 작업을 멈추고 사용자에게 확인합니다.
- 실제 AWS SAM 구현은 승인된 API contract를 Lambda handler, API Gateway route, request/response validation, IAM, environment configuration, observability, Aurora MySQL access로 옮기되 기존 contract를 약화하면 안 됩니다.

## Database 규칙

- 기본 데이터베이스 대상은 Amazon Aurora MySQL-Compatible on Amazon RDS입니다.
- PostgreSQL을 기본으로 가정하지 않습니다.
- Neo4j, Graph DB, graph traversal 모델링을 기본으로 사용하지 않습니다.
- entity, relationship, index, migration은 승인된 Spec 또는 data contract와 맞춰야 합니다.
- 새 테이블, 대화 기록 저장, graph modeling, MVP 밖 데이터 보존을 도입하기 전에는 사용자 확인이 필요합니다.

## RAG 챗봇 및 AI 라우팅

RAG 기능은 frontend UI, backend API, retrieval/data, prompt, review 작업이 함께 필요할 수 있습니다.

기본 전제는 다음과 같습니다.

- 대화형 streaming이 필요하면 HTTP REST endpoint와 Lambda/API Gateway response streaming을 우선합니다.
- WebSocket은 기본값이 아닙니다.
- WebSocket은 승인된 Spec에서 장시간 양방향 세션, response streaming으로 해결하기 어려운 server push, 기타 REST streaming으로 충족할 수 없는 동작을 요구할 때만 사용합니다.
- model prompt, retrieval context, generated output은 secret 및 private configuration과 분리합니다.
- server-only AI provider key나 retrieval credential을 client-side code에 노출하지 않습니다.

## 저장 범위

현재 MVP의 기본 저장 범위는 다음과 같습니다.

- 사용자가 의도적으로 저장한 확정 또는 최종 여행 일정만 저장합니다.
- 진행 중인 chat message는 server-side에 기본 저장하지 않습니다.
- 완성되지 않은 plan draft는 server-side에 기본 저장하지 않습니다.
- "앱을 나갔다 들어와도 진행 중이던 대화를 이어가기"는 MVP 기본 범위로 가정하지 않습니다.
- 브라우저 local draft 저장은 사용자가 명시적으로 요청하거나 승인된 Spec에 포함된 경우에만 제안할 수 있으며, secret이나 민감 정보를 저장하면 안 됩니다.

conversation history, draft restore, background planning, durable AI generation state가 필요하면 구현 전에 Spec 업데이트가 필요합니다.

## Crawl 라우팅

사용자가 crawl, scrape, URL 데이터 수집, deep crawl, column extraction, BeautifulSoup, Selenium, Scrapling 사용을 요청하면 Crawl Focus로 봅니다.

Lovv 크롤링 기본값은 다음과 같습니다.

- Python 3.12를 사용합니다.
- static HTML은 BeautifulSoup을 우선합니다.
- rendering 또는 interaction이 필요할 때만 Selenium을 사용합니다.
- extraction helper가 유용할 때만 Scrapling을 사용합니다.
- 사용자 제공 또는 승인된 URL만 크롤링합니다.
- 사용자 지정 또는 승인된 column만 추출합니다.
- crawl column이나 source URL을 임의로 만들지 않습니다.
- 계획, 구현, 리뷰 전에 `docs/prompts/crawl-task-prompt.md`를 읽습니다.

## Frontend 라우팅

UI, React, TailwindCSS, route, component, hook, client state, form, accessibility, responsive behavior, frontend API integration, onboarding, chatbot screen, map UI, itinerary UI 요청은 Frontend domain work로 봅니다.

Frontend 에이전트는 계획, 구현, 리뷰 전에 `docs/agents/frontend-agent-rules.md`를 읽어야 합니다.

## 기능 입력 경계

사용자가 제공하면 좋은 입력은 다음과 같습니다.

- 기능 또는 제품 목표.
- 대상 사용자 흐름 또는 기대 동작.
- 알고 있는 경우 MVP 우선순위 또는 반드시 필요한 동작.
- 알고 있는 경우 명시적 제외 범위.
- 가능한 경우 GitHub Issue, Spec, Task, 파일 범위.

Main Codex가 추론해야 하는 항목은 다음과 같습니다.

- Domain: Frontend, Backend AWS SAM, RAG/AI, Crawl, Full-stack, QA, Security.
- Core Role: Spec Agent, Task Agent, Implementation Agent, Review Agent.
- Execution Mode: 일반 기능은 Hybrid, 보안/auth/DB/migration/모호하거나 되돌리기 어려운 작업은 Sequential, write scope가 명확히 분리된 경우에만 Parallel.
- 필요한 context 파일과 review gate.

이 문서로 판단이 명확한 경우, Main Codex는 사용자에게 agent role, execution mode, stack 세부사항을 직접 고르라고 요구하지 않습니다.

## 라우팅 예시

- "프론트엔드 로그인 기능 구현해야 해" -> Frontend domain, auth-sensitive, 승인된 Spec이 없으므로 Frontend Spec Agent 생성, Sequential Mode 우선.
- "이제 API 짜야돼" -> Backend AWS SAM domain, 승인된 Spec이 없으므로 Backend AWS SAM Spec Agent 생성.
- "DB 설계해야 해" -> Aurora MySQL-compatible database scope, entity 또는 승인된 Spec이 부족하면 질문, Graph DB는 기본 사용하지 않음.
- "RAG 챗봇 붙여야 해" -> 요청 동작에 따라 RAG/API/Frontend scope 판단, 기본은 REST/response streaming, WebSocket은 기본 가정하지 않음.
- "대화하다 나갔다 들어와도 이어지게 해줘" -> 기본 MVP 저장 범위가 아니므로 durable conversation/draft state를 추가하는 Spec 업데이트 필요.
- "크롤링 해야 해" -> Crawl Focus, 구현 전 승인된 URL, column, output path, output format, verification, stop condition 필요.
