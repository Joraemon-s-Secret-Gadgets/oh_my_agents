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

아래 코드 블록으로 작성된 `AGENTS.md`들은 실제로 하위 폴더에 새 `AGENTS.md` 파일을 만들 때 사용하는 생성 템플릿입니다.

즉, 이 코드 블록 자체가 현재 폴더에 적용되는 별도 규칙은 아니며, 사용자가 `frontend/AGENTS.md를 생성해줘` 또는 `backend/AGENTS.md를 생성해줘`처럼 요청했을 때 에이전트가 복사해서 해당 폴더 상황에 맞게 채우는 기준 양식입니다.

템플릿 안의 빈 항목은 실제 폴더의 목적, 소유 파일, 허용 변경, 금지 변경, 검증 명령, 보안 민감 영역으로 채워야 합니다. 루트의 보안, 워크플로우, 환경 변수, Workspace Boundary 규칙은 템플릿으로 생성된 하위 파일에서도 그대로 상속됩니다.

하위 폴더용 `AGENTS.md` 기본 템플릿은 다음과 같습니다.

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

Agents working in this folder must also follow `docs/agents/frontend-agent-rules.md`.

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
- Required UI states:
- Accessibility requirements:
- Responsive requirements:
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
- Keep route/view behavior aligned with the approved Spec and frontend task packet.
- Do not duplicate derived UI state unless there is a clear reason.
- Keep form submission, validation, disabled, pending, and error states explicit.
- Verify responsive behavior before marking user-visible UI complete.

## Allowed Changes

- React components, hooks, client utilities, route/view files, styles, tests, and frontend documentation within this folder's scope.

## Forbidden Changes

- Do not change backend API behavior from frontend folders.
- Do not hardcode API secrets, tokens, or server-only environment variables.
- Do not bypass root security, environment, or Workspace Boundary rules.
- Do not introduce new global styling conventions without approval.
- Do not store or log tokens, credentials, sensitive user data, or server-only configuration in client code.
- Do not treat client-side auth checks as the only authorization boundary.

## Local Verification

- Use project-defined frontend commands when available.
- If commands are unknown, inspect package scripts before running tests.
- Suggested checks once configured:
  - frontend lint
  - frontend unit/component tests
  - frontend typecheck when configured
  - frontend build
  - manual UI state, responsive, and accessibility check
  - browser or Playwright verification for significant user-visible UI changes

## Primary Agent Roles

- Primary: Implementation Agent for frontend Tasks and Subtasks.
- Review: Review Agent with frontend UX, accessibility, state, and API-integration focus.
- Security-sensitive areas: client environment variables, auth UI, token handling, forms, redirects, user-generated content.
- QA: Frontend QA Review Agent for user flows, UI states, regression risk, responsive behavior, and browser verification.
- UX/A11y: Frontend UX and Accessibility Review Agent for semantic HTML, keyboard navigation, focus management, error copy, contrast, and touch targets.

## Handover Notes

- Document API assumptions, unverified UI states, accessibility gaps, and any required backend coordination.
````

### Backend AWS SAM Folder-Level `AGENTS.md` Template

Lovv 프로젝트의 `backend/AGENTS.md`, `api/AGENTS.md`, `sam/AGENTS.md`, Lambda function 폴더, backend module 폴더용 `AGENTS.md`를 만들 때 사용하는 기본 템플릿입니다.

에이전트가 실제로 사용할 원문 템플릿은 [docs/agents/templates/backend-aws-sam.md](../templates/backend-aws-sam.md)입니다.

````md
# AGENTS.md

This file defines local backend AWS SAM agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

Agents working in this folder must also follow `docs/projects/lovv-project-context.md`.

## Agent Focus

This folder is backend-focused.
Agents working here must prioritize AWS SAM boundaries, Lambda handlers, API Gateway contracts, request/response validation, authentication, authorization, data integrity, observability, IAM safety, and server-side security.

## Project Stack

