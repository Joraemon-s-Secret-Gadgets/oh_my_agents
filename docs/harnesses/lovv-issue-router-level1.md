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

## 기본 설정

별도 Python 패키지는 필요하지 않습니다. Python 3.10 이상과 표준 라이브러리만 사용합니다.

### 1. GitHub CLI 설치 확인

```bash
gh --version
```

설치되어 있지 않다면 GitHub CLI를 설치합니다.

macOS Homebrew:

```bash
brew install gh
```

Windows:

```powershell
winget install --id GitHub.cli
```

### 2. GitHub 로그인

```bash
gh auth login
```

권장 선택:

- GitHub.com
- HTTPS
- Login with a web browser

로그인 상태를 확인합니다.

```bash
gh auth status
```

### 3. 저장소 clone

```bash
git clone https://github.com/Joraemon-s-Secret-Gadgets/oh_my_agents.git
cd oh_my_agents
```

### 4. Codex Skill 설치

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
cp -R skills/lovv-agent-team-launcher ~/.codex/skills/lovv-agent-team-launcher
```

이미 설치되어 있다면 업데이트 시 기존 로컬 Skill을 교체합니다.

```bash
rm -rf ~/.codex/skills/oh-my-agents ~/.codex/skills/lovv-agent-team-launcher
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
cp -R skills/lovv-agent-team-launcher ~/.codex/skills/lovv-agent-team-launcher
```

### 5. Token 설정 방식

공개 issue는 token 없이도 조회할 수 있습니다. 다만 팀 작업에서는 `gh auth login`을 권장합니다.

harness는 token을 다음 순서로 찾습니다.

1. `GITHUB_TOKEN`
2. `GH_TOKEN`
3. `gh auth token`
4. token 없이 공개 API 요청

직접 token을 환경 변수로 넣어야 한다면 다음처럼 설정합니다.

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

`gh auth token` fallback을 사용하지 않고 공개 API 또는 환경 변수 token만 사용하려면 다음 옵션을 사용합니다.

```bash
python3 scripts/lovv_issue_router.py 123 --no-gh-auth
```

## 출력 예시

실행하면 다음 형태의 Markdown proposal이 출력됩니다.

```md
# Issue Agent Routing Proposal

Issue:
- Repository: `Joraemon-s-Secret-Gadgets/Lovv`
- Issue Number: `#123`
- Title: ...

Recommended Agent:
- Display Name: Frontend Implementation Agent
- Core Role: Implementation Agent
- Domain Focus: Frontend
- Work Focus: Code
- Execution Mode: Hybrid Mode

Structured Agent Contract:
- Goal: ...
- Source of Truth: ...
- Scope:
- Out of Scope:
- Required Context:
- Verification:
- Stop Condition:
```

## 권장 팀 흐름

1. 팀원이 GitHub Issue 번호를 지정합니다.
2. harness가 Issue Routing Proposal을 생성합니다.
3. 사용자가 agent, mode, scope, missing input을 확인합니다.
4. 사용자가 승인하면 Codex 현재 세션 또는 tool-backed subagent harness로 실행합니다.
5. 실행 결과는 issue comment, docs report, 또는 PR description에 수동으로 연결합니다.

실제 subagent team 실행이 필요하면 `docs/harnesses/lovv-agent-team-launcher.md`와 `$lovv-agent-team-launcher` Skill을 사용합니다.

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
