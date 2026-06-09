#!/usr/bin/env python3
"""Level 1 semi-automatic GitHub Issue router for Lovv agent work.

This script reads one GitHub Issue and produces a Markdown routing proposal.
It does not start implementation, create branches, commit, open PRs, or close
issues. It is intentionally a safe planning harness.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


DEFAULT_REPO = "Joraemon-s-Secret-Gadgets/Lovv"
API_BASE = "https://api.github.com"


@dataclass(frozen=True)
class RoutingDecision:
    display_name: str
    core_role: str
    domain_focus: str
    work_focus: str
    execution_mode: str
    scope: list[str]
    out_of_scope: list[str]
    required_context: list[str]
    output_format: str
    verification: list[str]
    stop_conditions: list[str]
    missing_inputs: list[str]


def parse_issue_number(raw: str) -> int:
    """Accept '#123', '123', or a GitHub issue URL."""
    match = re.search(r"(?:issues/|#)?(\d+)$", raw.strip())
    if not match:
        raise ValueError(f"Cannot parse issue number from: {raw}")
    return int(match.group(1))


def normalize_label(label: str) -> str:
    return label.strip().lower().replace("_", "-")


def resolve_github_token(token_env: str = "GITHUB_TOKEN", use_gh_auth: bool = True) -> str | None:
    """Resolve a GitHub token from env first, then from `gh auth token`.

    Public issues can be read without a token, so failures here intentionally
    fall back to unauthenticated API requests.
    """
    token = os.environ.get(token_env) or os.environ.get("GH_TOKEN")
    if token:
        return token
    if not use_gh_auth:
        return None
    try:
        completed = subprocess.run(
            ["gh", "auth", "token"],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    gh_token = completed.stdout.strip()
    return gh_token or None


def fetch_json(url: str, token: str | None = None) -> Any:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "lovv-issue-router-level1",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API error {error.code}: {body}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"GitHub API request failed: {error.reason}") from error


def get_issue(repo: str, issue_number: int, token: str | None = None) -> dict[str, Any]:
    owner_repo = urllib.parse.quote(repo, safe="/")
    url = f"{API_BASE}/repos/{owner_repo}/issues/{issue_number}"
    issue = fetch_json(url, token)
    if "pull_request" in issue:
        raise RuntimeError(f"#{issue_number} is a pull request, not a plain issue.")
    return issue


def get_comments(
    repo: str,
    issue_number: int,
    token: str | None = None,
    limit: int = 3,
) -> list[dict[str, Any]]:
    if limit <= 0:
        return []
    owner_repo = urllib.parse.quote(repo, safe="/")
    url = f"{API_BASE}/repos/{owner_repo}/issues/{issue_number}/comments?per_page={min(limit, 30)}"
    comments = fetch_json(url, token)
    return comments[-limit:]


def label_names(issue: dict[str, Any]) -> list[str]:
    return [normalize_label(label.get("name", "")) for label in issue.get("labels", [])]


def text_blob(issue: dict[str, Any]) -> str:
    body = issue.get("body") or ""
    title = issue.get("title") or ""
    labels = " ".join(label_names(issue))
    return f"{title}\n{body}\n{labels}".lower()


def has_any(values: set[str], candidates: set[str]) -> bool:
    return bool(values.intersection(candidates))


def contains_any(text: str, candidates: tuple[str, ...]) -> bool:
    return any(candidate in text for candidate in candidates)


def choose_agent(issue: dict[str, Any]) -> tuple[str, str, str, str]:
    labels = set(label_names(issue))
    blob = text_blob(issue)

    is_frontend = has_any(labels, {"frontend", "front", "ui", "react", "tailwind"}) or contains_any(
        blob, ("frontend", "front", "ui", "react", "tailwind", "화면", "프론트", "컴포넌트")
    )
    is_backend = has_any(
        labels,
        {"backend", "api", "lambda", "sam", "api-gateway", "db", "database", "server"},
    ) or contains_any(
        blob,
        (
            "backend",
            "api",
            "lambda",
            "sam",
            "api gateway",
            "api-gateway",
            "database",
            "db",
            "서버",
            "백엔드",
        ),
    )
    is_security = has_any(labels, {"security", "auth", "secret"}) or contains_any(
        blob, ("security", "auth", "token", "secret", "password", "보안", "인증", "인가")
    )
    is_review = has_any(labels, {"review", "qa", "test", "testing"}) or contains_any(
        blob, ("review", "qa", "test", "검토", "리뷰", "테스트")
    )
    is_crawl = has_any(labels, {"crawl", "scrape", "crawler"}) or contains_any(
        blob, ("crawl", "scrape", "beautifulsoup", "selenium", "scrapling", "크롤", "수집")
    )

    if is_crawl:
        return ("Crawl Task Agent", "Implementation Agent", "Crawl", "Crawl")
    if is_security and is_frontend:
        return ("Frontend Security Review Agent", "Review Agent", "Frontend", "Security")
    if is_security and is_backend:
        return ("Backend Security Review Agent", "Review Agent", "Backend", "Security")
    if is_security:
        return ("Security Review Agent", "Review Agent", "General", "Security")
    if is_review and is_frontend:
        return ("Frontend QA Review Agent", "Review Agent", "Frontend", "QA")
    if is_review and is_backend:
        return ("Backend API Review Agent", "Review Agent", "Backend", "QA")
    if has_any(labels, {"spec", "requirements", "design", "docs"}) or contains_any(
        blob, ("spec", "requirement", "design", "기획", "명세", "요구사항")
    ):
        return ("Spec Agent", "Spec Agent", "General", "Planning")
    if has_any(labels, {"task", "subtask", "breakdown"}) or contains_any(
        blob, ("task", "subtask", "breakdown", "작업", "쪼개")
    ):
        return ("Task Agent", "Task Agent", "General", "Planning")
    if is_frontend:
        return ("Frontend Implementation Agent", "Implementation Agent", "Frontend", "Code")
    if is_backend:
        return ("Backend Implementation Agent", "Implementation Agent", "Backend", "Code")
    return ("Spec Agent", "Spec Agent", "General", "Planning")


def choose_execution_mode(issue: dict[str, Any], core_role: str, work_focus: str) -> str:
    labels = set(label_names(issue))
    blob = text_blob(issue)
    if has_any(labels, {"parallel"}) or contains_any(blob, ("parallel", "병렬")):
        return "Parallel Mode"
    if work_focus == "Security" or has_any(labels, {"security", "auth", "db", "database", "migration"}):
        return "Sequential Mode"
    if contains_any(
        blob,
        (
            "security",
            "auth",
            "authorization",
            "payment",
            "migration",
            "database",
            "보안",
            "인증",
            "인가",
            "결제",
            "마이그레이션",
        ),
    ):
        return "Sequential Mode"
    if core_role in {"Spec Agent", "Task Agent"} and not issue.get("body"):
        return "Sequential Mode"
    return "Hybrid Mode"


def infer_scope(issue: dict[str, Any], domain_focus: str, work_focus: str) -> list[str]:
    labels = set(label_names(issue))
    scope: list[str] = []
    if domain_focus == "Frontend":
        scope.extend(["frontend/", "docs/specs/ when planning output is needed"])
    elif domain_focus == "Backend":
        scope.extend(["backend/ or api/ or sam/", "database/ or SQL/data-access files when API or data changes are involved"])
    elif domain_focus == "Crawl" or work_focus == "Crawl":
        scope.extend(["scripts/ or backend/ crawl-related files", "docs/prompts/crawl-task-prompt.md"])
    elif has_any(labels, {"docs", "spec", "task"}):
        scope.append("docs/")
    else:
        scope.append("TBD: ask user for target files, folders, or behavior")
    return scope


def required_context(domain_focus: str, core_role: str, work_focus: str, execution_mode: str) -> list[str]:
    context = [
        "AGENTS.md",
        "docs/projects/lovv-project-context.md",
        "docs/agents/agent-creation-guidelines.md",
        f"docs/agents/modes/{execution_mode.split()[0].lower()}.md",
    ]
    if domain_focus == "Frontend":
        context.append("docs/agents/frontend-agent-rules.md")
    if core_role == "Review Agent":
        context.append("docs/agents/review-format.md")
    if work_focus == "Security":
        context.append("docs/agents/security-review-checklist.md")
    if work_focus == "Crawl":
        context.append("docs/prompts/crawl-task-prompt.md")
    if core_role in {"Spec Agent", "Task Agent"}:
        context.append("docs/agents/spec-task-format.md")
    return context


def missing_inputs(issue: dict[str, Any], core_role: str, domain_focus: str, scope: list[str]) -> list[str]:
    missing: list[str] = []
    labels = set(label_names(issue))
    if "TBD: ask user for target files, folders, or behavior" in scope:
        missing.append("작업 대상 파일, 폴더, 또는 사용자-visible behavior 범위")
    if core_role == "Implementation Agent":
        missing.append("검증 명령어 또는 수동 검증 기준")
    if core_role == "Review Agent":
        missing.append("리뷰 대상 diff, branch, PR, 또는 changed files")
    if domain_focus == "Crawl":
        missing.append("수집 URL, 컬럼, 출력 경로, stop condition")
    if not issue.get("body"):
        missing.append("이슈 본문에 목표, 완료 조건, 제약 사항")
    if not labels:
        missing.append("agent 라우팅을 위한 labels: frontend/backend/review/security/spec/task 등")
    return missing[:3]


def make_decision(issue: dict[str, Any]) -> RoutingDecision:
    display_name, core_role, domain_focus, work_focus = choose_agent(issue)
    execution_mode = choose_execution_mode(issue, core_role, work_focus)
    scope = infer_scope(issue, domain_focus, work_focus)
    return RoutingDecision(
        display_name=display_name,
        core_role=core_role,
        domain_focus=domain_focus,
        work_focus=work_focus,
        execution_mode=execution_mode,
        scope=scope,
        out_of_scope=[
            "Do not start implementation before user approval.",
            "Do not create branches, commits, PRs, or close issues automatically.",
            "Do not touch files outside the approved scope.",
        ],
        required_context=required_context(domain_focus, core_role, work_focus, execution_mode),
        output_format=(
            "Routing proposal first. After user approval, use the role-specific final report format."
        ),
        verification=[
            "Level 1 routing only: verify issue metadata, inferred agent, mode, scope, and missing inputs.",
            "No code verification is run before user approval.",
        ],
        stop_conditions=[
            "Stop before implementation, branch creation, commit, PR creation, or issue close.",
            "Stop and ask the user if scope, verification, or source of truth is ambiguous.",
            "Stop if GitHub API data cannot be fetched or the issue is a pull request.",
        ],
        missing_inputs=missing_inputs(issue, core_role, domain_focus, scope),
    )


def blockquote(text: str) -> str:
    if not text.strip():
        return "> _No issue body provided._"
    return "\n".join(f"> {line}" if line else ">" for line in text.strip().splitlines())


def comment_snippets(comments: list[dict[str, Any]]) -> str:
    if not comments:
        return "- No comments loaded."
    lines: list[str] = []
    for comment in comments:
        user = comment.get("user", {}).get("login", "unknown")
        body = (comment.get("body") or "").strip().replace("\n", " ")
        snippet = textwrap.shorten(body, width=220, placeholder="...")
        lines.append(f"- {user}: {snippet}")
    return "\n".join(lines)


def render_markdown(repo: str, issue: dict[str, Any], decision: RoutingDecision, comments: list[dict[str, Any]]) -> str:
    labels = ", ".join(label.get("name", "") for label in issue.get("labels", [])) or "none"
    assignees = ", ".join(user.get("login", "") for user in issue.get("assignees", [])) or "none"
    milestone = issue.get("milestone", {}) or {}
    milestone_title = milestone.get("title", "none")
    issue_number = issue.get("number")
    issue_url = issue.get("html_url", f"https://github.com/{repo}/issues/{issue_number}")

    def list_items(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items)

    missing = list_items(decision.missing_inputs) if decision.missing_inputs else "- None"

    return f"""# Issue Agent Routing Proposal

