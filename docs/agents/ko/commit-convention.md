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
