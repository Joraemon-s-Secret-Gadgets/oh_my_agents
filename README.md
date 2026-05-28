# oh_my_agents
에이전트(AI) 협업을 위한 최상위/하위 AGENTS.md 표준 가이드라인 및 워크플로우 관리 저장소

## Codex Skill

팀원은 `skills/oh-my-agents`를 각자 Codex Skill 폴더에 설치해서 사용할 수 있습니다.

```bash
mkdir -p ~/.codex/skills
cp -R skills/oh-my-agents ~/.codex/skills/oh-my-agents
```

새 Codex 세션에서 `$oh-my-agents`를 사용하면, 프로젝트 `AGENTS.md`를 기준으로 Spec/Task/Implementation/Review subagent 생성 흐름을 표준화합니다.
