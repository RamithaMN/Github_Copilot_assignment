# Q2 Evidence: Exact Stopping Marker Capture

The earlier reviewer receipt documented a successful stop but did not preserve a
separate final-text event containing the requested marker. This fresh bounded run
closed that evidence gap.

## Session identity

- **Session type:** custom read-only `repo-reviewer` follow-up
- **Copilot CLI:** 1.0.88
- **Session ID:** `6bdc024a-bd99-472c-8170-b811e380fcef`
- **Started:** `2026-09-27T16:07:10.992Z` (`2026-09-27 20:07:10 +04:00`)
- **Final response event:** `2026-09-27T16:07:16.343Z`
- **Exit code:** `0`
- **Working fixture:** `/private/tmp/q2-marker-final.qr9cY1`

The fixture was an archive of the submitted `HEAD`. It was separate from the
submission worktree. Only the `view` tool was available; shell, edit, create,
network, delegation, and all GitHub MCP tools were disabled.

## Exact stopping instruction

```text
Perform one bounded read-only review. Use only the view tool to inspect src/main.py, then stop. Your final response must contain exactly two lines. The first line must be: CLI entrypoint inspected; review complete. The second line must be exactly: STOP: REVIEW COMPLETE. Do not add punctuation after the second line and do not call any more tools after the view.
```

The agent made one `view` call for `src/main.py`, then made no further tool calls.
The preserved final `assistant.message` content was exactly:

```text
CLI entrypoint inspected; review complete.
STOP: REVIEW COMPLETE
```

The CLI result reported `exitCode: 0`, zero added lines, zero removed lines, and
an empty modified-file list. This receipt proves the literal stopping marker,
not just successful termination.
