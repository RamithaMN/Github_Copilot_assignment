# GitHub MCP Write Attempt Evidence

## Scope

- Date: 2026-09-26
- Copilot CLI: 1.0.88
- Repository: `RamithaMN/Github_Copilot_assignment`
- Candidate: PR #4, `Complete Q2 agentic session evidence`
- Candidate URL: https://github.com/RamithaMN/Github_Copilot_assignment/pull/4
- Managed MCP server: `github-mcp-server`

The repository search found no open pull request older than 30 days in the
repositories controlled by the authenticated account. PR #4 was created on
2026-09-26, so it is not a 30-day stale PR. To test the write boundary without
misrepresenting its age, the session used the product's supported
`inactive_days=0` demo override and stated that deviation explicitly.

## Read and decision

The read-only MCP session fetched the live PR list and returned PR #4 with:

```text
number: 4
updated_at: 2026-09-26T18:26:46Z
```

The list response did not include labels. A follow-up MCP label read was attempted,
but the managed server could not resolve PR #4 as an issue for that operation. The
agent therefore reported that the before-label state could not be established,
rather than inventing an empty result.

The harmless repository label `needs-attention` was created as a one-time setup
prerequisite with the authenticated GitHub CLI. The MCP write session was limited to
applying that existing label; it was not permitted to merge, comment, edit files, or
change PR state.

## Exact write-session boundary

The Copilot CLI was started with these additional built-in MCP tools:

```text
--add-github-mcp-tool issue_write
--add-github-mcp-tool issue_read
--add-github-mcp-tool pull_request_read
--add-github-mcp-tool label_write
```

The session prompt prohibited bash, `gh`, REST, and web tools. It required an
explicit approval immediately before this single intended operation:

```json
{
  "owner": "RamithaMN",
  "repo": "Github_Copilot_assignment",
  "method": "update",
  "issue_number": 4,
  "labels": ["needs-attention"]
}
```

The Copilot approval prompt said:

```text
Yes authorizes a single label update to PR #4; no other labels or changes will be made.
```

The approval was explicitly accepted.

## Action result and verification

The GitHub MCP server rejected the approved write:

```text
403: Must have admin rights to Repository
```

The agent stopped without retrying through another tool. Its post-action MCP read
also could not resolve the label state. An independent GitHub read confirmed the
external state was unchanged:

```json
{
  "number": 4,
  "state": "OPEN",
  "updatedAt": "2026-09-26T18:26:46Z",
  "labels": []
}
```

This is the honest end-to-end result available in the installed environment:

```text
FETCH -> DECIDE -> APPROVE -> ATTEMPT ACT -> POLICY BLOCK -> VERIFY NO CHANGE
```

The full successful `ACT -> VERIFY label present` loop cannot be claimed because
the managed GitHub MCP server requires repository-admin permission that the
authenticated account did not have for this repository. The committed configuration
and this transcript preserve the exact intended write surface without credentials.
