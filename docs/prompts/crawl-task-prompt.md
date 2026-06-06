# Crawl Task Prompt Template

Use this prompt when the target URLs are already known and the user will provide the columns to extract.

This is a prompt template, not a persistent agent role. Do not add it to default agent loading context unless the current task is a crawl task.

```md
다음 URL에서 지정한 컬럼만 추출해줘.

## Crawl Task Rules

- Use Python 3.12.
- Implement crawl logic as Python files or scripts inside the workspace.
- Prefer BeautifulSoup for static HTML.
- Use Selenium only when rendering or interaction is required.
- Use Scrapling only when extraction helper is useful.
- Do not add another crawler framework such as Scrapy or Playwright unless the user or approved Task explicitly allows it.
- Use the Python standard library or an already-approved project HTTP client for fetching when BeautifulSoup is used for parsing.
- Crawl only user-provided or Task-approved URLs.
- Extract only user-specified or Task-approved columns.
- Do not invent additional columns.
- Respect robots.txt, terms, rate limits, copyright, and privacy.
- Record source_url, retrieved_at, and failure_reason when applicable.

## Crawl Safety Rules

- Do not bypass login, paywalls, CAPTCHAs, access controls, or anti-abuse protections.
- Do not collect personal data, sensitive data, or copyrighted content beyond the approved columns.
- Use explicit timeouts, retry limits, and exponential backoff for network requests.
- Use a conservative request interval or approved rate limit.
- Do not download binaries, media archives, or large files unless explicitly approved.
- Do not execute scripts from crawled pages.
- Store outputs only inside the project workspace.

## Deep Crawl Rules

- Deep crawling is disabled by default.
- Use deep crawling only when the user or approved Task provides seed URLs, domain allowlist, max depth, max pages, rate limit, output columns, and stop condition.
- Stay within the approved domain allowlist.
- Track visited URLs and avoid repeated requests.
- Stop when max depth, max pages, robots.txt, terms, rate limit, or stop condition is reached.
- Do not add URLs, targets, or columns that were not approved.

## Data Quality Rules

- Validate that every output row matches the approved column schema.
- Include source_url, retrieved_at, and failure_reason when applicable.
- Deduplicate records using the approved key or source_url when no key is provided.
- Record status_code and failure_reason internally for failed requests.
- Provide a small sample output and row count before reporting completion.

## Input URLs

- [URL 1]
- [URL 2]

## Columns

- [column_1]
- [column_2]
- source_url
- retrieved_at
- failure_reason

## Output

- Save as `[output path]`.
- Include one record per URL.
- If extraction fails, fill `failure_reason`.
- Do not add columns that are not listed above.

## Notes

- [Any source-specific rule, selector hint, sample limit, or manual check]
```

## Example

```md
다음 URL에서 지정한 컬럼만 추출해줘.

## Crawl Task Rules

- Use Python 3.12.
- Implement crawl logic as Python files or scripts inside the workspace.
- Prefer BeautifulSoup for static HTML.
- Use Selenium only when rendering or interaction is required.
- Use Scrapling only when extraction helper is useful.
- Do not add another crawler framework such as Scrapy or Playwright unless the user or approved Task explicitly allows it.
- Use the Python standard library or an already-approved project HTTP client for fetching when BeautifulSoup is used for parsing.
- Crawl only user-provided or Task-approved URLs.
- Extract only user-specified or Task-approved columns.
- Do not invent additional columns.
- Respect robots.txt, terms, rate limits, copyright, and privacy.
- Record source_url, retrieved_at, and failure_reason when applicable.

## Crawl Safety Rules

- Do not bypass login, paywalls, CAPTCHAs, access controls, or anti-abuse protections.
- Do not collect personal data, sensitive data, or copyrighted content beyond the approved columns.
- Use explicit timeouts, retry limits, and exponential backoff for network requests.
- Use a conservative request interval or approved rate limit.
- Do not download binaries, media archives, or large files unless explicitly approved.
- Do not execute scripts from crawled pages.
- Store outputs only inside the project workspace.

## Deep Crawl Rules

- Deep crawling is disabled by default.
- Use deep crawling only when the user or approved Task provides seed URLs, domain allowlist, max depth, max pages, rate limit, output columns, and stop condition.
- Stay within the approved domain allowlist.
- Track visited URLs and avoid repeated requests.
- Stop when max depth, max pages, robots.txt, terms, rate limit, or stop condition is reached.
- Do not add URLs, targets, or columns that were not approved.

## Data Quality Rules

- Validate that every output row matches the approved column schema.
- Include source_url, retrieved_at, and failure_reason when applicable.
- Deduplicate records using the approved key or source_url when no key is provided.
- Record status_code and failure_reason internally for failed requests.
- Provide a small sample output and row count before reporting completion.

## Input URLs

- https://example.com/place-1
- https://example.com/place-2

## Columns

- title
- address
- description
- source_url
- retrieved_at
- failure_reason

## Output

- Save as `data/raw/example_places.jsonl`.
- Include one JSON object per URL.
- If extraction fails, fill `failure_reason`.
- Do not add columns that are not listed above.
```
