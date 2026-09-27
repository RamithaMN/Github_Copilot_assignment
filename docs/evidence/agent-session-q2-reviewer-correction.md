# Q2 Agent Session: Reviewer Setup Correction

This is the second of the three Q2 sessions. It demonstrates a failed bounded
review setup followed by a configuration/instruction correction, not a production
code edit.

## Initial bounded session

- CLI: GitHub Copilot CLI 1.0.88
- Agent: `repo-reviewer`
- Permission boundary: `view`, `glob`, and `grep`
- Disabled: shell, edit, web, task delegation, and GitHub MCP tools
- Scope: inspect repository health and report observed findings

The observed first attempt failed in two setup ways:

```text
[plugin-dir] no plugin.json or SKILL.md found in .../plugins/repository-health-review
Unknown tool: read
Unknown tool: search
```

The complete redacted excerpt is in
`docs/evidence/raw/copilot-review-session-redacted.md`.

## Setup correction

The human corrected the agent context rather than patching a review result:

```text
Use only tool names exposed by the current Copilot session; never invent tool names.
If a requested tool is unavailable, report that limitation and stop rather than guessing.
```

The instruction is present in `.github/copilot-instructions.md` and is preserved by
commit [`6feeb12`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/6feeb12).
The root Copilot plugin manifest is preserved by
[`3fab71e`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/3fab71e).
The evidence deliberately distinguishes those two setup corrections rather than
claiming that the agent edited the plugin itself during the review.

## Corrected rerun and verification boundary

The corrected bounded command was:

```bash
copilot -C . --agent repo-reviewer \
  --available-tools view,glob,grep --mode interactive \
  -i "Review the repository context and report only files actually inspected. Do not run shell commands or edit files. If a summary conflicts with the read trace, follow the trace."
```

The observed trace included:

```text
MD Read copilot-instructions.md 11 lines read
PY Read main.py 38 lines read
PY Read test_main.py 52 lines read
```

The rerun reported zero file changes, kept shell unavailable, and used only the
exposed read tools. The full follow-up and human verification are in
`docs/evidence/copilot-review-session-2026-09-26.md`.
