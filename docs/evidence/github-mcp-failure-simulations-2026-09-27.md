# MCP Failure Simulation Receipt

The repository now has a deterministic bounded-transport harness at
`scripts/mcp_failure_simulation.py`. It invokes the same decision boundary for
three provider-like failures without contacting GitHub or attempting a write.
The injected transport fixtures are deliberate: the sandbox does not permit a
local TCP listener, so an HTTP server fixture would not be portable to CI.

Command:

```bash
python3.12 scripts/mcp_failure_simulation.py
```

Observed output:

```json
[
  {
    "scenario": "slow",
    "status": "UNKNOWN",
    "decision": "timeout; stop and report, no write",
    "write_attempted": false
  },
  {
    "scenario": "outage",
    "status": "UNKNOWN",
    "decision": "unavailable; stop and report (_UnavailableError)",
    "write_attempted": false
  },
  {
    "scenario": "malformed",
    "status": "UNKNOWN",
    "decision": "malformed or incomplete response; no action",
    "write_attempted": false
  }
]
```

The command was run on 2026-09-27. `tests/test_mcp_failure_simulation.py`
asserts all three outcomes and the no-write invariant. The harness is evidence
for the policy boundary, not a claim that Copilot CLI's private MCP transport
was replaced or directly configured with these timeout values.
