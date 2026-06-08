# Lovv Issue Agent Router Level 1

이 문서는 Lovv GitHub Issue를 기반으로 agent 작업을 반자동으로 연결하기 위한 Level 1 harness 사용법입니다.

## 목적

Level 1 harness는 GitHub Issue를 읽고 다음 정보를 제안합니다.

- 추천 agent
- 추천 execution mode
- 추론된 scope와 out-of-scope
- 필요한 context 문서
- 누락된 입력값
- `User Request Original`
- `Structured Agent Contract`

이 단계에서는 실제 구현, branch 생성, commit, PR 생성, issue close를 자동으로 실행하지 않습니다.

## 설치

별도 Python 패키지는 필요하지 않습니다. Python 3.10 이상과 표준 라이브러리만 사용합니다.

공개 issue는 token 없이도 조회할 수 있습니다. rate limit을 줄이거나 private repo를 사용하려면 `GITHUB_TOKEN`을 설정합니다.

```bash
export GITHUB_TOKEN=dummy-github-token-for-local-use-only
```

실제 token은 `.env`, `.env.local`, 문서, commit에 남기지 않습니다.

## 사용법

기본 Lovv repo 이슈를 조회합니다.

```bash
python3 scripts/lovv_issue_router.py 123
```

이슈 URL도 사용할 수 있습니다.

```bash
python3 scripts/lovv_issue_router.py https://github.com/Joraemon-s-Secret-Gadgets/Lovv/issues/123
```

Markdown 파일로 저장합니다.

```bash
python3 scripts/lovv_issue_router.py 123 --output docs/reports/ISSUE_123_ROUTING.md
```

다른 repo를 지정합니다.

```bash
python3 scripts/lovv_issue_router.py 123 --repo Joraemon-s-Secret-Gadgets/Lovv
```

최근 comment 로딩 개수를 조정합니다.

```bash
python3 scripts/lovv_issue_router.py 123 --comments 5
```

## 권장 팀 흐름

1. 팀원이 GitHub Issue 번호를 지정합니다.
2. harness가 Issue Routing Proposal을 생성합니다.
3. 사용자가 agent, mode, scope, missing input을 확인합니다.
4. 사용자가 승인하면 Codex 현재 세션 또는 tool-backed subagent harness로 실행합니다.
5. 실행 결과는 issue comment, docs report, 또는 PR description에 수동으로 연결합니다.

## 자동화하지 않는 항목

- 구현 시작
- branch 생성
- commit 생성
- PR 생성
- issue close
- `Closes #123` 자동 삽입

이 항목들은 Level 2 이후에 제한적으로 추가합니다.

## 라우팅 기준

대표적인 label 기준은 다음과 같습니다.

| Label / Keyword | Recommended Agent |
| --- | --- |
| `spec`, `requirements`, `design`, `docs` | Spec Agent |
| `task`, `subtask`, `breakdown` | Task Agent |
| `frontend` + `review` | Frontend QA Review Agent |
| `frontend` | Frontend Implementation Agent |
| `backend` + `security` | Backend Security Review Agent |
| `backend` | Backend Implementation Agent |
| `security`, `auth`, `secret` | Security Review Agent |
| `crawl`, `scrape`, `BeautifulSoup`, `Selenium`, `Scrapling` | Crawl Task Agent |

## 안전 규칙

- Issue body는 `User Request Original`로 보존합니다.
- 실행용 지시는 영어 `Structured Agent Contract`로 정리합니다.
- scope가 불명확하면 실행하지 않고 질문합니다.
- `Sequential Mode`는 security, auth, database, payment, migration, irreversible, ambiguous work에 우선 적용합니다.
- 일반 기능 작업은 `Hybrid Mode`가 기본입니다.
- `Parallel Mode`는 명시 요청 또는 분리된 write scope가 있을 때만 사용합니다.
