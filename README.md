# oh_my_agents 프로젝트 가이드

이 저장소는 `AGENTS.md` 기반으로 에이전트 협업 규칙, 역할별 실행 기준, 실행 모드, 재사용 가능한 프롬프트를 관리하기 위한 문서 저장소입니다.

## 중요: AGENTS.md는 Harness가 아닙니다

`AGENTS.md`는 규칙서입니다. 에이전트가 어떻게 기획하고, 구현하고, 리뷰하고, 보안을 점검하고, 작업을 인계해야 하는지를 정의합니다.

하지만 `AGENTS.md` 자체가 독립적인 subagent를 자동으로 생성하거나 실행하거나 관리하지는 않습니다.

`Spec Agent`, `Task Agent`, `Implementation Agent`, `Review Agent`, `Frontend QA Review Agent`, `Backend Security Review Agent` 같은 역할 에이전트를 실제로 생성하거나 작업을 위임하려면 지원되는 agent harness가 필요합니다.

Harness의 예시는 다음과 같습니다.

- 사용자 요청을 해석하고 제한된 agent invocation을 준비하는 Codex Skill, 예: `oh-my-agents`
- 별도 agent context를 만들고, 범위가 제한된 지시를 전달하고, 최종 보고서를 수집하고, 사용하지 않는 agent를 정리할 수 있는 tool-backed subagent system
- 이 저장소의 규칙을 읽고 role, scope, verification, handoff contract를 강제하는 custom orchestration script 또는 service

지원되는 harness가 없다면 현재 Codex 세션이 role activation 방식으로 규칙을 따를 수는 있습니다. 다만 이것은 독립적인 subagent를 실제로 생성하는 것과는 다릅니다.

## Skill 및 실행 방식 요약

이 저장소는 세 가지 실행 계층을 함께 사용합니다.

| 구분 | 역할 | 실제 subagent 생성 여부 |
| --- | --- | --- |
| `scripts/lovv_issue_router.py` | GitHub Issue를 읽고 agent, mode, scope, missing input, `Structured Agent Contract`를 제안하는 Level 1 CLI harness | 생성하지 않음 |
| `$oh-my-agents` Skill | `AGENTS.md` 기준으로 단일 role agent를 라우팅하고 실행 계약을 정리하는 Skill | Codex 환경에 tool-backed harness가 있을 때만 가능 |
| `$lovv-agent-team-launcher` Skill | GitHub Issue 기반으로 Agent Team을 제안하고, 승인 후 실제 subagent team 실행을 시도하는 Skill | Codex 환경에 tool-backed harness가 있을 때만 가능 |

정리하면 다음과 같습니다.

```text
AGENTS.md
= 프로젝트 규칙서

lovv_issue_router.py
= GitHub Issue 기반 routing proposal 생성기

oh-my-agents Skill
= 단일 agent role 라우터

lovv-agent-team-launcher Skill
= agent team proposal / launch 라우터

Codex tool-backed subagent harness
= 실제 subagent를 spawn / wait / close 하는 실행 계층
```

## 작업 방식 선택 기준

| 상황 | 권장 방식 |
| --- | --- |
| Issue를 읽고 어떤 agent가 맞는지만 보고 싶을 때 | `python3 scripts/lovv_issue_router.py <issue>` |
| 단일 역할 agent가 필요할 때 | `$oh-my-agents` |
| 여러 역할이 함께 필요한 기능 작업일 때 | `$lovv-agent-team-launcher` |
| 사용자가 작업할 때 | team proposal을 먼저 보고 승인 후 실행 |
| Owner 전용 파일럿 | `Owner Auto Team`을 명시한 경우에만 자동 team 실행 |

## 사용자용 짧은 호출 규칙

사용자는 긴 prompt를 직접 작성하지 않고, GitHub Issue 번호와 원하는 동작만 입력하는 것을 기본으로 합니다.

