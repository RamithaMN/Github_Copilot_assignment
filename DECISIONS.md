# Decisions

Each decision below links to the implementation commit, test, session, or external
receipt that supports the choice. The links are evidence pointers, not claims that
the alternative was experimentally implemented.

## Decision 1 - CLI instead of web application

- Choice: build a Python CLI.
- Alternative: build a web dashboard.
- Cost accepted: less visual polish and no persistent user interface.
- What would change my mind: a requirement for multi-user monitoring or scheduled reports.
- Receipt: [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) introduced the Python CLI structure and entrypoint.

## Decision 2 - REST adapter for the product

- Choice: keep the application behind `github_service.py` using the GitHub REST API.
- Alternative: make the CLI an MCP client.
- Cost accepted: the product and assignment MCP demonstration use separate integrations.
- What would change my mind: a requirement for the product itself to consume MCP tools.
- Receipt: [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) introduced `src/github_service.py`; [`8771ed9`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/8771ed9) records the adapter's trusted-certificate correction.

## Decision 3 - Read-only default

- Choice: local checks and GitHub reads are the default behavior.
- Alternative: automatically comment on or label every stale pull request.
- Cost accepted: findings require a separate approved action.
- What would change my mind: a controlled operational workflow with explicit write authorization.
- Receipt: [`ff6c746`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/ff6c746) added the opt-in, confirmation-gated label workflow and its tests.

## Decision 4 - Thirty-day stale threshold

- Choice: stale means no activity for more than 30 days, measured by `updated_at`.
- Alternative: use creation date or a 90-day threshold.
- Cost accepted: the rule is intentionally simple and may not fit every team.
- What would change my mind: a repository-specific policy supplied as a documented configuration.
- Receipt: [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) implemented `updated_at` and the 30-day default; [`03afba4`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/03afba4) added the strict cutoff test.

## Decision 5 - Fixed MVP checks

- Choice: implement the assignment's fixed checks first.
- Alternative: build a general policy-file engine.
- Cost accepted: teams cannot customize every rule in v1.
- What would change my mind: repeated use across repositories with materially different policies.
- Receipt: [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) introduced the fixed local and GitHub check set used by the MVP.

## Decision 6 - pytest

- Choice: use pytest as the primary test runner.
- Alternative: use unittest only.
- Cost accepted: one development dependency is required.
- What would change my mind: an environment policy that permits only the standard library.
- Receipt: [`03afba4`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/03afba4) added the pytest suite and CI workflow.

## Decision 7 - Adapter boundary

- Choice: all external GitHub operations go through `github_service.py`.
- Alternative: call GitHub directly from each checker.
- Cost accepted: a small amount of adapter code.
- What would change my mind: removal of external checks from the product.
- Receipt: [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) placed GitHub access behind `src/github_service.py`; [`8771ed9`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/8771ed9) records the adapter-level network correction.

## Decision 8 - No numeric health score

- Choice: report named statuses with evidence.
- Alternative: calculate a 0-100 score.
- Cost accepted: results are less convenient to rank.
- What would change my mind: a validated scoring policy with user-agreed weights.
- Receipt: [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) introduced named `Status` values and report output without a numeric score.

## Decision 9 - Configurable stale threshold with a stable default

- Choice: expose `--inactive-days` while keeping the assignment's 30-day default.
- Alternative: hard-code 30 days or introduce a full policy configuration file.
- Cost accepted: the CLI has one additional option and callers can choose a
  threshold that differs from the assignment default.
- What would change my mind: a repository policy standard that requires all
  checks to come from a shared configuration document.
- Receipt: [`44661b4`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/44661b4) records the bounded agent session that implemented and tested `--inactive-days` while retaining the 30-day default.

## Decision 10 - Explicit opt-in label workflow

- Choice: keep ordinary CLI runs read-only and require `--apply-needs-attention`, a
  stale-PR validation, an interactive confirmation, and a fresh verification read
  for the single supported GitHub write.
- Alternative: automatically label every stale pull request during a health check.
- Cost accepted: one extra command, prompt, and network read when an operator really
  wants the action.
- What would change my mind: a separately governed batch-action service with its own
  review queue and audit trail.
- Receipt: [`ff6c746`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/ff6c746) added the confirmation and verification path; [`555ce03`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/555ce03) narrowed its MCP scope; [PR #4](https://github.com/RamithaMN/Github_Copilot_assignment/pull/4) and the [MCP write receipt](docs/evidence/github-mcp-write-attempt.md) preserve the failed-first and successful retry.
