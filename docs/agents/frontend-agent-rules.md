# Frontend Agent Rules

Use this file when a task has Frontend domain focus, React, TailwindCSS, browser-facing UI, frontend routes, components, hooks, client state, forms, accessibility, or frontend API integration.

This file specializes frontend work only. It must not weaken root `AGENTS.md`, workspace, security, environment variable, execution mode, review, or Git rules.

## Frontend Context Loading

For Frontend domain work, load:

- Root `AGENTS.md`.
- The selected execution mode file.
- The current Spec, Task, or Subtask packet.
- The nearest folder-level `AGENTS.md` when working inside a frontend folder.
- This file.

Load additional docs only when needed:

- `docs/agents/review-format.md` for frontend review.
- `docs/agents/security-review-checklist.md` for auth UI, client environment variables, token handling, redirects, user-generated content, form input, external scripts, or dependency changes.

Do not load `AGENTS.ko.md` unless Korean explanation or Korean doc synchronization is requested.

## Frontend Spec Agent

Frontend Spec Agent must define:

- User flow and screen flow.
- Route or view ownership.
- UI state matrix: loading, empty, success, error, disabled, pending, validation, permission, and offline states when relevant.
- Data dependencies and API contract assumptions.
- Form behavior, validation timing, error copy, and submission states.
- Accessibility requirements: semantic structure, labels, focus order, keyboard navigation, contrast, announcements, and error association.
- Responsive behavior across mobile, tablet, and desktop.
- Security and privacy concerns for client-visible data, tokens, user input, and redirects.
- Test and verification strategy.

Frontend Spec Agent must not write implementation code.

## Frontend Task Agent

Frontend Task Agent must split frontend work into Atomic Subtasks that are independently implementable and reviewable.

Prefer separate Subtasks for:

- Route or page shell.
- Component structure.
- API integration and data mapping.
- Form state and validation.
- Loading, error, empty, and success states.
- Accessibility and keyboard behavior.
- Responsive layout.
- Tests or browser verification.

Avoid mixing frontend UI, backend API, database, and test changes in one Subtask unless they are tightly coupled and explicitly scoped.

Each frontend Subtask must include:

- Purpose.
- Target files or folders.
- API/data assumptions.
- UI states to implement.
- Accessibility requirements.
- Responsive requirements.
- Verification commands or manual browser checks.
- Out-of-scope files and behavior.

## Frontend Implementation Agent

Frontend Implementation Agent must:

- Follow existing React structure, component patterns, hooks, routing, and naming.
- Use TailwindCSS consistently with existing design tokens, spacing, layout, and responsive conventions.
- Prefer small focused components with clear props and readable state flow.
- Keep UI state local unless shared state is clearly required.
- Handle loading, error, empty, success, disabled, pending, and validation states when relevant.
- Treat client-side validation as UX support only. Backend validation remains required.
- Preserve semantic HTML, labels, focus states, keyboard navigation, and readable error text.
- Avoid introducing a component library, state library, styling framework, animation library, or icon library unless explicitly approved.
- Do not expose server-only environment variables, secrets, API tokens, or private configuration to client-side code.
- Do not change backend API behavior from frontend scope unless the Task explicitly includes full-stack coordination.

Before editing, summarize the active frontend Task/Subtask, target files, UI states, API assumptions, and verification plan.

## React Rules

- Prefer existing component composition patterns over new abstractions.
- Avoid large components that mix data loading, form logic, presentation, and unrelated side effects.
- Keep hooks deterministic and scoped to one concern.
- Do not create broad global state unless the same state is required across distant routes or features.
- Avoid direct DOM manipulation unless integrating with an approved browser API or library.
- Keep derived UI state derived instead of duplicating it in state.

## TailwindCSS Rules

- Use existing Tailwind utilities, tokens, breakpoints, and layout patterns.
- Avoid one-off arbitrary values unless needed to match an existing design constraint.
- Do not create a new color system, spacing scale, shadow style, or typography scale without approval.
- Keep class names readable. Extract repeated complex patterns only when it improves maintainability.
- Ensure responsive classes preserve content order, readability, and touch target size.

## Frontend QA Review Agent

Frontend QA Review Agent must check:

- Implementation matches the approved Spec, Task, Subtask, and user intent.
- Required UI states exist: loading, empty, success, error, disabled, pending, validation, and permission states when relevant.
- Main user flows work from entry to completion.
- Edge cases and regression risks are covered.
- Tests, lint, build, or manual browser checks were run or clearly reported as unavailable.
- No unrelated UI, route, state, API, or style behavior changed.

Use browser or Playwright verification when the task changes user-visible UI and a runnable frontend target is available.

## Frontend UX and Accessibility Review Agent

Frontend UX and Accessibility Review Agent must check:

- Semantic HTML and landmark structure.
- Correct labels, names, roles, and descriptions.
- Keyboard navigation and visible focus states.
- Focus management for dialogs, drawers, menus, validation, and route transitions.
- Error text that is visible, understandable, and associated with the relevant field or control.
- Color contrast and non-color-only status indicators.
- Responsive layout at mobile, tablet, and desktop widths.
- Text overflow, wrapping, touch target size, and content overlap.

Accessibility findings that block task completion should be reported as Blocker when they prevent core usage or violate required acceptance criteria.

## Frontend Security Review Agent

Frontend Security Review Agent must check:

- No server-only secrets, API tokens, private keys, or sensitive environment variables are exposed to client code.
- Client-side auth checks are not treated as the only authorization boundary.
- Tokens are not stored or logged unsafely.
- Redirects and callback URLs are validated.
- User-generated content is rendered safely and not injected as executable HTML.
- External scripts, dependencies, and asset URLs are approved and necessary.
- Error messages do not expose sensitive implementation details.

Security-sensitive frontend work should also load `docs/agents/security-review-checklist.md`.

## Frontend Verification

Use project-defined commands when available. If commands are unknown, inspect package scripts first.

Suggested verification:

- Frontend lint.
- Unit/component tests.
- Typecheck when configured.
- Build.
- Browser/manual verification for user-visible flows.
- Responsive and accessibility spot checks.

If a runnable frontend target exists, significant UI changes should be verified in a browser before completion.

## Frontend Handoff

Frontend handoff must include:

- Changed files.
- UI states implemented or reviewed.
- API assumptions and backend coordination needs.
- Accessibility or responsive gaps.
- Commands or browser checks run.
- Screenshots or notes when visual verification was performed.
- Known limitations and next recommended action.
