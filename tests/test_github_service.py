import json

import pytest

from src.github_service import GitHubService, parse_repository


def test_parse_repository():
    assert parse_repository("octo/project") == ("octo", "project")


@pytest.mark.parametrize("value", ["", "octo", "/project", "octo/project/extra"])
def test_parse_repository_rejects_invalid_values(value):
    with pytest.raises(ValueError):
        parse_repository(value)


def test_service_filters_pull_requests_from_issue_results():
    calls = []

    def transport(method, url, headers, body):
        calls.append((method, url, headers, body))
        return [{"number": 1}, {"number": 2, "pull_request": {"url": "..."}}]

    service = GitHubService(token="secret", transport=transport)
    assert service.list_open_issues("octo/project") == [{"number": 1}]
    assert calls[0][0] == "GET"
    assert calls[0][1].endswith("/repos/octo/project/issues?state=open&per_page=100")
    assert calls[0][2]["Authorization"] == "Bearer secret"


def test_apply_label_sends_json_body():
    calls = []

    def transport(method, url, headers, body):
        calls.append((method, url, headers, body))
        return [{"name": "needs-attention"}]

    service = GitHubService(transport=transport)
    assert service.apply_label("octo/project", 7, "needs-attention") == [{"name": "needs-attention"}]
    method, url, headers, body = calls[0]
    assert method == "POST"
    assert url.endswith("/repos/octo/project/issues/7/labels")
    assert headers["Content-Type"] == "application/json"
    assert json.loads(body) == {"labels": ["needs-attention"]}

