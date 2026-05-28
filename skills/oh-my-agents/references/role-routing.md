# Role Routing

Use this reference when an agent creation request is abstract or mixes domain and focus labels.

## Display Name Format

```md
[Domain] [Focus] [Core Role]
```

Core roles:

- Spec Agent
- Task Agent
- Implementation Agent
- Review Agent

Domain labels:

- General
- Frontend
- Backend
- Full-stack

Focus labels:

- Code
- QA
- Security
- UX
- Performance
- Crawl

## Interpretation Examples

```md
Frontend QA Review Agent
= Core Role: Review Agent
= Domain Focus: Frontend
= Work Focus: QA
```

```md
Backend Security Review Agent
= Core Role: Review Agent
= Domain Focus: Backend
= Work Focus: Security
```

```md
Crawl Implementation Agent
= Core Role: Implementation Agent
= Domain Focus: General unless backend/data scope is explicit
= Work Focus: Crawl
```

## Common Defaults

- If the user says "프론트 리뷰", use Frontend Review Agent.
- If the user says "프론트 QA", use Frontend QA Review Agent.
- If the user says "백엔드 보안", use Backend Security Review Agent.
- If the user says "전체 흐름 검증", use Full-stack QA Review Agent.
- If the user says "크롤링해줘", use Crawl Implementation Agent.
- If the user says "크롤링 결과 검증", use Crawl QA Review Agent.

Do not create new root roles for domain or focus labels. Domain and focus only narrow scope, context, and output expectations.
