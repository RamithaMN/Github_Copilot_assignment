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

Applying `needs-attention` remains an explicit opt-in action. It requires a separate
Copilot session enabling the exact GitHub label-update tool and a user approval at the
moment of the write, followed by a fresh read to verify the label.

The configuration intentionally exposes only the operations needed for the read loop.
Credentials belong in the environment, never in this repository.
