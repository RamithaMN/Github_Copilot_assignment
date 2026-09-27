# GitHub MCP Context Cost

The first version of this record said that the historical MCP session had no
recoverable token telemetry. That was too broad. Copilot CLI's local event store
retained exact usage checkpoints and shutdown receipts for both historical write
sessions. The redacted receipt is
`github-mcp-historical-token-telemetry.md`.

The historical sessions did not use `/context`, `/usage`, `--usage-output-file`,
or OpenTelemetry. A resumed `/context` capture was attempted later, but Copilot
treated the non-interactive input as an ordinary prompt; that failed attempt is
explicitly not counted as a snapshot. The event-store receipts are therefore the
authoritative historical measurement, while the separate fresh run below proves
the supported `--usage-output-file` path.

This record therefore uses reproducible character counts as a lower-level proxy and
records the exact tool reduction. The proxy is clearly not a provider token count.

Measured from the committed configuration on 2026-09-27:

| Configuration | Tools | Tool-name characters | Minified server JSON characters |
| --- | ---: | ---: | ---: |
| Earlier read server | 5 | 72 | 163 |
| Final read server | 2 | 34 | 116 |
| Earlier approved-write server | 5 | 66 | 214 |
| Final approved-write server | 4 | 55 | 200 |

The read tool-name surface therefore fell from 5 tools to 2, a reduction of 38 tool
name characters. The approved-write surface fell from 5 tools to 4, a reduction of
11 tool name characters. The final `.github/mcp.json` is 25 lines and 561 bytes;
the earlier version was 29 lines and 658 bytes. These are configuration proxies, not
claims about the provider's hidden tokenization.

## Measured follow-up

A read-only follow-up run with `--usage-output-file` captured exact telemetry. It
reported `9,195` input tokens, `65` output tokens, `4,559` cache-read tokens, and
`4,630` cache-write tokens. Its session checkpoint attributed `1,008` tokens to the
two enabled MCP tool definitions. The MCP call returned `[]` in `2` result-content
bytes and took `3,092 ms` of API time. The full redacted receipt is
`docs/evidence/github-mcp-token-telemetry-2026-09-27.md`.

This is a new measured read-only run. It complements, rather than replaces, the
historical event-store telemetry; it does not change the historical write outcome.

For a future measurement, capture `/context` before and after MCP activation, capture
`/usage` at the end of the session, and enable Copilot CLI OpenTelemetry file export
with `COPILOT_OTEL_ENABLED=true` and `COPILOT_OTEL_FILE_EXPORTER_PATH`. The OTel
`gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, and
`gen_ai.tool.definitions` attributes can then be retained as the receipt. See the
[Copilot CLI context-management documentation](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management)
and [CLI command reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference).

The higher-value context trimming was semantic: one repository and one PR, with
`number`, `updated_at`, state, and labels requested. Bodies, diffs, files, comments,
reviews, check runs, repository-wide search, merge, branch, deletion, and Actions
tools were omitted. The cost accepted was one additional verification read after the
list response omitted labels, plus separate read-only and approved-write server
initialization.
