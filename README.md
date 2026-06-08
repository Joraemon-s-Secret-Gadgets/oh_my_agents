# oh_my_agents
에이전트(AI) 협업을 위한 최상위/하위 AGENTS.md 표준 가이드라인 및 워크플로우 관리 저장소

## Usage Modes

- Plus / 일반 사용: 루트 `AGENTS.md`와 `docs/agents/*`를 필요할 때만 읽는 토큰 절약형 구조를 사용합니다.
- PRO20x 사용: `PRO20x/AGENTS.md`를 사용해 토큰 부담 없이 주요 운영 규칙을 한 파일에서 확인합니다.

## Codex Skill

팀원은 `skills/oh-my-agents`를 각자 Codex Skill 폴더에 설치해서 사용할 수 있습니다.

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

이미 설치되어 있다면 업데이트 시 기존 로컬 Skill을 교체합니다.

```bash
rm -rf ~/.codex/skills/oh-my-agents
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

새 Codex 세션에서 `$oh-my-agents`를 사용하면, 프로젝트 `AGENTS.md`를 기준으로 Spec/Task/Implementation/Review subagent 생성 흐름을 표준화합니다.
