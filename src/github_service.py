"""Small GitHub REST adapter with injectable transport for deterministic tests."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.request

import certifi
from collections.abc import Callable, Mapping
from typing import Any


Transport = Callable[[str, str, Mapping[str, str], bytes | None], Any]


class GitHubServiceError(RuntimeError):
    """Raised when GitHub data cannot be fetched or validated."""


def parse_repository(value: str) -> tuple[str, str]:
    """Return owner and repository from an ``owner/repository`` value."""

    parts = value.strip().split("/")
    if len(parts) != 2 or not all(parts):
        raise ValueError("repository must use the OWNER/REPOSITORY format")
    return parts[0], parts[1]


class GitHubService:
    """Fetch the small set of GitHub resources used by the checker.

    ``transport`` is intentionally injectable. Production calls use urllib;
    tests can return decoded JSON without opening a network connection.
    """

    def __init__(
        self,
        token: str | None = None,
        *,
        base_url: str = "https://api.github.com",
        timeout: float = 10.0,
        transport: Transport | None = None,
    ) -> None:
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.transport = transport

    def list_open_issues(self, repository: str) -> list[dict[str, Any]]:
        """Return open issues, excluding pull requests returned by GitHub."""

        payload = self._request("GET", f"/repos/{self._path(repository)}/issues?state=open&per_page=100")
        if not isinstance(payload, list):
            raise GitHubServiceError("GitHub returned an invalid issues payload")
        return [item for item in payload if isinstance(item, dict) and "pull_request" not in item]

    def list_open_pull_requests(self, repository: str) -> list[dict[str, Any]]:
        """Return open pull requests with their activity timestamps."""

        payload = self._request("GET", f"/repos/{self._path(repository)}/pulls?state=open&per_page=100")
        if not isinstance(payload, list):
            raise GitHubServiceError("GitHub returned an invalid pull requests payload")
        return [item for item in payload if isinstance(item, dict)]

    def apply_label(self, repository: str, issue_number: int, label: str) -> Any:
        """Apply one label through the GitHub issues endpoint."""

        if not label.strip():
            raise ValueError("label must not be empty")
        return self._request(
            "POST",
            f"/repos/{self._path(repository)}/issues/{issue_number}/labels",
            body={"labels": [label]},
        )

    def _path(self, repository: str) -> str:
        owner, name = parse_repository(repository)
        return f"{owner}/{name}"

    def _request(self, method: str, path: str, *, body: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "github-repository-health-checker",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        encoded_body = json.dumps(body).encode("utf-8") if body is not None else None
        if encoded_body is not None:
            headers["Content-Type"] = "application/json"

        if self.transport is not None:
            try:
                return self.transport(method, url, headers, encoded_body)
            except Exception as exc:  # pragma: no cover - defensive adapter boundary
                raise GitHubServiceError(f"GitHub transport failed: {exc}") from exc

        request = urllib.request.Request(url, data=encoded_body, headers=headers, method=method)
        try:
            context = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(request, timeout=self.timeout, context=context) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise GitHubServiceError(f"GitHub request failed: {exc}") from exc
