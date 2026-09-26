from pathlib import Path

import pytest

from src import main as main_module
from src.models import CheckResult, Status


def test_main_orchestrates_checks_and_renders_report(monkeypatch, tmp_path, capsys):
    local_results = [CheckResult("README", Status.PASS, "README.md found")]
    github_results = [CheckResult("Open issues", Status.PASS, "0 open issue(s)")]
    calls = {}

    class FakeService:
        pass

    def fake_local_checks(path: Path):
        calls["path"] = path
        return local_results

    def fake_github_checks(service, repository, *, inactive_days=30):
        calls["service"] = service
        calls["repository"] = repository
        calls["inactive_days"] = inactive_days
        return github_results

    monkeypatch.setattr(main_module, "GitHubService", lambda token=None: FakeService())
    monkeypatch.setattr(main_module, "run_local_checks", fake_local_checks)
    monkeypatch.setattr(main_module, "run_github_checks", fake_github_checks)

    assert main_module.main(["--path", str(tmp_path), "--repo", "octo/project"]) == 0

    output = capsys.readouterr().out
    assert "GitHub Repository Health: octo/project" in output
    assert "[PASS   ] README: README.md found" in output
    assert calls["path"] == tmp_path
    assert isinstance(calls["service"], FakeService)
    assert calls["repository"] == "octo/project"
    assert calls["inactive_days"] == 30


def test_main_passes_inactive_days_to_github_checks(monkeypatch, tmp_path, capsys):
    captured = {}

    class FakeService:
        pass

    def fake_github_checks(service, repository, *, inactive_days=30):
        captured["inactive_days"] = inactive_days
        return []

    monkeypatch.setattr(main_module, "GitHubService", lambda token=None: FakeService())
    monkeypatch.setattr(main_module, "run_local_checks", lambda path: [])
    monkeypatch.setattr(main_module, "run_github_checks", fake_github_checks)

    assert main_module.main(
        ["--path", str(tmp_path), "--repo", "octo/project", "--inactive-days", "45"]
    ) == 0

    assert captured["inactive_days"] == 45


@pytest.mark.parametrize(
    "arguments, message",
    [
        (["--path", "/does/not/exist", "--repo", "octo/project"], "not a directory"),
        (["--path", ".", "--repo", "octo"], "OWNER/REPOSITORY"),
    ],
)
def test_main_rejects_invalid_cli_arguments(arguments, message, capsys):
    with pytest.raises(SystemExit) as error:
        main_module.main(arguments)

    assert error.value.code == 2
    assert message in capsys.readouterr().err
