"""Command-line entry point for the repository health checker."""

from __future__ import annotations

import argparse
import os
from collections.abc import Callable
from pathlib import Path

from .checker import find_stale_pull_requests, run_github_checks, run_local_checks
from .github_service import GitHubService, parse_repository
from .report import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check local repository hygiene and GitHub metadata.")
    parser.add_argument("--path", type=Path, required=True, help="local repository path")
    parser.add_argument("--repo", required=True, help="GitHub repository in OWNER/REPOSITORY format")
    parser.add_argument(
        "--inactive-days",
        type=int,
        default=30,
        help="days without activity before an open pull request is considered stale (default: 30)",
    )
    parser.add_argument(
        "--apply-needs-attention",
        type=int,
        metavar="PR_NUMBER",
        help="ask for confirmation before labeling a stale pull request",
    )
    return parser


def main(argv: list[str] | None = None, *, input_fn: Callable[[str], str] = input) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.path.is_dir():
        parser.error(f"repository path is not a directory: {args.path}")
    if args.inactive_days < 0:
        parser.error("inactive days must be zero or greater")
    if args.apply_needs_attention is not None and args.apply_needs_attention < 1:
        parser.error("PR_NUMBER must be greater than zero")
    try:
        parse_repository(args.repo)
    except ValueError as exc:
        parser.error(str(exc))

    service = GitHubService(token=os.getenv("GITHUB_TOKEN"))
    results = run_local_checks(args.path) + run_github_checks(
        service, args.repo, inactive_days=args.inactive_days
    )
    print(render_report(args.repo, results))

    if args.apply_needs_attention is not None:
        _apply_needs_attention(
            parser,
            service,
            args.repo,
            args.apply_needs_attention,
            inactive_days=args.inactive_days,
            input_fn=input_fn,
        )
    return 0


def _apply_needs_attention(
    parser: argparse.ArgumentParser,
    service: GitHubService,
    repository: str,
    pull_number: int,
    *,
    inactive_days: int,
    input_fn: Callable[[str], str],
) -> None:
    """Apply the only supported external write after validation and confirmation."""

    try:
        open_pull_requests = service.list_open_pull_requests(repository)
        stale = find_stale_pull_requests(open_pull_requests, inactive_days=inactive_days)
    except Exception as exc:
        parser.error(f"cannot validate pull request before label write: {exc}")

    candidate = next((item for item in stale if item.number == pull_number), None)
    if candidate is None:
        parser.error(
            f"pull request #{pull_number} is not an open stale pull request; no label was applied"
        )

    answer = input_fn(
        f"Apply needs-attention to stale pull request #{pull_number} in {repository}? [y/N]: "
    )
    if answer.strip().lower() not in {"y", "yes"}:
        print("No external write performed.")
        return

    try:
        service.apply_label(repository, pull_number, "needs-attention")
        refreshed = service.list_open_pull_requests(repository)
    except Exception as exc:
        parser.error(f"label write failed; no verification available: {exc}")

    refreshed_item = next((item for item in refreshed if item.get("number") == pull_number), None)
    labels = refreshed_item.get("labels", []) if refreshed_item else []
    label_names = {
        str(label.get("name"))
        for label in labels
        if isinstance(label, dict) and label.get("name")
    }
    if "needs-attention" not in label_names:
        parser.error("label write completed but verification did not find needs-attention")
    print(f"Applied and verified needs-attention on pull request #{pull_number}.")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
