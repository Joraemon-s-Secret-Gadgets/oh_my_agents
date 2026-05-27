### Frontend React + Tailwind Folder-Level `AGENTS.md` Template

Use this template when creating `frontend/AGENTS.md` or a frontend feature-level `AGENTS.md`.

````md
# AGENTS.md

This file defines local frontend agent instructions for this folder.
It inherits the root `AGENTS.md`; local rules must not weaken root-level security, workflow, review, environment variable, or Workspace Boundary rules.

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

## Allowed Changes

- React components, hooks, client utilities, route/view files, styles, tests, and frontend documentation within this folder's scope.

## Forbidden Changes

- Do not change backend API behavior from frontend folders.
- Do not hardcode API secrets, tokens, or server-only environment variables.
- Do not bypass root security, environment, or Workspace Boundary rules.
- Do not introduce new global styling conventions without approval.

## Local Verification

- Use project-defined frontend commands when available.
- If commands are unknown, inspect package scripts before running tests.
- Suggested checks once configured:
  - frontend lint
  - frontend unit/component tests
  - frontend build
  - manual UI state and accessibility check

## Primary Agent Roles

- Primary: Implementation Agent for frontend Tasks and Subtasks.
- Review: Review Agent with frontend UX, accessibility, state, and API-integration focus.
- Security-sensitive areas: client environment variables, auth UI, token handling, forms, redirects, user-generated content.

## Handover Notes

- Document API assumptions, unverified UI states, accessibility gaps, and any required backend coordination.
````
