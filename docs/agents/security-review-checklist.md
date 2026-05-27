## Security Review Checklist

Review Agent must run this checklist when a Task touches authentication, authorization, user input, files, external APIs, dependencies, configuration, data storage, logging, or workspace operations.

### Secrets / Credentials

Check for:

- Hardcoded API keys, tokens, passwords, private keys, or credentials.
- Real secrets in `.env`, config files, logs, fixtures, test data, or documentation.
- Unprotected `.env` files that are missing from `.gitignore` and could be included in agent commits.
- Server-only secrets exposed to client-side code.
- Confusion between example values and real credentials.

### Authentication

Check for:

- Missing login, session, or token validation.
- Unsafe handling of expired, forged, missing, or malformed tokens.
- Authentication errors that reveal internal information.
- Passwords, tokens, or session values written to logs.

### Authorization / Access Control

Check for:

- Confusion between "is logged in" and "has access to this resource".
- Missing ownership or membership checks for user-specific data.
- Admin-only behavior available to normal users.
- Authorization enforced only in the frontend.
- Object ID changes that allow access to another user's data.

### Input Validation

Check for:

- Unvalidated user input from body, query, params, headers, forms, files, or external APIs.
- Missing type, length, format, enum, and range checks.
- Unsafe handling of empty values, very long values, malformed JSON, or special characters.
- Trusting client-side validation without server-side validation.

### Injection

Check for:

- SQL, NoSQL, LDAP, or ORM queries built through unsafe string concatenation.
- Shell commands that include user-controlled input.
- Dynamic code execution such as `eval`, unsafe template execution, or untrusted dynamic imports.
- Regex, template, or script generation from untrusted input.

### XSS / Client-Side Safety

Check for:

- Rendering user input as raw HTML.
- Unsafe use of `dangerouslySetInnerHTML` or equivalent APIs.
- Markdown, rich text, iframe, script, or URL rendering without sanitization.
- Error messages, toast messages, or previews that display raw user input unsafely.

### Session / Cookie / CSRF / CORS

Check for:

- Missing `HttpOnly`, `Secure`, or `SameSite` cookie protections where needed.
- State-changing requests that need CSRF protection.
- Overly broad CORS configuration such as unrestricted origins.
- Changes that weaken session expiration, refresh, or rotation behavior.

### Sensitive Data Exposure

Check for:

- Personal data, payment data, internal IDs, tokens, or private metadata returned unnecessarily.
- Sensitive data in logs, errors, analytics, monitoring, or client-side state.
- Sensitive values stored in `localStorage` or `sessionStorage` without a clear reason.
- Stack traces, database details, internal paths, or service metadata exposed to users.

### File Handling

Check for:

- Missing file size, type, extension, or MIME validation.
- File paths built from user-controlled input.
- Path traversal through `../`, absolute paths, symlinks, or encoded path segments.
- Executable or user-uploaded files stored in public locations without protection.
- Download endpoints that return files without authorization checks.

### External API / Network

Check for:

- SSRF risks from user-controlled URLs.
- Missing webhook signature verification.
- Missing timeout, retry limit, or failure handling for external calls.
- External API errors that expose internal state or secrets.
- Costly external calls without limits when abuse is possible.

### Dependency / Supply Chain

Check for:

- New dependencies that are unnecessary or too broad for the Task.
- Unmaintained, unknown, or suspicious packages.
- Unexpected lockfile changes.
- Packages with risky install scripts, native binaries, or unclear provenance.
- Dependency changes that increase client bundle exposure of sensitive code.

### Abuse / Rate Limit

Check for:

- Login, signup, password reset, search, upload, email, payment, or AI calls without abuse protection where relevant.
- Requests that can trigger excessive database work, loops, memory use, or external API cost.
- Missing pagination, size limits, or throttling for expensive operations.

### Workspace Safety

Check for:

- Reads or writes outside the current workspace.
- Use of `../`, absolute paths, home directory paths, or parent project paths.
- Commands that affect global dependencies, global config, OS settings, or unrelated repositories.
- Generated Tasks that require access outside the workspace without explicit user approval.
- Changed files that are not part of the approved Task or Subtask.

## Security Review Output Format

Security findings must use English field names and English category values.
All explanation after the colon must be written in Korean.

Use this format:

```md
- Severity: Blocker | Major | Minor | Approved
- Area: Secrets | Authentication | Access Control | Input Validation | Injection | XSS | Session | Sensitive Data | File Handling | External API | Dependency | Rate Limit | Workspace Safety
- Evidence: 문제가 확인된 파일, 위치, 입력값, 코드 흐름을 한글로 구체적으로 설명합니다.
- Risk: 공격자나 잘못된 사용자가 이 문제를 어떻게 악용할 수 있는지 설명합니다.
- Required Fix: 승인 전에 필요한 보안 수정 사항을 구체적으로 적습니다.
- Retest: 수정 후 어떤 요청, 테스트, 시나리오로 다시 확인해야 하는지 적습니다.
```

Blocker security issues include:

- Hardcoded real secrets.
- Authentication or authorization bypass.
- User data exposure.
- Injection vulnerability.
- Unsafe file access outside the workspace.
- Unapproved destructive operation.
- Dependency change with clear security risk.
