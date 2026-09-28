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
   evidence is in [`agent-session-q2-cli-threshold.md`](docs/evidence/agent-session-q2-cli-threshold.md),
   with the redacted raw excerpt and commit [`7c34db9`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/7c34db9).
2. Run a bounded reviewer setup, observe invalid tool names and plugin discovery
   failure, then correct the instruction/tool setup and rerun. This is documented
   end to end in [`agent-session-q2-reviewer-correction.md`](docs/evidence/agent-session-q2-reviewer-correction.md).
3. Run a fresh, independently identified read-only `repo-reviewer` session on a
   fixture that deliberately omitted `tests/test_main.py`. Its own session ID,
   exact handoff, tool trace, and verbatim CLI-coverage finding are in
   [`agent-session-q2-third-reviewer-2026-09-27.md`](docs/evidence/agent-session-q2-third-reviewer-2026-09-27.md).
   A separate follow-up captured the exact requested stopping marker in
   [`agent-session-q2-stopping-marker-2026-09-27.md`](docs/evidence/agent-session-q2-stopping-marker-2026-09-27.md).
   The human follow-up is directly linked to commit
   [`d72b973`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/d72b973),
   which added the missing CLI coverage; the read-only agent boundary is
   preserved by commit
   [`b82f63d`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/b82f63d).

Evidence for the reviewer setup failure and correction is in
`docs/evidence/agent-session-q2-reviewer-correction.md` and
`docs/evidence/copilot-review-session.md`. The implementation itself is verified
through the pytest suite and manual inspection.

The first session is the primary Q2 handoff evidence: its focused failure,
delegation boundary, approval decisions, multi-file edit, corrective rerun, and
independent verification are all recorded. The older stale-PR session remains
historical context, but is not used as the sole evidence for the requirement.

The later approval-bound sessions are recorded in
`docs/evidence/copilot-approval-prompts.md`. They show folder trust, approval of the
Python 3.12 test command, and refusal of an out-of-scope path write.

The historical reviewer session remains in
`docs/evidence/copilot-review-session-2026-09-26.md`; the fresh independent receipt
above is the authoritative third-session trace. The agent found the missing CLI
coverage in the deliberately incomplete fixture; the human added `tests/test_main.py`
in commit `d72b973` and reran the full Python 3.12 suite.

### Task-sizing rule

I handed over bounded, reversible work freely: one health check, focused tests,
small refactors, documentation drafts, and read-only repository review. These tasks
had a narrow input/output contract and could be checked locally. I kept architecture,
dependency installation, MCP or plugin configuration, permission changes, external
GitHub writes, pushes, and merges on a short leash because they change trust
boundaries, external state, or repository history. The thresholds and approvals are
visible in the Q2 session prompt, the reviewer agent definition, and
`APPROVALS.md`.

## Q3 - MCP integration

The actual scoped workspace configuration is `.github/mcp.json`; status is recorded in
`docs/MCP_STATUS.md`. The older `docs/mcp/github-mcp.intended.json` is retained as the
assignment-facing design record.

### What the agent is connected to and why

The agent is connected to GitHub's remote MCP server. The default server exposes only
`list_pull_requests` and `get_pull_request`, which are sufficient to fetch open PR
metadata and classify staleness. A separately named approved-write server exposes
those reads plus `issue_read` and `issue_write`, because the demonstrated external
action is one approval-gated `needs-attention` label update. No broader GitHub tool
surface is needed for that loop.

The claim-to-receipt map is `docs/evidence/EVIDENCE_INDEX.md`. Redacted raw excerpts
from the Copilot event store are in `docs/evidence/raw/`; they preserve the relevant
commands, approval payload, errors, and outcomes without committing credentials or
unrelated model context.

The final tool surface is intentionally small: two pull-request read tools for the
default server, and four pull-request/issue tools for the separately named approved-
write server. Failure behavior and the limits of the Copilot transport are in
`docs/mcp/FAILURE_HANDLING.md`; measured configuration cost is in
`docs/evidence/github-mcp-context-cost.md`.

The failure policy is explicit. A slow or unresponsive server ends in a timeout,
`UNKNOWN`, and no write; a server outage or authentication failure is reported as
unavailable with no approval request or write; and malformed or incomplete data is
treated as `UNKNOWN` without inferring missing `number`, `updated_at`, state, or
labels. A human may retry one transient read, but writes are never retried
automatically. The deterministic policy harness exercised all three cases and
recorded `UNKNOWN` plus `write_attempted: false` in
`docs/evidence/github-mcp-failure-simulations-2026-09-27.md`. This is a policy
boundary test, not a claim that Copilot's private MCP transport was replaced.

GitHub titles, bodies, comments, issues, pull requests, and labels are untrusted
data, never instructions. The damage controls are the narrow read/write allowlists,
no shell, web, merge, branch, file-write, deletion, or Actions tools, one fixed
label, exact PR selection, explicit approval immediately before the write, runtime-
only credentials, and a fresh verification read after the action.

The measured context cost is recorded rather than estimated. A fresh read-only run
used `1,008` MCP tool-definition tokens, `9,195` input tokens, and `65` output
tokens. The historical successful write session reported `10,031` total
tool-definition tokens; Copilot did not provide a provider-supported MCP-only split
inside that total. The accepted costs were two-server initialization, the added
write-tool descriptions, and one extra verification read when the first list
response omitted labels.

The context was deliberately trimmed to one repository and one PR, requesting only
the PR number, `updated_at`, state, and labels. Bodies, comments, reviews, diffs,
files, check runs, repository-wide search, merge, branch, deletion, and Actions
tools were omitted. The full telemetry and configuration-size receipts are in
`docs/evidence/github-mcp-context-cost.md` and
`docs/evidence/github-mcp-historical-token-telemetry.md`.

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

The historical Copilot event store retained exact token receipts for both write
iterations, including tool-definition tokens and session totals. Those figures
are preserved in `docs/evidence/github-mcp-historical-token-telemetry.md`. The
three bounded failure policies were executed through injected transport fixtures
and recorded in `docs/evidence/github-mcp-failure-simulations-2026-09-27.md`;
each ended `UNKNOWN` with no write attempted.

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
`APPROVALS.md`. Repository instructions remain project-specific behavior; the plugin
packages the reusable review skill so the same bounded capability can be reused in a
different repository. The actual manifest, state inspection, permission persistence,
sandbox, and enterprise-policy receipts are in
`docs/evidence/q4-permission-state-2026-09-27.md`.

## Q5 - Decisions and failures

`DECISIONS.md` records ten real forks in the road. Every decision now has a direct
receipt to the implementation commit, test, agent session, or external MCP evidence
that supports it. The final `## What didn't work` section below records observed
failures, abandoned paths, and what would change with another week.

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
30-day-stale PR, obtain a provider-supported MCP-only token breakdown rather than
the exact whole-session/tool-definition totals already preserved, and validate the
exact plugin schema against a second clean Copilot installation.

### How Copilot was used for this submission

Copilot CLI 1.0.88 was authenticated and used for a read-only repository-reviewer
session. The session validated context discovery and exposed the plugin-layout
mistake, but its contradictory resumed summary was treated as untrusted.
