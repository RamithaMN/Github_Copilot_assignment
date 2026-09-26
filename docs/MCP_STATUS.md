# MCP Status

The repository contains an intentionally scoped intended configuration at
`docs/mcp/github-mcp.intended.json`.

## Observed environment

At implementation time, the `copilot` executable was not available. The available
environment exposed Codex and GitHub CLI, but not a GitHub Copilot CLI or a known
Copilot MCP configuration directory. Therefore no actual Copilot MCP server
activation or fetch-decide-act-verify loop is claimed here.

## Intended loop

When run in a supported Copilot environment, the agent should fetch open pull
requests, classify stale items using `updated_at` and the 30-day rule, request
approval, apply the `needs-attention` label, and re-fetch to verify the label.

The configuration intentionally exposes only the operations needed for that loop.
Credentials belong in the environment, never in this repository.

