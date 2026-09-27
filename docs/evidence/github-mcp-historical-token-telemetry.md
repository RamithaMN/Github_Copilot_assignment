# Historical MCP Token Telemetry Receipt

The earlier statement that the historical MCP session had no recoverable token
telemetry was too broad. Copilot CLI's local event store retained usage
checkpoints and shutdown receipts for both the failed first write and the
successful retry. The raw event files remain outside the repository because
they contain encrypted model-call identifiers; this file preserves the relevant
redacted numeric fields and tool names.

## Successful retry

Session: `76b3d362-5bbb-4964-97d8-0a5c9d52890b`  
Date: 2026-09-26  
Operation: approved MCP label write followed by verification

The event-store `session.usage_checkpoint` recorded:

```text
model: gpt-6-luna
tool_count: 26
tool_tokens: 10319
prompt_tokens: 19763
cache_read: 19311
cache_write: 449
```

The same checkpoint listed the enabled GitHub MCP tools:

```text
github-mcp-server-get_file_contents
github-mcp-server-issue_read
github-mcp-server-list_issues
github-mcp-server-list_pull_requests
github-mcp-server-approved-write-issue_read
github-mcp-server-approved-write-issue_write
github-mcp-server-approved-write-list_pull_requests
```

The `session.shutdown` receipt recorded the complete session totals:

```text
inputTokens: 143296
outputTokens: 2227
cacheReadTokens: 123512
cacheWriteTokens: 19760
reasoningTokens: 1456
toolDefinitionsTokens: 10031
currentTokens: 21355
totalApiDurationMs: 26592
```

## Failed first attempt

Session: `2c812966-bbf2-4390-b306-f7609fa1c6ab`  
Operation: approved write rejected by GitHub with `403 Must have admin rights to Repository`

Its shutdown receipt recorded:

```text
inputTokens: 106822
outputTokens: 2477
cacheReadTokens: 87631
cacheWriteTokens: 19173
reasoningTokens: 1717
toolDefinitionsTokens: 10031
currentTokens: 19878
totalApiDurationMs: 29170
```

These are exact provider-reported session totals. Copilot does not expose a
separate token subtotal for only the MCP definitions inside `tool_tokens`; the
receipt therefore reports the exact total tool-definition cost and the exact
MCP tool inventory rather than inventing an MCP-only split.

## Capture method and limitation

The historical write sessions did not use `--usage-output-file`, OpenTelemetry,
or a slash-command snapshot. Their event-store checkpoint and shutdown records
are the authoritative telemetry that was actually retained. A later attempt to
resume the successful session with `-p "/context"` was recorded as an ordinary
prompt and did not produce a `/context` snapshot; that failed capture is not
presented as success.

A separate fresh read-only run did use `--usage-output-file`; its receipt is
`github-mcp-token-telemetry-2026-09-27.md`. It is a new measurement, not a
retroactive replacement for the historical write session.
