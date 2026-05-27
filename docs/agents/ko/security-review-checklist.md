## Security Review Checklist

보안 리뷰는 모든 작업에 같은 강도로 적용할 필요는 없습니다.

하지만 다음 영역을 건드리는 작업이면 반드시 세부 보안 점검을 해야 합니다.

- 인증
- 권한
- 사용자 입력
- 파일 처리
- 외부 API
- dependency
- 설정
- 데이터 저장
- 로그
- workspace 작업

주요 점검 영역은 다음과 같습니다.

### Secrets / Credentials

API key, token, password, private key 같은 값이 코드, 로그, 설정, 테스트 데이터에 들어가지 않았는지 확인합니다.

또한 `.env` 관련 파일이 `.gitignore`에서 누락되어 커밋 대상에 포함될 위험이 없는지 확인합니다. 실제 secret은 Git에 올리지 않고, 공유가 필요한 경우 `.env.example`에 더미 값으로 구조만 남깁니다.

### Authentication

로그인, 세션, 토큰 검증이 누락되지 않았는지 확인합니다.

### Authorization / Access Control

로그인 여부와 리소스 접근 권한을 구분해서 확인합니다. 가장 중요한 보안 점검 영역입니다.

### Input Validation

사용자 입력, URL parameter, request body, header, 파일명, 외부 API 응답을 검증하는지 확인합니다.

### Injection

SQL, shell command, dynamic code execution, template 생성 등에 외부 입력이 안전하지 않게 들어가지 않는지 확인합니다.

### XSS / Client-Side Safety

사용자 입력을 HTML, markdown, iframe, URL 등으로 렌더링할 때 안전한지 확인합니다.

### Session / Cookie / CSRF / CORS

쿠키 보안 설정, CSRF 방어, CORS 범위, 세션 만료 정책이 약해지지 않았는지 확인합니다.

### Sensitive Data Exposure

개인정보, 토큰, 내부 ID, stack trace, DB 정보, 내부 경로가 응답이나 로그에 노출되지 않는지 확인합니다.

### File Handling

파일 업로드, 다운로드, 경로 조합에서 path traversal, 권한 누락, public 노출 위험이 없는지 확인합니다.

### External API / Network

외부 URL 호출, webhook, timeout, retry, rate limit, SSRF 위험을 확인합니다.

### Dependency / Supply Chain

새 dependency가 꼭 필요한지, 신뢰 가능한지, lockfile 변경이 의도된 것인지 확인합니다.

### Abuse / Rate Limit

로그인, 회원가입, 업로드, 검색, AI 호출 등 남용 가능성이 있는 기능에 제한이 필요한지 확인합니다.

### Workspace Safety

현재 프로젝트 밖 파일을 읽거나 쓰지 않는지, `../` 또는 absolute path로 workspace boundary를 우회하지 않는지 확인합니다.
