# Q4 Permission and Plugin Vetting Receipt

Observed on 2026-09-27 with GitHub Copilot CLI 1.0.88. This receipt records the
actual local permission state and the plugin review; it does not infer persistence
from the assignment brief.

## Persisted state

The Copilot state directory was inspected for permission, URL, and settings files:

```text
$ find ~/.copilot -maxdepth 3 -type f \( -iname '*permission*' -o -iname '*config*' -o -iname '*setting*' -o -iname '*url*' \)
~/.copilot/config.json
~/.copilot/settings.json
```

The observed contents were:

```json
// ~/.copilot/config.json (permission-relevant fields only)
{
  "lastLoggedInUser": {"host": "https://github.com", "login": "rohitsundaram"},
  "loggedInUsers": [{"host": "https://github.com", "login": "rohitsundaram"}]
}
```

```json
// ~/.copilot/settings.json
{
  "experimental": true
}
```

No durable `permissions-config.json`, `allowedUrls`, path allowlist, or tool
allowlist was present in the inspected state. The saved state contained account
login metadata and the experimental flag, not the session approvals used for this
assignment.

The folder-trust prompt was answered with `1. Yes`, explicitly for the current
session only; the exact prompt and decision are preserved in
`copilot-approval-prompts.md`. The refusal of `/tmp/copilot-approval-refusal.txt`
also produced no file. Therefore the observed persistence boundary was:

```text
session-only folder trust and tool approvals -> gone after the session
account login and experimental setting       -> remained in ~/.copilot state
```

No reset command was needed because no durable permission state was created. The
repository policy still requires reviewing and resetting any future persisted
allowlist when the task or repository changes.

## CLI permission semantics

The installed CLI help reported:

```text
Denial rules always take precedence over allow rules, even --allow-all-tools.
By default, file access is restricted to paths within the current working
directory and its subdirectories, plus the system temporary directory.
```

The assignment sessions did not use `--allow-all`, `--yolo`, or
`--allow-all-paths`. The repository-reviewer session exposed only `view`, `glob`,
and `grep`; the Q2 implementation session separately allowed only the tools needed
for the bounded code change.

## Plugin vetting

The authored plugin was reviewed before use:

| Surface | Observed result | Decision |
| --- | --- | --- |
| Root manifest | `plugins/repository-health-review/plugin.json` is valid JSON and declares no tools, hooks, MCP servers, or credentials. | Allow as a small reusable capability. |
| Codex manifest | The optional `.codex-plugin/plugin.json` compatibility file was removed before submission. | Keep the submission focused on the Copilot plugin route. |
| Skill | `skills/repository-health-review/SKILL.md` is read-oriented and requires evidence-backed `PASS`, `WARNING`, `FAIL`, or `UNKNOWN` findings. | Allow; no shell, write, or GitHub-write instruction. |
| Network/MCP | No network endpoint or MCP server is declared by the plugin. | No additional network access. |
| Credentials | No token, secret, or credential lookup is declared. | Credentials remain environment-only. |

The first Copilot review reported that the root `plugin.json` was missing. Adding
that manifest corrected discovery; the before/after is recorded in
`copilot-review-session.md` and the correction is in commit `3bb63fd`.

## Permission tightening

The initial MCP design exposed five read/write tools. The committed correction
narrowed the default read server to two pull-request tools and kept four metadata
and action tools behind a separately named approved-write server. The change is
recorded by commits `ea7fa6a` and `36d6551`, with the final state in
`.github/mcp.json`. The read-only reviewer was independently narrowed to
`view`, `glob`, and `grep` in commit `b82f63d`.

## Enterprise-policy impact

| Actual restriction | Effect on this submission | Preserved redesign |
| --- | --- | --- |
| MCP disabled | The live GitHub MCP loop cannot run. | Keep the committed intended config; use the CLI REST adapter for product behavior and mark MCP unavailable. |
| `--allow-all` blocked | Nothing essential breaks. | Continue with narrow tool allowlists and explicit approvals. |
| Plugin activation blocked | The reusable skill cannot load. | Keep the reviewed source and manifest; use repository instructions and the bounded custom agent. |
| Agent restricted to one directory | Outside-project writes and broad inspection are unavailable. | Keep the workflow inside the repository and request separate approval for external verification. |