Issue:
- Repository: `{repo}`
- Issue Number: `#{issue_number}`
- Title: {issue.get("title", "")}
- Labels: {labels}
- Assignee: {assignees}
- Milestone: {milestone_title}
- Source URL: {issue_url}

User Request Original:
{blockquote(issue.get("body") or "")}

Recent Comments:
{comment_snippets(comments)}

Recommended Agent:
- Display Name: {decision.display_name}
- Core Role: {decision.core_role}
- Domain Focus: {decision.domain_focus}
- Work Focus: {decision.work_focus}
- Execution Mode: {decision.execution_mode}

Structured Agent Contract:
- Goal: Resolve or prepare the work requested in `{repo}#{issue_number}` according to the issue title, body, labels, and approved project agent rules.
- Source of Truth: GitHub Issue `{repo}#{issue_number}` and user confirmation after this proposal.
- Scope:
{textwrap.indent(list_items(decision.scope), "  ")}
- Out of Scope:
{textwrap.indent(list_items(decision.out_of_scope), "  ")}
- Required Context:
{textwrap.indent(list_items(decision.required_context), "  ")}
- Output Format: {decision.output_format}
- Verification:
{textwrap.indent(list_items(decision.verification), "  ")}
- Stop Condition:
{textwrap.indent(list_items(decision.stop_conditions), "  ")}

