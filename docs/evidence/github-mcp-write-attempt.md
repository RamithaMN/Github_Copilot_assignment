# GitHub MCP Write Loop Evidence

## Scope

- Date: 2026-09-26
- Copilot CLI: 1.0.88
- Repository: `RamithaMN/Github_Copilot_assignment`
- Candidate: PR #4, `Complete Q2 agentic session evidence`
- Candidate URL: https://github.com/RamithaMN/Github_Copilot_assignment/pull/4
- MCP server: `github-mcp-server-approved-write`

The repository search found no open pull request older than 30 days in the
repositories controlled by the authenticated account. PR #4 was created on
2026-09-26, so it is not a 30-day stale PR. To test the write path without
misrepresenting its age, the session used the product's supported
`inactive_days=0` demo override and stated that deviation explicitly. The
default product rule remains more than 30 days and is covered by tests.

## Failed iteration and setup correction

The first write-capable session used the scoped server without a runtime
authorization header. It reached the approval prompt, but the MCP call failed:

```text
403: Must have admin rights to Repository
```

No label was changed. The setup was corrected rather than hand-patching the
result: `.github/mcp.json` now references the runtime-only substitution
`${COPILOT_MCP_GITHUB_TOKEN}` in the approved-write server's Authorization header.
The token was supplied only to the Copilot process and was never committed.

The session was rerun with the same narrow tool set and explicit approval gate.

## Fetch and decision

The read-only MCP session fetched the live PR list and returned PR #4 with:

```text
number: 4
updated_at: 2026-09-26T18:26:46Z
```

The initial list response did not include labels, and the first label-read attempts
could not resolve PR #4 as an issue. The agent reported that limitation rather than
inventing a before state. The repository label `needs-attention` was created as a
one-time setup prerequisite; the MCP action itself only applied that existing label.

The agent explicitly decided that PR #4 was not 30-day stale and used
`inactive_days=0` only to exercise the controlled action path.

## Exact tool boundary

The Copilot CLI session enabled only these additional built-in GitHub MCP tools:

```text
--add-github-mcp-tool issue_write
--add-github-mcp-tool issue_read
--add-github-mcp-tool pull_request_read
--add-github-mcp-tool label_write
```

The historical session enabled the four read/write tools above. The final committed
workspace write server is narrower: it exposes `list_pull_requests`,
`get_pull_request`, `issue_read`, and `issue_write`; `label_write` is not enabled
because the observed action used `issue_write`. Repository authentication was
supplied at runtime:

```json
"headers": {
  "Authorization": "Bearer ${COPILOT_MCP_GITHUB_TOKEN}"
}
```

The session prompt prohibited bash, `gh`, REST, and web tools. It requested an
approval immediately before this single intended operation:

```json
{
  "owner": "RamithaMN",
  "repo": "Github_Copilot_assignment",
  "method": "update",
  "issue_number": 4,
  "labels": ["needs-attention"]
}
```

The Copilot approval prompt stated that the approval authorized only one label
update and no other PR changes. The approval was explicitly accepted, followed by
the separate MCP tool-use confirmation for the exact payload.

## Action and verification

The corrected MCP call succeeded and returned a GitHub issue/PR response with id
`5596269253`. Copilot then re-fetched the PR through MCP. The after-state contained:

```text
PR #4 labels: ["needs-attention"]
```

An independent GitHub read confirmed the same state:

```json
{
  "number": 4,
  "state": "OPEN",
  "updatedAt": "2026-09-26T19:08:26Z",
  "labels": ["needs-attention"]
}
```

The demonstrated loop is therefore:

```text
FETCH -> DECIDE -> APPROVE -> ACT -> RE-FETCH -> VERIFY
```

The only qualification is intentional and visible: the live candidate was not
30-day stale, so `inactive_days=0` was used for the controlled write-path demo.
The implementation does not claim otherwise.

## Context cost and trimming

The historical read-only configuration exposed five tools and the write session
added four action tools. The final committed configuration exposes only two read
tools and four approved-write tools; the exact reduction is measured in
`docs/evidence/github-mcp-context-cost.md`.
Repository-wide search, diffs, comments, actions, merges, branch writes, file writes,
and deletion tools were excluded.

The prompt narrowed the context to one repository and one PR and requested only
number, timestamps, state, and labels. It omitted bodies, diffs, files, comments,
and check runs. The tradeoff was one extra label-read attempt when the list response
omitted labels, plus the cost of initializing the read-only and approved-write
servers. The runtime token was not placed in the repository or prompt transcript.
