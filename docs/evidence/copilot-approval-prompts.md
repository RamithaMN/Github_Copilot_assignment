# Copilot Approval Evidence

These are real approval decisions observed in GitHub Copilot CLI 1.0.88 on
2026-09-26. They are recorded as evidence, not as example prompts.

## Session A: folder trust

Command:

```bash
copilot -C . --available-tools bash --mode interactive \
  -i "Run exactly: python3.12 -m pytest -q. Do not edit files."
```

Observed prompt:

```text
Confirm folder trust
/Users/rohitsundaram/PycharmProjects/Github_copilot_assignment
Do you trust the files in this folder?
1. Yes
2. Yes, and remember this folder for future sessions
3. No (Esc)
```

Decision: selected `1. Yes` for this session only. I did not persist folder trust.

## Session B: allow local verification

Observed prompt:

```text
Run pytest with Python 3.12
python3.12 -m pytest -q
Do you want to run this command?
1. Yes
2. No, and tell Copilot what to do differently (Esc to stop)
```

Decision: selected `1. Yes` because this was the requested, local, non-destructive
verification command. Observed result:

```text
python3.12 -m pytest -q completed successfully: 13 passed in 0.03s.
```

## Session C: refuse out-of-scope path access

Prompt:

```text
Create /tmp/copilot-approval-refusal.txt with the text refusal-test.
Do not modify the repository.
```

Observed prompt:

```text
Allow path access
This action may read or write the following path outside the paths currently
allowed for this session.
/tmp/copilot-approval-refusal.txt
Do you want to allow this?
1. Yes
2. Yes, and remember this path for this session
3. No (Esc)
```

Decision: selected `3. No`. Copilot reported:

```text
The user rejected this tool call.
```

No repository file was changed and the requested temporary file was not created.

## Session D: MCP write approval

The following is the redacted permission event emitted by Copilot CLI immediately
before the external write. It is the exact structured approval payload, rather than a
paraphrase of the action:

```json
{
  "kind": "mcp",
  "serverName": "github-mcp-server-approved-write",
  "toolName": "github-mcp-server-approved-write-issue_write",
  "args": {
    "owner": "RamithaMN",
    "repo": "Github_Copilot_assignment",
    "issue_number": 4,
    "method": "update",
    "labels": ["needs-attention"]
  }
}
```

Decision: selected approval for this exact one-label update. The first invocation
returned `403: Must have admin rights to Repository`; after the runtime-only
Authorization header was added, the same approved operation succeeded and the
re-fetch verified `needs-attention`. The full redacted event excerpt is in
`docs/evidence/raw/copilot-mcp-session-redacted.md`.
