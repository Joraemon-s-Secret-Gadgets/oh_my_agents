# Lovv Project Context

This file defines Lovv-specific product, stack, routing, and persistence assumptions for project agents.

Load this file before choosing an agent role, domain, execution mode, or harness in this project. This file specializes Lovv project context only; it does not weaken the root `AGENTS.md`.

## Source Of Truth

- The user defines the product feature, goal, user-visible behavior, exclusions, and MVP priority.
- Main Codex infers technical routing from this project context, root `AGENTS.md`, approved Specs, Tasks, GitHub Issues, and existing project files.
- Do not invent features, data columns, APIs, or persistence behavior that the user or approved Spec did not request.
- If the user asks for a new feature or implementation goal without an approved Spec, create a Spec Agent when a supported subagent harness is available.

## Default Project Stack

- Frontend: React.
- Styling: TailwindCSS.
- API Runtime: AWS SAM with AWS Lambda.
- API Gateway: Amazon API Gateway.
- Backend Mode: Serverless by default.
- Database: Amazon Aurora MySQL-Compatible on Amazon RDS.
- Graph Database: Not in current scope. Do not use Neo4j or another graph database unless the user explicitly approves a new Spec.
- Compute Exclusion: Do not assume EC2 is required. EC2 is out of default scope unless a future approved Spec adds it.
- AI: RAG-based chatbot, recommendation, and itinerary generation when the feature requires AI behavior.
- Crawl: Python 3.12 with BeautifulSoup, Selenium, and Scrapling for approved crawl tasks.

## Backend API Routing

Treat Lovv API work as the Backend AWS SAM domain unless the user explicitly changes the stack.

Route requests as follows:

- "API", "endpoint", "Lambda", "SAM", "API Gateway", "serverless", or "backend" -> Backend AWS SAM domain.
- "DB", "database", "schema", "migration", or "data model" -> Aurora MySQL-compatible data/API domain.
- No approved API Spec -> create a Backend AWS SAM Spec Agent.
- Approved API Spec but no Tasks/Subtasks -> create a Backend AWS SAM Task Agent.
- Approved API Subtask and implementation request -> create a Backend AWS SAM Implementation Agent.
- Completed API diff, changed files, PR, or review request -> create a Backend AWS SAM Review Agent or Security Review Agent depending on risk.

Backend AWS SAM agents must consider Lambda handler boundaries, `template.yaml` or SAM template changes, API Gateway routes, event/request schemas, response contracts, environment variables, IAM permissions, observability, and Aurora MySQL data access when relevant.

## Existing API Source Of Truth

Lovv already has API/data-boundary documents from the AWS SAM/backend structure review and the Task 9/10 API scaffolding work. Backend AWS SAM agents must read these before creating or changing API contracts, Lambda handlers, API Gateway routes, SAM templates, or frontend API adapters for the same domain.

Primary API source-of-truth documents:

- Small City API Contract: `docs/specs/LOVV_SMALL_CITY_API_CONTRACT.md`
- City Data Contract: `docs/specs/LOVV_CITY_DATA_CONTRACT.md`
- Task 9 API Contract Scope: `docs/specs/TASK9_API_CONTRACT_SCOPE.md`
- Task 9 Completion Report: `docs/reports/TASK9_COMPLETION.md`
- Task 10 Data Loading Scope: `docs/specs/TASK10_DATA_LOADING_SCOPE.md`
- Task 10 Completion Report: `docs/reports/TASK10_COMPLETION.md`
- Earlier backend integration packet: `docs/specs/TASK6_MAP_PROVIDER_BACKEND_INTEGRATION_SUBTASKS.md`

Current interpretation:

- Task 9 defines the future `GET /api/small-cities` and `GET /api/small-cities/:cityId` contract placeholders.
- Task 10 keeps the implementation frontend-only while routing static city data through the Task 9 API-shaped adapter boundary.
- The current implemented product path is frontend-only for this area; the database is still under construction.
- These documents are existing contract and adapter-boundary evidence, not proof that a live AWS SAM backend endpoint is already deployed.
- Endpoint paths in these documents are not confirmed production or staging API addresses until the SAM/API Gateway deployment, stage/base URL, auth/environment configuration, and DB readiness are verified.
- Do not invent conflicting endpoints, filters, pagination, response fields, metadata exposure rules, or frontend adapter behavior.
- Do not implement live fetch calls against these paths until a real API address and backend readiness are confirmed by an approved Spec, deployment output, or user instruction.
- If the actual API address, deployment state, or DB readiness is unclear, stop and ask the user before continuing.
- A real AWS SAM implementation must map the approved API contract into Lambda handlers, API Gateway routes, request/response validation, IAM, environment configuration, observability, and Aurora MySQL access without weakening the existing contract.

