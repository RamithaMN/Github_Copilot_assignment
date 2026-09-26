"""Command-line entry point for the repository health checker."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from .checker import run_github_checks, run_local_checks
from .github_service import GitHubService, parse_repository
from .report import render_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check local repository hygiene and GitHub metadata.")
    parser.add_argument("--path", type=Path, required=True, help="local repository path")
    parser.add_argument("--repo", required=True, help="GitHub repository in OWNER/REPOSITORY format")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.path.is_dir():
        parser.error(f"repository path is not a directory: {args.path}")
    try:
        parse_repository(args.repo)
    except ValueError as exc:
        parser.error(str(exc))

    service = GitHubService(token=os.getenv("GITHUB_TOKEN"))
    results = run_local_checks(args.path) + run_github_checks(service, args.repo)
    print(render_report(args.repo, results))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

