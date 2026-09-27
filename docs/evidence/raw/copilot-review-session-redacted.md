# Redacted Copilot Review Session Excerpt

This excerpt preserves the observed review failure and correction from the bounded
`repo-reviewer` sessions. It excludes encrypted reasoning and unrelated file-list
output. The session had only `view`, `glob`, and `grep`; shell, edit, web, and MCP
tools were unavailable.

## First attempt

```text
[plugin-dir] no plugin.json or SKILL.md found in .../plugins/repository-health-review

Unknown tool: read
Unknown tool: search
```

## Corrected instruction

```text
Use only tool names exposed by the current Copilot session; never invent tool names.
If a requested tool is unavailable, report that limitation and stop rather than guessing.
```

## Corrected session trace

```text
MD Read copilot-instructions.md 11 lines read
PY Read main.py 38 lines read
PY Read test_main.py 52 lines read
```

The corrected session reported shell commands were disabled and made zero file
changes. The root plugin manifest and tool-name instruction were then preserved in
the repository history.
