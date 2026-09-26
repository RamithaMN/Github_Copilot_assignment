from src.models import CheckResult, Status
from src.report import render_report


def test_render_report_contains_statuses_and_messages():
    report = render_report(
        "octo/project",
        [CheckResult("README", Status.PASS, "README.md found")],
    )
    assert "GitHub Repository Health: octo/project" in report
    assert "[PASS   ] README: README.md found" in report

