# Evidence Index

This index maps the material claims in the submission to a receipt. Commit links
point to the public repository history; session links point to redacted excerpts
copied from the local Copilot CLI event store. Secrets, encrypted model reasoning,
and unrelated repository listings are omitted.

| Claim | Receipt |
| --- | --- |
| The health-check CLI exists and has focused tests. | [`45a2133`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45a2133) |
| Copilot context includes a before/after tool correction. | [`12bdc72`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/12bdc72), [`6feeb12`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/6feeb12), [redacted review transcript](raw/copilot-review-session-redacted.md) |
| A bounded agent changed multiple files, read a failure, and reran tests. | [`44661b4`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/44661b4), [redacted Q2 transcript](raw/copilot-q2-session-redacted.md) |
| The reviewer agent was restricted to read-only tools. | [`befcf86`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/befcf86) |
| Real approval prompts included an allow and a refusal. | [`45cbe7c`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/45cbe7c), [approval records](copilot-approval-prompts.md) |
| The MCP write first failed, then succeeded after runtime authentication was fixed. | [`050c714`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/050c714), [`555ce03`](https://github.com/RamithaMN/Github_Copilot_assignment/commit/555ce03), [redacted MCP transcript](raw/copilot-mcp-session-redacted.md), [PR #4](https://github.com/RamithaMN/Github_Copilot_assignment/pull/4) |
| The current suite passes. | [latest verification receipt](latest-verification.md) |
| The final branch is not the same as `main`. | `main` is at `b7f3e24`; the submission branch contains `555ce03` plus the evidence commits on `q2-agent-cli-threshold`. No squash was performed. |

The last row is intentionally explicit: submit the branch or merge it into `main`
without squashing. The repository's approval policy does not permit an automatic
merge without an explicit user decision.