Missing Inputs:
{missing}

Recommended Next Action:
- 사용자에게 이 routing proposal 승인을 요청합니다.
- 승인 전에는 구현, branch 생성, commit, PR 생성, issue close를 하지 않습니다.
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a Level 1 agent routing proposal from a GitHub Issue.",
    )
    parser.add_argument("issue", help="Issue number, #number, or issue URL.")
    parser.add_argument(
        "--repo",
        default=DEFAULT_REPO,
        help=f"GitHub owner/repo. Default: {DEFAULT_REPO}",
    )
    parser.add_argument(
        "--comments",
        type=int,
        default=3,
        help="Number of recent issue comments to include. Use 0 to skip comments.",
    )
    parser.add_argument(
        "--output",
        help="Optional output Markdown path. Prints to stdout when omitted.",
    )
    parser.add_argument(
        "--token-env",
        default="GITHUB_TOKEN",
        help="Environment variable that stores a GitHub token. Default: GITHUB_TOKEN. GH_TOKEN is also accepted.",
    )
    parser.add_argument(
        "--no-gh-auth",
        action="store_true",
        help="Do not fall back to `gh auth token` when no token env var is set.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    token = resolve_github_token(args.token_env, use_gh_auth=not args.no_gh_auth)
    issue_number = parse_issue_number(args.issue)
    issue = get_issue(args.repo, issue_number, token)
    comments = get_comments(args.repo, issue_number, token, args.comments)
    proposal = render_markdown(args.repo, issue, make_decision(issue), comments)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(proposal)
        print(f"Wrote routing proposal: {args.output}")
    else:
        print(proposal)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
