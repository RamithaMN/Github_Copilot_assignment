# GitHub MCP Token Telemetry Receipt

This is a measured follow-up run, not a retroactive estimate of the 2026-09-26
write session. Copilot CLI 1.0.88 was run on 2026-09-27 with
`--usage-output-file` enabled and a read-only GitHub MCP prompt. The session made
one `list_pull_requests` call for `RamithaMN/Github_Copilot_assignment`, returned
`[]`, made no file changes, and performed no write.

## Captured usage

The redacted usage JSON reported:

```json
{
  "totalUserRequests": 1,
  "totalPremiumRequestCost": 1,
  "totalNanoAiu": 65744000,
  "inputTokens": 9195,
  "outputTokens": 65,
  "cacheReadTokens": 4559,
  "cacheWriteTokens": 4630,
  "lastCallInputTokens": 4633,
  "lastCallOutputTokens": 11,
  "totalApiDurationMs": 3092,
  "model": "gpt-6-luna"
}
```

The Copilot session usage checkpoint attributed `1008` tokens to the two enabled
MCP tool definitions:

```text
github-mcp-server-list_pull_requests
github-mcp-server-pull_request_read
tool_tokens: 1008
tools_truncated: 0
```

The MCP result was `[]` and measured `2` result-content bytes. These figures are
the exact exported values for this follow-up run. They are not claimed to be the
historical write session's cost.

## Reproduction

```bash
copilot -C . --no-color --no-auto-update --experimental \
  --output-format json \
  --usage-output-file /tmp/github-mcp-usage.json \
  --add-github-mcp-tool list_pull_requests \
  --add-github-mcp-tool pull_request_read \
  -p "Use only GitHub MCP read tools. Fetch open pull requests for RamithaMN/Github_Copilot_assignment and return only number, updated_at, state, and labels. Do not use shell, web, REST, or write tools. Stop after the read."
```

The temporary usage file was inspected and only the numeric, non-secret fields
above were committed. No token or credential value was recorded.
