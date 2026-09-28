# Evidence Index

This index maps the material claims in the submission to a receipt. Commit links
point to the public repository history; session links point to redacted excerpts
copied from the local Copilot CLI event store. Secrets, encrypted model reasoning,
and unrelated repository listings are omitted.

| Claim | Receipt |
| --- | --- |
| The health-check CLI exists and has focused tests. | [`c11d18b`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/c11d18b) |
| Copilot context includes a before/after tool correction. | [`b55ed4b`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/b55ed4b), [`3bb63fd`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/3bb63fd), [redacted review transcript](raw/copilot-review-session-redacted.md) |
| A bounded agent changed multiple files, read a failure, and reran tests. | [`7c34db9`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/7c34db9), [redacted Q2 transcript](raw/copilot-q2-session-redacted.md) |
| A bounded reviewer setup failed, was corrected through instructions/tools, and was rerun read-only. | [reviewer-correction receipt](agent-session-q2-reviewer-correction.md), [`3bb63fd`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/3bb63fd) |
| A separate custom-agent reviewer session found the missing CLI coverage, with its own session ID and verbatim finding; the human follow-up is linked directly. | [third reviewer session](agent-session-q2-third-reviewer-2026-09-27.md), [`d72b973`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/d72b973) |
| The exact Q2 stopping marker was captured in a separate bounded follow-up with exit code 0 and no file changes. | [stopping-marker receipt](agent-session-q2-stopping-marker-2026-09-27.md) |
| The reviewer agent was restricted to read-only tools. | [`b82f63d`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/b82f63d) |
| Real approval prompts included an allow and a refusal. | [`ac09ada`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/ac09ada), [approval records](copilot-approval-prompts.md) |
| The MCP write first failed, then succeeded after runtime authentication was fixed. | [`7cdf202`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/7cdf202), [`ea7fa6a`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/ea7fa6a), [redacted MCP transcript](raw/copilot-mcp-session-redacted.md), [PR #4](https://github.com/RamithaMN/Github_Copilot_assignment/pull/4) |
| A follow-up MCP run recorded exact token/tool telemetry. | [token telemetry receipt](github-mcp-token-telemetry-2026-09-27.md), [context-cost analysis](github-mcp-context-cost.md) |
| Historical MCP write sessions have exact event-store usage receipts. | [historical telemetry receipt](github-mcp-historical-token-telemetry.md) |
| Slow, unavailable, and malformed MCP responses stop safely without writes. | [failure simulation receipt](github-mcp-failure-simulations-2026-09-27.md) |
| Q4 plugin vetting, persisted permission state, sandboxing, and enterprise impact were observed. | [Q4 permission-state receipt](q4-permission-state-2026-09-27.md) |
| The Q5 decision log has a receipt for every decision. | [DECISIONS.md](../../DECISIONS.md) |
| The current suite passes. | [latest verification receipt](latest-verification.md) |
| The final branch history is preserved without squashing. | `main` contains merge commit [`81fc311`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/81fc311) plus follow-up merge [`d235f2f`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/d235f2f); the source branch contains [`ce91d8c`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/ce91d8c). |

The last row is intentionally explicit: the submission is now on `main` through
regular merge commits, and the source branch remains available for inspection.
