# Decisions

## Decision 1 - CLI instead of web application

- Choice: build a Python CLI.
- Alternative: build a web dashboard.
- Cost accepted: less visual polish and no persistent user interface.
- What would change my mind: a requirement for multi-user monitoring or scheduled reports.

## Decision 2 - REST adapter for the product

- Choice: keep the application behind `github_service.py` using the GitHub REST API.
- Alternative: make the CLI an MCP client.
- Cost accepted: the product and assignment MCP demonstration use separate integrations.
- What would change my mind: a requirement for the product itself to consume MCP tools.

## Decision 3 - Read-only default

- Choice: local checks and GitHub reads are the default behavior.
- Alternative: automatically comment on or label every stale pull request.
- Cost accepted: findings require a separate approved action.
- What would change my mind: a controlled operational workflow with explicit write authorization.

## Decision 4 - Thirty-day stale threshold

- Choice: stale means no activity for more than 30 days, measured by `updated_at`.
- Alternative: use creation date or a 90-day threshold.
- Cost accepted: the rule is intentionally simple and may not fit every team.
- What would change my mind: a repository-specific policy supplied as a documented configuration.

## Decision 5 - Fixed MVP checks

- Choice: implement the assignment's fixed checks first.
- Alternative: build a general policy-file engine.
- Cost accepted: teams cannot customize every rule in v1.
- What would change my mind: repeated use across repositories with materially different policies.

## Decision 6 - pytest

- Choice: use pytest as the primary test runner.
- Alternative: use unittest only.
- Cost accepted: one development dependency is required.
- What would change my mind: an environment policy that permits only the standard library.

## Decision 7 - Adapter boundary

- Choice: all external GitHub operations go through `github_service.py`.
- Alternative: call GitHub directly from each checker.
- Cost accepted: a small amount of adapter code.
- What would change my mind: removal of external checks from the product.

## Decision 8 - No numeric health score

- Choice: report named statuses with evidence.
- Alternative: calculate a 0-100 score.
- Cost accepted: results are less convenient to rank.
- What would change my mind: a validated scoring policy with user-agreed weights.

