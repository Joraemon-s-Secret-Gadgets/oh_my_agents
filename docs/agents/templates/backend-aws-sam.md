### Backend AWS SAM Folder-Level `AGENTS.md` Template

Use this template when creating `backend/AGENTS.md`, `api/AGENTS.md`, `sam/AGENTS.md`, Lambda function folders, or backend module-level `AGENTS.md` files for Lovv.

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
