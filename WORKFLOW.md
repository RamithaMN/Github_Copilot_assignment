# Workflow

## Project summary

This repository implements a small GitHub Repository Health Checker for the GitHub
Copilot practitioner assignment. The product is intentionally modest; the submission
focuses on context design, bounded delegation, safe external access, approvals, and
evidence.

## Verification command

The primary verification command is:

```bash
python -m pytest
```

The CLI smoke command is:

```bash
python -m src.main --path . --repo OWNER/REPOSITORY
```

## Q1 - Copilot context and instruction layer

### Repository instructions

`.github/copilot-instructions.md` defines Python compatibility, independent checks,
the status vocabulary, the `github_service.py` boundary, untrusted external text,
non-modification of inspected repositories, and the required verification command.

### Path-scoped instructions

`.github/instructions/tests.instructions.md` applies to tests and requires deterministic
pytest tests, mocked external responses, boundary coverage, and focused-then-full runs.

### Prompt files

`.github/prompts/add-health-check.prompt.md` and `.github/prompts/fix-test.prompt.md`
provide repeatable, task-specific workflows.

### Instruction added after a failure

The intended correction is:

```text
All external GitHub operations must go through github_service.py.
Health-check functions must not directly call GitHub APIs.
```

This prevents external calls from being mixed into business logic and keeps tests
deterministic. A Copilot before/after transcript has not been captured because the
Copilot CLI is not installed in this environment; this is not claimed as completed
Copilot evidence.

### What was deliberately left out

The global instruction file does not contain every health-check implementation detail,
a numeric health-score policy, credentials, broad write permissions, or rules already
enforced by tests and tooling.

## Q2 - Agentic sessions

The repository-reviewer agent is defined at `.github/agents/repo-reviewer.agent.md`.
Its scope is read-only review with evidence-backed findings.

The intended bounded sessions are:

1. Add stale pull-request detection using `updated_at` and the 30-day rule.
2. Correct one failed iteration involving a check or malformed external response through a test or instruction improvement.
3. Run the repository-reviewer agent against the resulting diff.

No Copilot transcript is claimed for these sessions because the Copilot CLI is not
available. The implementation itself has been verified through the pytest suite and
manual inspection.

## Q3 - MCP integration

The intended scoped configuration is in `docs/mcp/github-mcp.intended.json`; status is
recorded in `docs/MCP_STATUS.md`.

The intended loop is fetch open pull requests, decide staleness from `updated_at`, ask
for approval, apply `needs-attention`, and re-fetch to verify. No live MCP call is
claimed. The observed environment did not provide a Copilot CLI or a known Copilot MCP
configuration location.

The application remains separate from this assignment workflow:

```text
CLI -> github_service.py -> GitHub REST API
Copilot agent -> GitHub MCP server -> GitHub state/actions
```

## Q4 - Plugin and approval governance

The local plugin is under `plugins/repository-health-review/`. It contains the
Codex-compatible manifest at `.codex-plugin/plugin.json` and a reusable review skill.
Because no Copilot runtime was available, no Copilot plugin activation is claimed.

The plugin was kept small and read-oriented. It does not duplicate the CLI, expose
credentials, or permit GitHub writes. Vetting and proposed approval boundaries are in
`APPROVALS.md`.

## What didn't work

### Dead ends, failures, and abandoned ideas

- The first `git init` attempt was blocked by the workspace filesystem permission around `.git`; retrying with the required elevated filesystem permission succeeded.
- Python 3.12 was not installed in the active environment; the implementation remains compatible with Python 3.11 while declaring 3.12 as the assignment target.
- `pytest` was not initially installed; it is declared in `requirements.txt` and must be installed in the project virtual environment before verification.
- The Copilot CLI and a known Copilot MCP configuration location were unavailable, so no live Copilot/MCP success is claimed.
- Automatic GitHub comments were deliberately not implemented; the planned external write is limited to an explicitly approved label action.

### What I would do differently with another week

Run the project in the target Copilot environment, capture the three required agentic
transcripts and real approval prompts, validate the exact Copilot plugin schema, and
complete the live MCP fetch-decide-act-verify demonstration against a controlled test
repository.

### How Copilot was used for this submission

Copilot usage evidence is not claimed because Copilot was unavailable in the current
environment. The repository records the intended context, agent, MCP, plugin, and
approval artifacts so the target environment can execute and verify them honestly.

