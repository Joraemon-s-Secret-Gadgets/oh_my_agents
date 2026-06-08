import unittest

from scripts.lovv_issue_router import (
    choose_agent,
    choose_execution_mode,
    make_decision,
    parse_issue_number,
)


def issue(title, body="", labels=None):
    return {
        "number": 123,
        "title": title,
        "body": body,
        "labels": [{"name": name} for name in (labels or [])],
        "assignees": [],
        "milestone": None,
        "html_url": "https://github.com/Joraemon-s-Secret-Gadgets/Lovv/issues/123",
    }


class LovvIssueRouterTest(unittest.TestCase):
    def test_parse_issue_number_variants(self):
        self.assertEqual(parse_issue_number("123"), 123)
        self.assertEqual(parse_issue_number("#123"), 123)
        self.assertEqual(parse_issue_number("https://github.com/org/repo/issues/123"), 123)

    def test_frontend_review_routes_to_frontend_qa_review_agent(self):
        display_name, core_role, domain_focus, work_focus = choose_agent(
            issue("화면 QA 검토", labels=["frontend", "review"])
        )
        self.assertEqual(display_name, "Frontend QA Review Agent")
        self.assertEqual(core_role, "Review Agent")
        self.assertEqual(domain_focus, "Frontend")
        self.assertEqual(work_focus, "QA")

    def test_security_routes_to_sequential_mode(self):
        target = issue("인증 토큰 보안 검토", labels=["backend", "security"])
        _, core_role, _, work_focus = choose_agent(target)
        self.assertEqual(choose_execution_mode(target, core_role, work_focus), "Sequential Mode")

    def test_unknown_issue_defaults_to_spec_agent_and_missing_scope(self):
        decision = make_decision(issue("새 기능 아이디어"))
        self.assertEqual(decision.display_name, "Spec Agent")
        self.assertIn("TBD: ask user for target files, folders, or behavior", decision.scope)
        self.assertTrue(decision.missing_inputs)


if __name__ == "__main__":
    unittest.main()
