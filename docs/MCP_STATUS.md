# MCP Status

The repository contains the actual Copilot workspace configuration at
`.github/mcp.json`. The older `docs/mcp/github-mcp.intended.json` remains as the
assignment-facing design record.

## Observed environment

GitHub Copilot CLI 1.0.88 is installed and authenticated as `rohitsundaram`.
Copilot documents a built-in `github-mcp-server`; the committed workspace config
uses GitHub's read-only remote MCP endpoint and allowlists only repository metadata
tools. No credentials are committed.

## Read loop

The configured safe loop is to fetch open pull requests, classify stale items using
`updated_at` and the 30-day rule, and report the result. The read-only configuration
does not expose GitHub writes.

## Write loop

The write path was tested against controlled PR #4 in
`RamithaMN/Github_Copilot_assignment`. Copilot was started with the exact additional
tools `issue_write`, `issue_read`, `pull_request_read`, and `label_write`, and it
requested approval immediately before the `issue_write` call. The approval was
granted, but GitHub returned `403: Must have admin rights to Repository`. The PR
remained unlabeled, and no successful external write is claimed.

The repository had no open PR older than 30 days, so the session used the product's
explicit `inactive_days=0` demo override only to exercise the action boundary. PR #4
was created on 2026-09-26 and was explicitly not described as 30-day stale. The
default product rule remains more than 30 days, and its boundary is covered by tests.

The complete attempted loop and the policy block are recorded in
`docs/evidence/github-mcp-write-attempt.md`.

## Context cost and trimming

The read-only server exposes five tools: `get_file_contents`, `list_issues`,
`issue_read`, `list_pull_requests`, and `get_pull_request`. The write attempt added
only the four tools needed for label setup, label reads, and one issue/PR update.
Repository-wide search, diffs, comments, actions, merges, branch writes, file writes,
and deletion tools were excluded.

The MCP prompt narrowed the context to one repository and one PR, requested only
`number`, `updated_at`, state, and labels, and omitted bodies, diffs, files, comments,
and check runs. This reduces prompt and response size, but the narrow response also
caused the list call to omit labels; a second label-read call was required and failed
under the managed server's repository-permission policy. That extra call and the
two-server initialization are the measured costs of the scoped setup.

The configuration intentionally exposes only the operations needed for the read loop.
Credentials belong in the environment, never in this repository.
