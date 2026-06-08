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

## 주요 파일

- `AGENTS.md`: 루트 프로젝트 에이전트 규칙입니다.
- `AGENTS.ko.md`: 팀원이 이해하기 위한 한국어 설명서입니다.
- `PRO20x/AGENTS.md`: PRO20x 사용자를 위한 full-context 버전입니다.
- `docs/agents/`: 토큰 절약을 위해 분리된 agent rule 파일입니다.
- `docs/agents/modes/`: Sequential, Hybrid, Parallel 실행 모드 문서입니다.
- `docs/prompts/`: crawl prompt 같은 작업별 프롬프트 템플릿입니다.
- `skills/oh-my-agents/`: agent routing과 invocation 지원을 위한 공유 Skill package입니다.

## Codex Skill 설치

팀원은 공유 Skill을 각자 로컬 Codex Skill 폴더에 설치해서 사용할 수 있습니다.

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

이미 설치되어 있다면 업데이트할 때 기존 로컬 Skill을 교체합니다.

```bash
rm -rf ~/.codex/skills/oh-my-agents
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

새 Codex 세션에서 `$oh-my-agents`를 사용하면 프로젝트 `AGENTS.md`를 기준으로 Spec, Task, Implementation, Review agent routing 흐름을 표준화할 수 있습니다.

## 팀 사용 팁

에이전트를 요청할 때는 가능하면 role, goal, source of truth, scope, out-of-scope behavior, verification command, expected output format을 함께 적는 것이 좋습니다.

이 정보가 부족하면 agent 또는 harness는 추측하지 않고 짧은 clarification question으로 필요한 내용을 확인해야 합니다.
