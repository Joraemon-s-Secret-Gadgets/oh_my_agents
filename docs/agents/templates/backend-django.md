### Backend Django Folder-Level `AGENTS.md` Template

Use this template when creating `backend/AGENTS.md` or a backend app/module-level `AGENTS.md`.

````md
# AGENTS.md

This file defines local backend agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

## Agent Focus

This folder is backend-focused.
Agents working here must prioritize Django app boundaries, API contracts, validation, authentication, authorization, data integrity, error handling, observability, and server-side security.

## Project Stack

- Framework: Django
- API Layer: Use the project's existing Django API pattern, such as Django REST Framework if already present.
- Database: Use the configured project database.
- Package Manager: Detect from project files before running commands.

## Folder Purpose

- Describe the backend domain, Django app, API area, or service module owned by this folder.

## Ownership Scope

- Owned files:
- Related frontend/API consumers:
- Explicitly out of scope:

## Local Rules

- Follow Django app boundaries and existing project structure.
- Keep business logic out of views when it grows; prefer services, selectors, forms, serializers, managers, or existing local patterns.
- Validate all user input server-side.
- Enforce authentication and authorization server-side.
- Never log passwords, tokens, API keys, secrets, or sensitive user data.
- Use Django migrations for model changes and review migrations before applying them.
- Use Django settings and environment variables safely; never hardcode secrets in settings or source code.
- Use Django's built-in password hashing and security mechanisms.
- Consider rate limiting or abuse protection for authentication-sensitive or costly endpoints.
- Return consistent error responses without leaking stack traces or internal details.

## Allowed Changes

- Django apps, models, migrations, views, serializers/forms, services, selectors, permissions, tests, and backend documentation within this folder's scope.

## Forbidden Changes

- Do not change frontend behavior from backend folders unless explicitly scoped.
- Do not bypass authentication, authorization, validation, or migration review.
- Do not commit real `.env` files, credentials, local databases, or generated secrets.
- Do not weaken root security, environment, or Workspace Boundary rules.

## Local Verification

- Use project-defined backend commands when available.
- If commands are unknown, inspect project scripts or Django management configuration before running tests.
- Suggested checks once configured:
  - backend lint
  - Django system checks
  - migrations check
  - backend unit/API tests
  - security-sensitive manual checks for auth, permissions, and validation

## Primary Agent Roles

- Primary: Implementation Agent for backend Tasks and Subtasks.
- Review: Review Agent with backend correctness, API contract, data integrity, and security focus.
- Security-sensitive areas: settings, environment variables, authentication, authorization, permissions, password handling, tokens, sessions, migrations, file access, external APIs.

## Handover Notes

- Document API contracts, migration status, auth/permission assumptions, unverified edge cases, and required frontend coordination.
````
