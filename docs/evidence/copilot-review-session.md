# Copilot Review Evidence

## Session metadata

- CLI: GitHub Copilot CLI 1.0.88
- Account: `rohitsundaram`
- Agent: `repo-reviewer`
- Repository: this project
- Session name: `repo-reviewer-session-3`
- Permission boundary: `view`, `glob`, and `grep` only
- Explicitly unavailable: shell, file writes, web fetch, tasks, and GitHub MCP tools

## Observed context loading

Copilot discovered:

- `.github/copilot-instructions.md`
- `.github/instructions/tests.instructions.md`
- `.github/agents/repo-reviewer.agent.md`
- The local repository-health plugin directory

It read the source, test, workflow, approval, decision, MCP, and plugin files without
editing them. The session reported zero file changes.

## What went wrong and what changed

The first review attempt reported:

```text
[plugin-dir] no plugin.json or SKILL.md found in .../plugins/repository-health-review
```

The local plugin initially had only the Codex-specific
`.codex-plugin/plugin.json`. Copilot requires `plugin.json` at the plugin root, so the
root manifest was added. The next session loaded the plugin directory without that
warning.

The first bounded command also used invalid `read` and `search` tool names. Copilot
reported them as unknown. The corrected session used the actual `view`, `glob`, and
`grep` tool names exposed by the CLI.

## Verification boundary

The session was a review only. It did not run shell commands, access GitHub MCP, edit
files, or claim test results. Its later resumed summary incorrectly claimed that the
source and tests had not been inspected even though the session log showed them being
read. That contradiction is recorded as a trust failure and is why the human remains
responsible for the authoritative pytest and plugin-validation results.

## Q1 before and after

Before the instruction was added, the first bounded review attempt guessed the tool
names `read` and `search`. Copilot reported both as unknown tools and the attempt did
not perform the intended review.

The instruction added after that failure was:

```text
Use only tool names exposed by the current Copilot session; never invent tool names.
If a requested tool is unavailable, report that limitation and stop rather than guessing.
```

After the instruction, the corrected session used `view`, `glob`, and `grep`, recorded
the files it read, reported that it did not run shell commands, and made a bounded
review finding. The later resumed-summary contradiction is also recorded as a separate
trust failure; the trace-authority instruction was added for that case as well.