## Database Rules

- Use Amazon Aurora MySQL-Compatible on Amazon RDS as the default database target.
- Do not assume PostgreSQL.
- Do not use Neo4j, graph DB, or graph traversal modeling by default.
- Keep entities, relationships, indexes, and migrations aligned with the approved Spec or data contract.
- Ask the user before introducing new tables, persistent conversation history, graph modeling, or non-MVP data retention.

## RAG Chatbot And AI Routing

RAG features may involve frontend UI, backend API, retrieval/data, prompt, and review work.

Default assumptions:

- Use HTTP REST endpoints and Lambda/API Gateway response streaming when conversational streaming is required.
- Do not use WebSocket by default.
- Use WebSocket only if an approved Spec requires long-lived bidirectional sessions, server-pushed events beyond response streaming, or other behavior that REST streaming cannot satisfy.
- Keep model prompts, retrieval context, and generated outputs separated from secrets and private configuration.
- Do not expose server-only AI provider keys or retrieval credentials to client-side code.

## Persistence Scope

The current MVP persistence default is:

- Persist confirmed or final itineraries when the user intentionally saves them.
- Do not persist in-progress chat messages server-side by default.
- Do not persist unfinished plan drafts server-side by default.
- Do not assume "resume unfinished conversation after leaving the app" is included in MVP.
- Optional browser-local draft storage may be proposed only when the user or approved Spec explicitly asks for it, and it must avoid secrets and sensitive data.

If a feature needs conversation history, draft restore, background planning, or durable AI generation state, stop and require a Spec update before implementation.

## Crawl Routing

Treat crawl work as Crawl Focus when the user asks to crawl, scrape, collect data from URLs, deep crawl, extract columns, or use BeautifulSoup, Selenium, or Scrapling.

Lovv crawl defaults:

- Use Python 3.12.
- Use BeautifulSoup for static HTML.
- Use Selenium only when rendering or interaction is required.
- Use Scrapling only when extraction helper behavior is useful.
- Crawl only user-provided or approved URLs.
- Extract only user-specified or approved columns.
- Do not invent crawl columns or source URLs.
- Load `docs/prompts/crawl-task-prompt.md` before planning, implementation, or review.

## Frontend Routing

Treat UI, React, TailwindCSS, route, component, hook, client state, form, accessibility, responsive behavior, frontend API integration, onboarding, chatbot screen, map UI, or itinerary UI requests as Frontend domain work.

Frontend agents must load `docs/agents/frontend-agent-rules.md` before planning, implementation, or review.

## Feature Input Boundary

The user should provide:

- Feature or product goal.
- Target user flow or expected behavior.
- MVP priority or must-have behavior when known.
- Explicit exclusions when known.
- GitHub Issue, Spec, Task, or file scope when available.

Main Codex should infer:

- Domain: Frontend, Backend AWS SAM, RAG/AI, Crawl, Full-stack, QA, or Security.
- Core Role: Spec Agent, Task Agent, Implementation Agent, or Review Agent.
- Execution Mode: Hybrid for ordinary feature work; Sequential for security, auth, DB, migration, ambiguous, or irreversible work; Parallel only for clearly separated write scopes.
- Required context files and review gates.

Main Codex should not ask the user to choose agent role, execution mode, or stack details when this context makes the choice clear.

## Routing Examples

- "프론트엔드 로그인 기능 구현해야 해" -> Frontend domain, auth-sensitive, no approved Spec means create a Frontend Spec Agent and prefer Sequential Mode.
- "이제 API 짜야돼" -> Backend AWS SAM domain, no approved Spec means create a Backend AWS SAM Spec Agent.
- "DB 설계해야 해" -> Aurora MySQL-compatible database scope; ask for entities or approved Spec if missing; do not use graph DB by default.
- "RAG 챗봇 붙여야 해" -> RAG/API/Frontend scope depending on requested behavior; default to REST/response streaming and do not assume WebSocket.
- "대화하다 나갔다 들어와도 이어지게 해줘" -> Not in default MVP persistence; require Spec update because it adds durable conversation/draft state.
- "크롤링 해야 해" -> Crawl Focus; require approved URLs, columns, output path, output format, verification, and stop condition before implementation.
