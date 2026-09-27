# GitHub MCP Context Cost

The Copilot CLI did not provide token accounting for the MCP handshake in the
captured session. To avoid inventing token counts, this record uses reproducible
character counts as a lower-level proxy and records the exact tool reduction.

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

The higher-value context trimming was semantic: one repository and one PR, with
`number`, `updated_at`, state, and labels requested. Bodies, diffs, files, comments,
reviews, check runs, repository-wide search, merge, branch, deletion, and Actions
tools were omitted. The cost accepted was one additional verification read after the
list response omitted labels, plus separate read-only and approved-write server
initialization.
