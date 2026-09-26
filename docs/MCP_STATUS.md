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
requested approval immediately before the `issue_write` call. The first approved
attempt returned `403: Must have admin rights to Repository`. The setup was corrected
by adding an authenticated runtime-only `Authorization` header, and the approved
retry applied `needs-attention`. Copilot re-fetched the PR and verified the label;
an independent `gh` read confirmed it.

The repository had no open PR older than 30 days, so the session used the product's
explicit `inactive_days=0` demo override only to exercise the action boundary. PR #4
was created on 2026-09-26 and was explicitly not described as 30-day stale. The
default product rule remains more than 30 days, and its boundary is covered by tests.

The complete failed-first-iteration and successful-retry loop are recorded in
`docs/evidence/github-mcp-write-attempt.md`.

## Context cost and trimming

The read-only server exposes five tools: `get_file_contents`, `list_issues`,
`issue_read`, `list_pull_requests`, and `get_pull_request`. The write attempt added
only the four tools needed for label setup, label reads, and one issue/PR update.
Repository-wide search, diffs, comments, actions, merges, branch writes, file writes,
and deletion tools were excluded.

The MCP prompt narrowed the context to one repository and one PR, requested only
`number`, `updated_at`, state, and labels, and omitted bodies, diffs, files, comments,
and check runs. This reduced prompt and response size. The list response still did
not contain labels, so a second label-read call was required; after the runtime
authentication fix, that re-fetch returned the label. The extra verification call,
the two-server initialization, and the added write-tool descriptions are the measured
costs of the scoped setup.

Each configuration intentionally exposes only the operations needed for its loop:
read-only metadata tools in the default server and the separately named approved-write
server. Credentials belong in the environment, never in this repository.
