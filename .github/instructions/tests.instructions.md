---
applyTo: "tests/**/*.py"
---

# Test Instructions

- Use pytest and plain test doubles for GitHub/MCP responses.
- Cover success, boundary, malformed-data, and external-failure behavior.
- Keep tests deterministic: do not call the network or depend on current time.
- Run the focused test first, then the complete suite after a behavior change.

