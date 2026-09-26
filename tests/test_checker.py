from datetime import datetime, timezone

from src.checker import (
    check_ci,
    check_dependencies,
    check_docs,
    check_gitignore,
    check_open_issues,
    check_readme,
    check_stale_pull_requests,
    check_tests,
    find_stale_pull_requests,
)
from src.models import Status


def test_local_checks_detect_expected_files(tmp_path):
    (tmp_path / "README.md").write_text("# Project")
    (tmp_path / ".gitignore").write_text("__pycache__/\n")
    (tmp_path / "tests").mkdir()
    (tmp_path / "requirements.txt").write_text("pytest\n")
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "test.yml").write_text("name: test\n")
    (tmp_path / "docs").mkdir()

    assert check_readme(tmp_path).status is Status.PASS
    assert check_gitignore(tmp_path).status is Status.PASS
    assert check_tests(tmp_path).status is Status.PASS
    assert check_dependencies(tmp_path).status is Status.PASS
    assert check_ci(tmp_path).status is Status.PASS
    assert check_docs(tmp_path).status is Status.PASS


def test_missing_required_files_are_reported(tmp_path):
    assert check_readme(tmp_path).status is Status.FAIL
    assert check_gitignore(tmp_path).status is Status.FAIL
    assert check_tests(tmp_path).status is Status.FAIL
    assert check_dependencies(tmp_path).status is Status.WARNING
    assert check_ci(tmp_path).status is Status.WARNING
    assert check_docs(tmp_path).status is Status.WARNING


def test_stale_boundary_is_strictly_more_than_thirty_days():
    now = datetime(2026, 1, 31, 12, tzinfo=timezone.utc)
    pull_requests = [
        {"number": 1, "title": "exactly at cutoff", "updated_at": "2026-01-01T12:00:00Z"},
        {"number": 2, "title": "older than cutoff", "updated_at": "2025-12-31T11:59:59Z"},
    ]
    stale = find_stale_pull_requests(pull_requests, now=now)
    assert [item.number for item in stale] == [2]


def test_malformed_pull_request_data_becomes_unknown():
    class Service:
        def list_open_pull_requests(self, repository):
            return [{"number": 1}]

    result = check_stale_pull_requests(Service(), "owner/repo")
    assert result.status is Status.UNKNOWN


def test_github_failures_become_unknown():
    class Service:
        def list_open_issues(self, repository):
            raise RuntimeError("network unavailable")

    result = check_open_issues(Service(), "owner/repo")
    assert result.status is Status.UNKNOWN