| 목적 | 입력 |
| --- | --- |
| 팀 제안만 받기 | `Lovv #123 팀 제안해줘` |
| 승인 후 순차형 시작 | `Lovv #123 제안 승인. 순차형으로 시작해줘` |
| 승인 후 하이브리드 시작 | `Lovv #123 제안 승인. 하이브리드로 시작해줘` |
| Owner 전용 자동 파일럿 | `Owner Auto Team: Lovv #123 하이브리드로 실행해줘` |

이 짧은 입력은 prompt engineering 문장이 아니라 실행 트리거입니다. 실제 작업의 source of truth는 Lovv GitHub Issue 본문, labels, Issue Template 필드, `AGENTS.md`, Skill, harness 규칙입니다.

사용자는 agent team preset이나 세부 role을 직접 맞추려고 하지 않아도 됩니다. Skill과 harness가 Issue의 `Layer`, `Priority`, `완료 조건`, `요구사항 / 수용 기준`, labels를 읽고 적합한 team을 제안해야 합니다.

## 기본 실행 모드

`oh-my-agents`를 사용한다고 해서 기본 실행 모드가 `Sequential Mode`가 되는 것은 아닙니다.

기본 모드 규칙은 다음과 같습니다.

- `Hybrid Mode`: 일반 기능 작업의 기본값입니다.
- `Sequential Mode`: 보안, DB, 인증, 인가, 결제, migration, 되돌리기 어려운 작업, 요구사항이 모호한 작업에 사용합니다.
- `Parallel Mode`: 사용자가 명시적으로 요청했거나 write scope가 명확히 분리되어 결과를 안전하게 통합할 수 있을 때만 사용합니다.

## 권장 사용 흐름

1. 루트 `AGENTS.md`를 읽습니다.
2. 에이전트 역할을 생성하거나 활성화하는 작업이라면 `docs/agents/agent-creation-guidelines.md`를 읽습니다.
3. 사용자의 원문 요청을 `User Request Original`로 보존합니다.
4. 실행 가능한 지시는 영어 `Structured Agent Contract`로 정리합니다.
5. 실행 모드를 하나만 선택합니다.
6. 선택된 역할, 도메인, focus에 필요한 규칙만 읽습니다.
7. 에이전트의 최종 보고를 수집합니다.
8. harness가 지원하는 경우, 사용이 끝났거나 응답이 없는 agent context를 정리합니다.

사용자 작업 흐름은 다음을 기본으로 합니다.

```text
GitHub Issue 선택
-> Issue Router로 routing proposal 생성
-> oh-my-agents 또는 lovv-agent-team-launcher로 실행 방식 제안
-> 사용자 승인
-> subagent harness가 있으면 실제 subagent 실행
-> harness가 없으면 현재 Codex 세션에서 role activation으로 대체
-> 최종 보고 수집
-> 사용이 끝난 agent context 정리
```

## Lovv Issue Router Level 1

사용자가 Lovv GitHub Issue를 기준으로 agent 작업을 시작할 때는 Level 1 harness를 사용할 수 있습니다.

기본 설정은 다음 순서로 진행합니다.

```bash
# 1. GitHub CLI 설치 확인
gh --version

# 2. GitHub 로그인
gh auth login

# 3. 로그인 상태 확인
gh auth status

# 4. 저장소 clone
git clone https://github.com/Joraemon-s-Secret-Gadgets/oh_my_agents.git
cd oh_my_agents
```

`gh auth login`을 완료하면 harness가 `gh auth token`을 통해 GitHub 인증 정보를 자동으로 사용합니다. 공개 issue는 인증 없이도 조회할 수 있지만, 팀 작업에서는 rate limit과 private 권한 문제를 줄이기 위해 `gh` 로그인을 권장합니다.

```bash
python3 scripts/lovv_issue_router.py 123
```

이 harness는 GitHub Issue를 읽고 agent, execution mode, scope, missing input, `Structured Agent Contract`를 제안합니다.

자동으로 구현, branch 생성, commit, PR 생성, issue close를 하지 않습니다. 사용자가 routing proposal을 승인한 뒤에만 실제 작업을 시작합니다.

