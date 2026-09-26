# GitHub Repository Health Checker

## What it is

A small Python CLI that checks repository hygiene locally and reads selected GitHub
metadata through an isolated service adapter.

## Features

- Checks README, `.gitignore`, tests, dependency configuration, CI workflows, and docs.
- Counts open issues.
- Finds open pull requests inactive for more than 30 days using `updated_at`.
- Reports `PASS`, `WARNING`, `FAIL`, or `UNKNOWN` without inventing an overall score.
- Keeps network access behind `src/github_service.py` so it can be mocked in tests.

## Requirements

- Python 3.12 for the assignment target. Python 3.11 is also supported by the current implementation.
- A GitHub token in `GITHUB_TOKEN` for authenticated metadata reads.

## Installation

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

## How to run

```bash
python -m src.main --path . --repo OWNER/REPOSITORY
```

When GitHub is unavailable, GitHub-backed checks report `UNKNOWN`; local checks still run.

## How to test

```bash
python -m pytest
```

## Example output

```text
GitHub Repository Health: OWNER/REPOSITORY
========================================
[PASS   ] README: README.md found
[PASS   ] .gitignore: .gitignore found
[PASS   ] Tests: test directory or test files found
[WARNING] Stale pull requests: inactive for more than 30 days: #23
```

## Time spent

Record the final measured time in `WORKFLOW.md` at submission time. No time estimate is
presented as observed evidence in this repository.

