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
