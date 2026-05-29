## Git Commit Convention Details

`Git Commit Convention Details`는 커밋 메시지를 작성할 때 따르는 세부 규칙입니다.

공식 기준은 Conventional Commits 1.0.0입니다.

공식 문서: https://www.conventionalcommits.org/en/v1.0.0/

기본 구조는 다음과 같습니다.

```md
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

각 구간의 의미는 다음과 같습니다.

- Header: 첫 줄인 `<type>(<optional scope>): <description>`이며, 이 커밋이 무엇인지 한 줄로 요약합니다.
- Body: 한 줄을 비운 뒤 전체 변경 맥락, 주요 변경 내용, 구현 메모, 검증 내용을 자세히 설명합니다.
- Footer: 한 줄을 비운 뒤 메타데이터를 적습니다. 해당 작업과 연결된 GitHub 이슈가 있으면 `Refs: #123`, `Closes: #123`, `Fixes: #123` 같은 형식으로 이슈 번호를 추가합니다.

작성 규칙은 다음과 같습니다.

- 각 커밋은 가능하면 하나의 완료된 `Subtask`에 대응해야 합니다.
- 커밋 메시지는 반드시 `type`으로 시작합니다.
- `feat`는 새로운 기능 추가에 사용하며 Semantic Versioning의 MINOR 변경과 연결됩니다.
- `fix`는 버그 수정에 사용하며 Semantic Versioning의 PATCH 변경과 연결됩니다.
- 그 외에 `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build` 등을 변경 성격에 맞게 사용할 수 있습니다.
- `scope`는 선택 사항이며 변경이 일어난 모듈이나 위치를 소괄호 안에 적습니다. 예: `feat(auth):`, `fix(api):`
- `description`은 type 또는 scope 뒤의 콜론과 공백 다음에 바로 작성합니다.
- `description`은 간결한 한 줄 요약이어야 하며, 대문자로 시작하지 않고 마침표로 끝나지 않아야 합니다.
- 추가 설명이 필요하면 한 줄을 비운 뒤 body를 작성할 수 있습니다.
- footer는 한 줄을 비운 뒤 git trailer 형식으로 작성합니다.
- 해당 Task 또는 Subtask에 연결된 GitHub 이슈가 있으면 footer에 이슈 번호를 포함합니다.
- 하위 호환성이 깨지는 변경은 `feat!:` 또는 `feat(api)!:`처럼 type 또는 scope 뒤에 `!`를 붙이거나, footer에 `BREAKING CHANGE:`를 반드시 명시합니다.
- footer token으로 사용할 때 `BREAKING CHANGE`는 반드시 대문자로 작성합니다.

## Commit Operation Guidelines

커밋은 현재 Task 또는 Subtask가 구현되고, 로컬 검증이 끝났으며, handoff 또는 기록 가능한 상태가 되었을 때만 생성합니다.

## Git Operation Ownership

이 프로젝트에는 별도 Git Agent를 두지 않습니다.

repository history 또는 remote state에 영향을 주는 Git 작업은 Main Codex가 최종 책임을 집니다. 여기에는 staging, commit, pull, push, branch switching, merge, rebase, pull request creation이 포함됩니다.

역할 subagent는 변경 파일 보고, commit message 제안, commit readiness 리뷰를 할 수 있지만, 사용자가 명시적으로 승인하고 Main Codex가 위임하지 않는 한 history 또는 remote를 변경하는 Git 명령을 실행하면 안 됩니다.

Implementation Agent는 자신의 변경을 직접 commit하거나 push하면 안 됩니다.

Review Agent는 리뷰한 변경을 직접 commit하거나 push하면 안 됩니다.

스테이징 전 확인 사항은 다음과 같습니다.

- `git status --short`를 실행하고 변경, staged, untracked, deleted 파일을 모두 확인합니다.
- 가능하면 `git diff --check` 또는 동등한 whitespace/conflict marker 검사를 실행합니다.
- `.env`, `.env.local`, 실제 credential 파일, 로컬 DB, 생성된 secret, 개인 로컬 머신 파일이 staged 상태가 아닌지 확인합니다.
- 환경 파일이나 생성 파일이 관련되어 있으면 `.gitignore`를 확인합니다.
- 변경 파일이 승인된 Task/Subtask 범위에 속하는지 확인합니다.

스테이징 규칙은 다음과 같습니다.

- `git add path/to/file`처럼 명시적인 경로 staging을 우선합니다.
- 변경 파일 목록을 모두 확인했고 모든 파일이 의도된 경우가 아니라면 `git add .` 같은 광범위 staging을 사용하지 않습니다.
- 사용자나 다른 에이전트의 관련 없는 변경을 staging하지 않습니다.
- Task에 의도적으로 포함된 것이 아니라면 생성 산출물을 staging하지 않습니다.
- 대용량 로그, 빌드 결과물, 캐시, 로컬 DB, dependency 폴더를 staging하지 않습니다.

커밋 시점은 다음과 같습니다.

- 불명확하거나 실패 중인 작업 중간이 아니라, 하나의 일관된 Subtask가 완료되었을 때 커밋합니다.
- 검증을 실행하지 못했다면 commit body 또는 handoff report에 이유를 적습니다.
- Task가 막힌 상태라면 사용자가 명시적으로 WIP commit을 요청하지 않는 한, 커밋보다 handoff note 또는 run log를 우선합니다.
- 파일이 바뀌었다는 이유만으로 커밋하지 않습니다. 변경은 review 가능한 범위여야 합니다.

Commit body 작성 기준은 다음과 같습니다.

- header만으로 변경 맥락이 충분하지 않을 때 body를 사용합니다.
- 주요 구현 메모, 검증 결과, 중요한 제약을 포함합니다.
- 다음 에이전트나 리뷰어가 이해할 수 있을 만큼 충분히 쓰되 장황하게 쓰지 않습니다.

Footer 작성 기준은 다음과 같습니다.

- 연결된 이슈가 있으면 `Refs: #123`, `Closes: #123`, `Fixes: #123` 같은 metadata를 포함합니다.
- 하위 호환성이 깨지면 `BREAKING CHANGE:`를 포함합니다.
- 이슈 번호나 외부 참조를 임의로 만들지 않습니다.

푸시 전 확인 사항은 다음과 같습니다.

- working tree가 clean 상태이거나, 의도적으로 커밋하지 않은 관련 없는 사용자 변경만 남아 있는지 확인합니다.
- target branch와 remote를 확인합니다.
- push가 공유 작업에 영향을 줄 수 있으면 사용자 보고에 branch와 commit hash를 포함합니다.

다음 경우에는 커밋하지 않습니다.

- 실제 secret 또는 환경 파일이 staged 상태입니다.
- 사용자가 승인하지 않은 관련 없는 파일이 포함되어 있습니다.
- 테스트나 검사가 실패했고 그 이유가 설명되지 않았습니다.
- 구현 범위가 모호합니다.
- 사용자가 명시적으로 커밋하지 말라고 했습니다.

예시는 다음과 같습니다.

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
