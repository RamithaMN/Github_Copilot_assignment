"""Repository checks and GitHub-derived health rules."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Protocol

from .models import CheckResult, PullRequestSummary, Status


class GitHubReader(Protocol):
    def list_open_issues(self, repository: str) -> list[dict[str, Any]]: ...

    def list_open_pull_requests(self, repository: str) -> list[dict[str, Any]]: ...


def run_local_checks(repo_path: Path) -> list[CheckResult]:
    """Run all checks that only inspect the local repository."""

    return [
        check_readme(repo_path),
        check_gitignore(repo_path),
        check_tests(repo_path),
        check_dependencies(repo_path),
        check_ci(repo_path),
        check_docs(repo_path),
    ]


def check_readme(repo_path: Path) -> CheckResult:
    path = repo_path / "README.md"
    return _file_result("README", path, "README.md found")


def check_gitignore(repo_path: Path) -> CheckResult:
    path = repo_path / ".gitignore"
    return _file_result(".gitignore", path, ".gitignore found")


def check_tests(repo_path: Path) -> CheckResult:
    tests_dir = repo_path / "tests"
    patterns = ("test_*.py", "*.test.js", "*.spec.js")
    found = tests_dir.is_dir() or any(
        path.is_file() for pattern in patterns for path in repo_path.glob(pattern)
    )
    if found:
        return CheckResult("Tests", Status.PASS, "test directory or test files found")
    return CheckResult("Tests", Status.FAIL, "no supported test directory or test files found")


def check_dependencies(repo_path: Path) -> CheckResult:
    names = ("requirements.txt", "pyproject.toml", "package.json", "pom.xml")
    found = next((name for name in names if (repo_path / name).is_file()), None)
    if found:
        return CheckResult("Dependencies", Status.PASS, f"dependency configuration found: {found}")
    return CheckResult("Dependencies", Status.WARNING, "no supported dependency configuration found")


def check_ci(repo_path: Path) -> CheckResult:
    workflow_dir = repo_path / ".github" / "workflows"
    if workflow_dir.is_dir() and any(path.is_file() for path in workflow_dir.iterdir()):
        return CheckResult("CI", Status.PASS, "GitHub Actions workflow found")
    return CheckResult("CI", Status.WARNING, "no GitHub Actions workflow found")


def check_docs(repo_path: Path) -> CheckResult:
    docs_dir = repo_path / "docs"
    markdown_files = list(repo_path.glob("*.md"))
    if docs_dir.is_dir() or markdown_files:
        return CheckResult("Documentation", Status.PASS, "documentation found")
    return CheckResult("Documentation", Status.WARNING, "no documentation directory or Markdown file found")


def check_open_issues(service: GitHubReader, repository: str) -> CheckResult:
    try:
        issues = service.list_open_issues(repository)
    except Exception as exc:
        return CheckResult("Open issues", Status.UNKNOWN, f"GitHub data unavailable: {exc}")
    count = len(issues)
    status = Status.PASS if count == 0 else Status.WARNING
    return CheckResult("Open issues", status, f"{count} open issue(s)")


def find_stale_pull_requests(
    pull_requests: list[dict[str, Any]],
    *,
    now: datetime | None = None,
    inactive_days: int = 30,
) -> list[PullRequestSummary]:
    """Return PRs with no activity strictly greater than ``inactive_days``."""

    reference = now or datetime.now(timezone.utc)
    cutoff = reference - timedelta(days=inactive_days)
    stale: list[PullRequestSummary] = []
    for item in pull_requests:
        try:
            number = int(item["number"])
            title = str(item.get("title", "(untitled)"))
            updated_at = str(item["updated_at"])
            updated = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            if updated.tzinfo is None:
                updated = updated.replace(tzinfo=timezone.utc)
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"invalid pull request data: {exc}") from exc
        if updated < cutoff:
            stale.append(PullRequestSummary(number, title, updated_at))
    return stale


def check_stale_pull_requests(
    service: GitHubReader,
    repository: str,
    *,
    now: datetime | None = None,
    inactive_days: int = 30,
) -> CheckResult:
    try:
        pull_requests = service.list_open_pull_requests(repository)
        stale = find_stale_pull_requests(pull_requests, now=now, inactive_days=inactive_days)
    except Exception as exc:
        return CheckResult("Stale pull requests", Status.UNKNOWN, f"GitHub data unavailable: {exc}")
    if not stale:
        return CheckResult("Stale pull requests", Status.PASS, "no open pull requests inactive for more than 30 days")
    numbers = ", ".join(f"#{item.number}" for item in stale)
    return CheckResult("Stale pull requests", Status.WARNING, f"inactive for more than 30 days: {numbers}")


def run_github_checks(
    service: GitHubReader,
    repository: str,
    *,
    now: datetime | None = None,
) -> list[CheckResult]:
    return [
        check_open_issues(service, repository),
        check_stale_pull_requests(service, repository, now=now),
    ]


def _file_result(check: str, path: Path, success_message: str) -> CheckResult:
    if path.is_file():
        return CheckResult(check, Status.PASS, success_message)
    return CheckResult(check, Status.FAIL, f"missing {path.name}")
