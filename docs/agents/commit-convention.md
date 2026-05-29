## Git Commit Convention Details

Agents must follow the official Conventional Commits 1.0.0 specification when creating commits.

Official reference: https://www.conventionalcommits.org/en/v1.0.0/

Commit structure:

```md
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

Commit sections:

- Header: The first line, `<type>(<optional scope>): <description>`, must summarize what the commit is in one concise line.
- Body: When the change needs explanation, describe the full context, major changes, implementation notes, and verification details after one blank line.
- Footer: Add metadata after one blank line. If the work has a related GitHub issue, include the issue reference, such as `Refs: #123`, `Closes: #123`, or `Fixes: #123`.

Rules:

- Each commit should map to one completed Subtask whenever possible.
- The commit message must start with a `type`.
- `feat` must be used for a new feature and maps to a Semantic Versioning MINOR change.
- `fix` must be used for a bug fix and maps to a Semantic Versioning PATCH change.
- Other allowed types include `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, and `build` when they accurately describe the change.
- An optional `scope` may be added in parentheses to identify the changed module or location, such as `feat(auth):` or `fix(api):`.
- A description must follow the colon and space immediately after the type or scope.
- The description must be a concise one-line summary, must not start with an uppercase letter, and must not end with a period.
- A longer body may be added after one blank line when the change needs more context.
- Footers may be added after one blank line and must follow git trailer-style formatting.
- Footers should include the related GitHub issue when the Task or Subtask maps to an issue.
- Breaking changes must be marked with `!` after the type or scope, such as `feat!:` or `feat(api)!:`, or with a footer that starts with `BREAKING CHANGE:`.
- `BREAKING CHANGE` must be uppercase when used as a footer token.

## Commit Operation Guidelines

Create commits only after the current Task or Subtask is implemented, locally verified, and ready to hand off or archive.

## Git Operation Ownership

There is no dedicated Git Agent in this project.

Main Codex owns Git operations that affect repository history or remote state, including staging, commit, pull, push, branch switching, merge, rebase, and pull request creation.

Role subagents may report changed files, suggest commit messages, or review commit readiness, but they must not run history-changing or remote-changing Git commands unless the user explicitly authorizes it and Main Codex delegates it.

Implementation Agent must not commit or push its own changes.

Review Agent must not commit or push reviewed changes.

Before staging:

- Run `git status --short` and review every changed, staged, untracked, and deleted file.
- Run `git diff --check` or equivalent whitespace/conflict-marker validation when available.
- Verify that `.env`, `.env.local`, real credential files, local databases, generated secrets, and personal machine files are not staged.
- Review `.gitignore` when environment or generated files are involved.
- Confirm the changed files belong to the approved Task/Subtask scope.

Staging rules:

- Prefer explicit path staging such as `git add path/to/file`.
- Do not use broad staging such as `git add .` unless the changed file list has been reviewed and every file is intended.
- Do not stage unrelated user changes.
- Do not stage generated artifacts unless they are intentionally part of the Task.
- Do not stage large logs, build outputs, caches, local databases, or dependency folders.

Commit timing:

- Commit after a coherent Subtask is complete, not in the middle of unclear or failing work.
- If verification could not run, mention the reason in the commit body or handoff report.
- If the Task is blocked, prefer a handoff note or run log over a commit unless the user explicitly asks for a WIP commit.
- Do not create a commit only because files changed; commit only when the change is reviewable and scoped.

Commit body guidance:

- Use the body when the change is not obvious from the header.
- Include relevant implementation notes, verification results, and important constraints.
- Keep body text concise but sufficient for the next agent or reviewer.

Footer guidance:

- Include related issue metadata when available, such as `Refs: #123`, `Closes: #123`, or `Fixes: #123`.
- Include `BREAKING CHANGE:` when compatibility is broken.
- Do not invent issue numbers or external references.

Before pushing:

- Ensure the working tree is clean or contains only intentionally uncommitted unrelated user changes.
- Confirm the target branch and remote.
- If the push may affect shared work, mention the branch and commit hash in the user report.

Do not commit when:

- Real secrets or environment files are staged.
- The change includes unrelated files that the user did not approve.
- Tests or checks are failing and the failure is unexplained.
- The implementation scope is ambiguous.
- The user explicitly asked not to commit.

Examples:

```md
feat(auth): add session refresh flow

세션 만료 시 refresh token으로 로그인 상태를 갱신하는 흐름을 추가합니다.
검증: auth API test와 세션 만료 수동 시나리오를 확인했습니다.

Refs: #42
```

```md
fix(api): handle missing project id
docs(agents): document folder-level inheritance
refactor(tasks): split handover template generation
test(auth): add expired token coverage
feat(api)!: change project response format

BREAKING CHANGE: project responses now wrap data in a result object
```
