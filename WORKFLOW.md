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
deterministic. The implementation and test suite enforce this boundary. A full
before/after Copilot code-edit transcript is not claimed; the observed review session
and its setup correction are recorded in
`docs/evidence/copilot-review-session.md`.

### What was deliberately left out

The global instruction file does not contain every health-check implementation detail,
a numeric health-score policy, credentials, broad write permissions, or rules already
enforced by tests and tooling.

## Q2 - Agentic sessions

The repository-reviewer agent is defined at `.github/agents/repo-reviewer.agent.md`.
Its scope is read-only review with evidence-backed findings.

The bounded sessions are:

1. Add stale pull-request detection using `updated_at` and the 30-day rule. This was implemented and verified by the local pytest suite; no Copilot code-edit transcript is claimed.
2. Correct the plugin integration after Copilot reported that the plugin directory lacked a root `plugin.json`.
3. Run the read-only repository-reviewer agent with only `view`, `glob`, and `grep` available. The session inspected the repository and produced an observed tool trace.

Evidence for the Copilot review and its failure/correction is in
`docs/evidence/copilot-review-session.md`. The implementation itself is verified
through the pytest suite and manual inspection.

The later approval-bound sessions are recorded in
`docs/evidence/copilot-approval-prompts.md`. They show folder trust, approval of the
Python 3.12 test command, and refusal of an out-of-scope path write.

## Q3 - MCP integration

The actual scoped workspace configuration is `.github/mcp.json`; status is recorded in
`docs/MCP_STATUS.md`. The older `docs/mcp/github-mcp.intended.json` is retained as the
assignment-facing design record.

The read loop was exercised against `rohitsundaram/Family-office-IC-agent` using the
GitHub MCP pull-request read tool. It returned no open pull requests, so the stale
decision was empty and no write was attempted. Evidence is in
`docs/evidence/github-mcp-read-loop.md`.

The write loop remains separately gated: enable the exact label-update tool, request
approval, apply `needs-attention`, then re-fetch to verify when a real stale candidate
exists. No external write is claimed in this session.

The application remains separate from this assignment workflow:

```text
CLI -> github_service.py -> GitHub REST API
Copilot agent -> GitHub MCP server -> GitHub state/actions
```

## Q4 - Plugin and approval governance

The local plugin is under `plugins/repository-health-review/`. It contains the
Codex-compatible manifest at `.codex-plugin/plugin.json`, the Copilot root
`plugin.json`, and a reusable review skill. The root manifest correction was observed
through Copilot's plugin discovery warning.

The plugin was kept small and read-oriented. It does not duplicate the CLI, expose
credentials, or permit GitHub writes. Vetting and proposed approval boundaries are in
`APPROVALS.md`.

## What didn't work

### Dead ends, failures, and abandoned ideas

- The first `git init` attempt was blocked by the workspace filesystem permission around `.git`; retrying with the required elevated filesystem permission succeeded.
- Python 3.12 was not installed in the active environment; the implementation remains compatible with Python 3.11 while declaring 3.12 as the assignment target.
- `pytest` was not initially installed; it is declared in `requirements.txt` and must be installed in the project virtual environment before verification.
- The first Copilot review attempt used invalid tool names and initially detected the plugin only as a Codex-format package; both issues were corrected and recorded in the evidence file.
- The resumed Copilot review contradicted its own observed read trace, so its summary was not accepted as authoritative evidence.
- Automatic GitHub comments were deliberately not implemented; the planned external write is limited to an explicitly approved label action.

### What I would do differently with another week

Run the project in the target Copilot environment, capture the three required agentic
transcripts and real approval prompts, validate the exact Copilot plugin schema, and
complete the live MCP fetch-decide-act-verify demonstration against a controlled test
repository.

### How Copilot was used for this submission

Copilot CLI 1.0.88 was authenticated and used for a read-only repository-reviewer
session. The session validated context discovery and exposed the plugin-layout
mistake, but its contradictory resumed summary was treated as untrusted.
