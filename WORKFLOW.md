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

The direct before/after example is the first bounded review attempt. Copilot guessed
the tool names `read` and `search`, and the CLI reported them as unknown. The added
instruction is:

```text
Use only tool names exposed by the current Copilot session; never invent tool names.
If a requested tool is unavailable, report that limitation and stop rather than guessing.
```

Before: `read` and `search` failed as unknown tools. After: the corrected session used
the exposed `view`, `glob`, and `grep` tools, read the repository, and reported its
permission boundary. The before/after record is in
`docs/evidence/copilot-review-session.md` and
`docs/evidence/copilot-review-session-2026-09-26.md`.

The trace-authority instruction remains an additional safeguard based on the later
resumed-summary contradiction.

### What was deliberately left out

The global instruction file does not contain every health-check implementation detail,
a numeric health-score policy, credentials, broad write permissions, or rules already
enforced by tests and tooling.

## Q2 - Agentic sessions

The repository-reviewer agent is defined at `.github/agents/repo-reviewer.agent.md`.
Its scope is read-only review with evidence-backed findings.

The bounded sessions are:

1. Implement the configurable stale-PR threshold in a multi-step session. A
   deliberately failing CLI test was prepared first. Copilot ran it, read the
   argparse failure, changed `src/main.py`, `src/checker.py`, tests, and
   `README.md`, reran the focused test, and ran the full suite. The complete
   evidence is in `docs/evidence/agent-session-q2-cli-threshold.md`.
2. Correct the plugin integration after Copilot reported that the plugin directory lacked a root `plugin.json`.
3. Run the read-only repository-reviewer agent with only `view`, `glob`, and `grep` available. The session inspected the repository and produced an observed tool trace.

Evidence for the Copilot review and its failure/correction is in
`docs/evidence/copilot-review-session.md`. The implementation itself is verified
through the pytest suite and manual inspection.

The first session is the primary Q2 handoff evidence: its focused failure,
delegation boundary, approval decisions, multi-file edit, corrective rerun, and
independent verification are all recorded. The older stale-PR session remains
historical context, but is not used as the sole evidence for the requirement.

The later approval-bound sessions are recorded in
`docs/evidence/copilot-approval-prompts.md`. They show folder trust, approval of the
Python 3.12 test command, and refusal of an out-of-scope path write.

A fresh read-only `repo-reviewer` session and its human follow-up are recorded in
`docs/evidence/copilot-review-session-2026-09-26.md`. The agent found the missing CLI
coverage; the human added `tests/test_main.py` and reran the full Python 3.12 suite.

## Q3 - MCP integration

The actual scoped workspace configuration is `.github/mcp.json`; status is recorded in
`docs/MCP_STATUS.md`. The older `docs/mcp/github-mcp.intended.json` is retained as the
assignment-facing design record.

The claim-to-receipt map is `docs/evidence/EVIDENCE_INDEX.md`. Redacted raw excerpts
from the Copilot event store are in `docs/evidence/raw/`; they preserve the relevant
commands, approval payload, errors, and outcomes without committing credentials or
unrelated model context.

The final tool surface is intentionally small: two pull-request read tools for the
default server, and four pull-request/issue tools for the separately named approved-
write server. Failure behavior and the limits of the Copilot transport are in
`docs/mcp/FAILURE_HANDLING.md`; measured configuration cost is in
`docs/evidence/github-mcp-context-cost.md`.

The read loop was exercised against `rohitsundaram/Family-office-IC-agent` using the
GitHub MCP pull-request read tool. It returned no open pull requests, so the stale
decision was empty and no write was attempted. Evidence is in
`docs/evidence/github-mcp-read-loop.md`.

The write path was tested against controlled PR #4 with the exact MCP tools enabled:
`issue_write`, `issue_read`, `pull_request_read`, and `label_write`. Copilot fetched
the PR, stated that the PR was not 30-day stale, requested approval for only the
`needs-attention` label, and received approval. The first attempt returned
`403: Must have admin rights to Repository`. The setup was corrected by supplying
the authenticated runtime-only MCP header, then the approved retry applied the label
and re-fetched the PR to verify it. An independent `gh` read confirmed the same
external state.

There was no open PR older than 30 days in the controlled repositories, so the
session used `inactive_days=0` only as a clearly marked action-path demo. It does not
claim that PR #4 satisfied the default 30-day stale rule. The full evidence, including
the failed first iteration, successful retry, and context-cost analysis, is in
`docs/evidence/github-mcp-write-attempt.md`.

The account-wide repository selection audit is recorded in
`docs/evidence/repository-selection.md`. It found zero open pull requests across
`RamithaMN`, so no legitimate stale candidate existed for the write demonstration.

The application remains separate from this assignment workflow:

```text
CLI -> github_service.py -> GitHub REST API
Copilot agent -> GitHub MCP server -> GitHub state/actions
```

The assignment's successful-write loop is demonstrated as:
`FETCH -> DECIDE -> APPROVE -> ACT -> RE-FETCH -> VERIFY`. The first failed
iteration and the corrected setup are retained as evidence rather than hidden.

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

- An unprivileged staging attempt was blocked by `.git/index.lock`; the literal error and the successful permission-corrected retry are recorded in `docs/evidence/setup-failures.md`.
- Python 3.12 and pytest availability varied by environment. Because the literal setup output was not preserved, this is not used as a standalone scored claim; the preserved focused and full-suite receipts are authoritative.
- The first Copilot review attempt used invalid tool names and initially detected the plugin only as a Codex-format package; both issues were corrected and recorded in the evidence file.
- The resumed Copilot review contradicted its own observed read trace, so its summary was not accepted as authoritative evidence.
- The first GitHub MCP write attempt reached explicit approval but was rejected with `403: Must have admin rights to Repository`. Adding the runtime-only Authorization header fixed the setup; the approved retry applied and verified the label. Both iterations are documented.
- Automatic GitHub comments were deliberately not implemented; the planned external write is limited to an explicitly approved label action.

### What I would do differently with another week

With another week, repeat the live MCP loop against a repository with a genuinely
30-day-stale PR, capture `/context` and `/usage`, enable OpenTelemetry file export
for token/tool attribution, and validate the exact plugin schema against a second
clean Copilot installation.

### How Copilot was used for this submission

Copilot CLI 1.0.88 was authenticated and used for a read-only repository-reviewer
session. The session validated context discovery and exposed the plugin-layout
mistake, but its contradictory resumed summary was treated as untrusted.