- Runtime: AWS SAM with AWS Lambda.
- API Gateway: Amazon API Gateway.
- Database: Amazon Aurora MySQL-Compatible on Amazon RDS.
- Compute: Serverless by default; do not assume EC2.
- Graph DB: Not in current scope; do not introduce Neo4j or another graph database without an approved Spec.
- Package Manager: Detect from project files before running commands.

## Folder Purpose

- Describe the backend API, Lambda function, SAM module, service module, or data-access area owned by this folder.

## Ownership Scope

- Owned files:
- Related frontend/API consumers:
- Related SAM template or infrastructure files:
- Related data models or SQL:
- Explicitly out of scope:

## Local Rules

- Before creating or changing small-city API routes, Lambda handlers, SAM templates, request/response contracts, or frontend API adapters, read the Existing API Source Of Truth section in `docs/projects/lovv-project-context.md`.
- Treat Task 9/10 small-city API documents as the current contract and adapter boundary, not as proof that a live backend endpoint already exists.
- Treat endpoint paths in those documents as placeholders until the actual SAM/API Gateway base URL, stage, auth/environment configuration, and DB readiness are verified.
- Do not implement live API calls while the related product path is still frontend-only or backend/DB readiness is unclear.
- Follow existing Lambda handler, service, repository, and validation patterns.
- Keep API contracts aligned with the approved Spec and frontend data assumptions.
- Validate all user input server-side.
- Enforce authentication and authorization server-side.
- Never log passwords, tokens, API keys, secrets, or sensitive user data.
- Use environment variables safely and never hardcode secrets.
- Keep IAM permissions least-privilege and scoped to the required Lambda behavior.
- Keep API Gateway routes, request schemas, response schemas, status codes, and error shapes explicit.
- Use Aurora MySQL-compatible access patterns approved by the Spec or data contract.
- Do not introduce graph database behavior, WebSocket behavior, or durable chat history unless an approved Spec requires it.
- Consider rate limiting, abuse protection, timeout limits, retry bounds, and cost impact for auth-sensitive, AI, crawl, or expensive endpoints.
- Return consistent error responses without leaking stack traces, internal IDs, credentials, or provider details.

## Allowed Changes

- Lambda handlers, services, repositories, validators, API contracts, SAM templates, backend tests, and backend documentation within this folder's scope.

## Forbidden Changes

- Do not change frontend behavior from backend folders unless explicitly scoped.
- Do not bypass authentication, authorization, validation, IAM review, or API contract review.
- Do not commit real `.env` files, credentials, local databases, generated secrets, or provider tokens.
- Do not introduce EC2, Neo4j, Graph DB, WebSocket, or server-side in-progress chat persistence without an approved Spec.
- Do not weaken root security, environment, or Workspace Boundary rules.

## Local Verification

- Use project-defined backend commands when available.
- If commands are unknown, inspect project scripts, SAM configuration, and test scripts before running checks.
- Suggested checks once configured:
  - backend lint
  - backend unit/API tests
  - SAM template validation
  - Lambda handler tests
  - API contract tests
  - database query or migration checks when relevant
  - security-sensitive manual checks for auth, permissions, IAM, validation, secrets, and logging

## Primary Agent Roles

- Primary: Implementation Agent for backend AWS SAM Tasks and Subtasks.
- Review: Review Agent with backend correctness, API contract, data integrity, IAM, observability, and security focus.
- Security-sensitive areas: environment variables, IAM, authentication, authorization, permissions, tokens, sessions, data access, API Gateway routes, external APIs, AI provider calls, logging.

## Handover Notes

- Document API contracts, SAM template assumptions, IAM assumptions, Aurora MySQL assumptions, unverified edge cases, and required frontend or RAG coordination.
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
루트 AGENTS.md의 Backend AWS SAM Folder-Level Template을 기반으로 작성하고,
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
Backend AWS SAM 템플릿을 기반으로 auth 백엔드 규칙만 작성해줘.
```
