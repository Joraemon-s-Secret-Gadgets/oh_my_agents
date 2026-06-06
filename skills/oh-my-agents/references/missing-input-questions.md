# Missing Input Questions

Ask at most three questions. Prefer the smallest set needed to safely create the subagent.

## Implementation Agent

```md
Implementation Agent를 생성하려면 범위를 안전하게 제한해야 합니다.

1. 구현할 Task/Subtask ID는 무엇인가요?
2. 수정 가능한 파일 또는 폴더 범위는 어디까지인가요?
3. 완료 후 실행해야 할 검증 명령이 있나요?
```

## Review Agent

```md
Review Agent를 생성하려면 리뷰 대상을 확정해야 합니다.

1. 리뷰할 변경 파일, 브랜치, PR, 또는 diff는 무엇인가요?
2. 기준이 되는 Spec/Task 문서는 어디인가요?
3. 리뷰 초점은 Code, QA, Security, UX 중 무엇인가요?
```

## Frontend Domain

```md
Frontend Agent를 생성하려면 UI 범위를 안전하게 제한해야 합니다.

1. 대상 frontend 파일/폴더 또는 route/component 범위는 어디인가요?
2. 반드시 처리해야 할 UI 상태와 API/data 가정은 무엇인가요?
3. 검증 명령 또는 browser check 기준은 무엇인가요?
```

## Spec Agent

```md
Spec Agent를 생성하려면 기능 의도를 확정해야 합니다.

1. 만들 기능이나 해결할 문제는 무엇인가요?
2. 주요 사용자는 누구인가요?
3. 반드시 제외하거나 지켜야 할 제약이 있나요?
```

## Task Agent

```md
Task Agent를 생성하려면 승인된 기준 문서가 필요합니다.

1. 기준이 되는 승인된 Spec 경로는 어디인가요?
2. 어느 정도 단위로 Subtask를 쪼개면 좋을까요?
3. 다음 Task 번호가 정해져 있나요?
```

## Crawl Focus

```md
Crawl Implementation Agent를 생성하려면 수집 범위를 확정해야 합니다.

1. 크롤링할 URL 목록은 무엇인가요?
2. 수집할 컬럼은 무엇인가요?
3. 결과 파일 형식과 저장 경로는 어떻게 할까요?
```

## Deep Crawl Focus

```md
Deep Crawl 작업은 범위를 더 강하게 제한해야 합니다.

1. seed URL과 허용 domain allowlist는 무엇인가요?
2. max depth, max pages, rate limit은 어떻게 제한할까요?
3. output columns, output path, stop condition은 무엇인가요?
```