자세한 사용법은 `docs/harnesses/lovv-issue-router-level1.md`를 참고합니다.

## Lovv Agent Team Launcher

실제 subagent 팀을 실행해야 할 때는 `lovv-agent-team-launcher` Skill을 사용합니다.

```text
Lovv #123 팀 제안해줘
```

Skill을 명시해야 하는 환경에서는 다음처럼 사용할 수 있습니다.

```text
$lovv-agent-team-launcher Lovv #123 팀 제안해줘
```

일반 사용자용 기본 흐름은 `팀 제안 -> 사용자 승인 -> subagent 실행 또는 role activation fallback`입니다.

지원되는 Codex subagent harness가 있으면 실제 subagent를 생성하고, 없으면 현재 세션에서 역할별로 순차 실행합니다.

대표적인 team preset은 다음과 같습니다.

| Team | 쓰는 경우 |
| --- | --- |
| Planning Team | 신규 기능, 요구사항, Spec, Task 분해 |
| Frontend Feature Team | React, Tailwind, UI, route, state, 접근성 |
| Backend API Team | Django, API, DB, migration, validation |
| Security Review Team | auth, token, secret, env, permission |
| Crawl Data Team | crawl, scrape, BeautifulSoup, Selenium, Scrapling |
| Release Gate Team | merge 전 최종 review, QA, security gate |

사용자용 기본 모드에서는 다음 작업을 자동화하지 않습니다.

- branch 생성
- commit 생성
- PR 생성
- issue close
- 승인 없는 implementation 시작

자세한 사용법은 `docs/harnesses/lovv-agent-team-launcher.md`를 참고합니다.

## 주요 파일

- `AGENTS.md`: 루트 프로젝트 에이전트 규칙입니다.
- `AGENTS.ko.md`: 사용자가 이해하기 위한 한국어 설명서입니다.
- `PRO20x/AGENTS.md`: PRO20x 사용자를 위한 full-context 버전입니다.
- `docs/agents/`: 토큰 절약을 위해 분리된 agent rule 파일입니다.
- `docs/agents/modes/`: Sequential, Hybrid, Parallel 실행 모드 문서입니다.
- `docs/harnesses/`: GitHub Issue 기반 harness 같은 팀 운영 도구 문서입니다.
- `docs/prompts/`: crawl prompt 같은 작업별 프롬프트 템플릿입니다.
- `scripts/`: 사용자가 실행할 수 있는 안전한 CLI harness 스크립트입니다.
- `skills/oh-my-agents/`: agent routing과 invocation 지원을 위한 공유 Skill package입니다.
- `skills/lovv-agent-team-launcher/`: 실제 agent team proposal과 subagent launch를 돕는 Skill package입니다.

## Codex Skill 설치

사용자는 공유 Skill을 각자 로컬 Codex Skill 폴더에 설치해서 사용할 수 있습니다.

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
cp -R skills/lovv-agent-team-launcher ~/.codex/skills/lovv-agent-team-launcher
```

이미 설치되어 있다면 업데이트할 때 기존 로컬 Skill을 교체합니다.

```bash
rm -rf ~/.codex/skills/oh-my-agents ~/.codex/skills/lovv-agent-team-launcher
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
cp -R skills/lovv-agent-team-launcher ~/.codex/skills/lovv-agent-team-launcher
```

새 Codex 세션에서 `$oh-my-agents`를 사용하면 프로젝트 `AGENTS.md`를 기준으로 Spec, Task, Implementation, Review agent routing 흐름을 표준화할 수 있습니다.

실제 agent team 실행이 필요하면 새 Codex 세션에서 `$lovv-agent-team-launcher`를 사용합니다.

## 팀 사용 팁

에이전트를 요청할 때는 가능한 한 먼저 Lovv GitHub Issue Template을 충실히 작성합니다.

짧은 호출만으로 판단하기 어려우면 agent 또는 harness는 추측하지 않고 부족한 입력만 짧게 질문해야 합니다.
