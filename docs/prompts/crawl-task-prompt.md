# Crawl Task Prompt Template

Use this prompt when the target URLs are already known and the user will provide the columns to extract.

This is a prompt template, not a persistent agent role. Do not add it to default agent loading context unless the current task is a crawl task.

```md
다음 URL에서 지정한 컬럼만 추출해줘.

## Crawl Task Rules

- Use Python 3.12.
- Prefer BeautifulSoup for static HTML.
- Use Selenium only when rendering or interaction is required.
- Use Scrapling only when extraction helper is useful.
- Crawl only user-provided or Task-approved URLs.
- Extract only user-specified or Task-approved columns.
- Do not invent additional columns.
- Respect robots.txt, terms, rate limits, copyright, and privacy.
- Record source_url, retrieved_at, and failure_reason when applicable.

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
- Prefer BeautifulSoup for static HTML.
- Use Selenium only when rendering or interaction is required.
- Use Scrapling only when extraction helper is useful.
- Crawl only user-provided or Task-approved URLs.
- Extract only user-specified or Task-approved columns.
- Do not invent additional columns.
- Respect robots.txt, terms, rate limits, copyright, and privacy.
- Record source_url, retrieved_at, and failure_reason when applicable.

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
