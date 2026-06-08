# Lovv Agent Team Launcher

이 문서는 팀원이 실제 subagent 팀을 실행할 때 사용하는 `lovv-agent-team-launcher` Skill 사용법입니다.

## 목적

`lovv-agent-team-launcher`는 GitHub Issue 기반으로 필요한 agent team을 제안하고, 사용자가 승인하면 지원되는 Codex subagent harness를 통해 실제 subagent를 실행하도록 돕습니다.

이 Skill은 permanent agent를 계속 띄워두는 도구가 아닙니다. 필요할 때 team preset을 선택하고, 실행 후 agent context를 정리하는 on-demand launcher입니다.

## 전제

- `oh-my-agents` Skill이 설치되어 있어야 합니다.
- `lovv-agent-team-launcher` Skill이 설치되어 있어야 합니다.
- 가능하면 GitHub CLI `gh` 로그인이 되어 있어야 합니다.
- 실제 subagent 생성은 Codex 환경에 tool-backed subagent harness가 있을 때만 가능합니다.
- harness가 없으면 현재 Codex 세션에서 role activation 방식으로 대체합니다.

## 설치

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
cp -R skills/lovv-agent-team-launcher ~/.codex/skills/lovv-agent-team-launcher
```

업데이트 시 기존 로컬 Skill을 교체합니다.

```bash
rm -rf ~/.codex/skills/oh-my-agents ~/.codex/skills/lovv-agent-team-launcher
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
cp -R skills/lovv-agent-team-launcher ~/.codex/skills/lovv-agent-team-launcher
```

## 사용 예시

팀원은 긴 prompt 대신 아래 짧은 호출을 기본으로 사용합니다.

| 목적 | 입력 |
| --- | --- |
| 팀 제안만 받기 | `Lovv #123 팀 제안해줘` |
| 승인 후 순차형 시작 | `Lovv #123 제안 승인. 순차형으로 시작해줘` |
| 승인 후 하이브리드 시작 | `Lovv #123 제안 승인. 하이브리드로 시작해줘` |
| Owner 전용 자동 파일럿 | `Owner Auto Team: Lovv #123 하이브리드로 실행해줘` |

일반 팀원용 기본 호출:

```text
Lovv #123 팀 제안해줘
```

Skill을 명시해야 하는 환경에서는 다음처럼 사용할 수 있습니다.

```text
$lovv-agent-team-launcher Lovv #123 팀 제안해줘
```

팀 변경 요청:

```text
Security Review Team도 포함해서 다시 제안해줘
```

Owner 전용 파일럿:

```text
Owner Auto Team: Lovv #123 하이브리드로 실행해줘
```

## 기본 흐름

1. Issue Router로 GitHub Issue를 읽습니다.
2. `User Request Original`과 `Structured Agent Contract`를 만듭니다.
3. Team preset을 선택합니다.
4. Team proposal을 사용자에게 보여줍니다.
5. 사용자가 승인하면 실제 subagent 생성 또는 role activation fallback을 진행합니다.
6. 모든 agent final report를 취합합니다.
7. 사용하지 않는 agent context를 정리합니다.

## Team Preset

| Team | 쓰는 경우 |
| --- | --- |
| Planning Team | 신규 기능, 요구사항, Spec, Task 분해 |
| Frontend Feature Team | React, Tailwind, UI, route, state, 접근성 |
| Backend API Team | Django, API, DB, migration, validation |
| Security Review Team | auth, token, secret, env, permission |
| Crawl Data Team | crawl, scrape, BeautifulSoup, Selenium, Scrapling |
| Release Gate Team | merge 전 최종 review, QA, security gate |

## 자동화하지 않는 항목

팀원용 기본 모드에서는 다음을 자동화하지 않습니다.

- branch 생성
- commit 생성
- PR 생성
- issue close
- `Closes #123` 자동 삽입
- 승인 없는 implementation 시작

Owner Auto Team Pilot에서도 commit, push, PR, issue close는 자동화하지 않습니다.

## 안전 규칙

- write scope가 겹치는 subagent는 동시에 실행하지 않습니다.
- 최대 2~3개 subagent부터 시작합니다.
- security, auth, DB, migration은 Sequential Mode를 우선합니다.
- frontend/backend/crawl scope가 명확하지 않으면 먼저 질문합니다.
- 최종 보고를 받은 뒤 subagent context를 정리합니다.
