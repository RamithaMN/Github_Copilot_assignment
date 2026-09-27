"""Exercise the bounded MCP failure policy against injected transport fixtures.

This is a receipt-producing harness, not the product's GitHub client. It keeps
the failure cases deterministic and never makes a GitHub write. The injected
transport avoids binding a local TCP listener, which is unavailable in some
sandboxed CI environments.
"""

from __future__ import annotations

import json
import socket
import time
from typing import Any


class _UnavailableError(OSError):
    """A deterministic stand-in for a refused MCP connection."""


def _bounded_read(transport: Any, *, timeout: float = 0.05) -> tuple[str, str]:
    try:
        payload = transport(timeout=timeout)
    except (TimeoutError, socket.timeout):
        return "UNKNOWN", "timeout; stop and report, no write"
    except (OSError, json.JSONDecodeError) as exc:
        return "UNKNOWN", f"unavailable; stop and report ({type(exc).__name__})"

    items = payload.get("pull_requests") if isinstance(payload, dict) else None
    if not isinstance(items, list) or any(
        not isinstance(item, dict) or not item.get("number") or not item.get("updated_at")
        for item in items
    ):
        return "UNKNOWN", "malformed or incomplete response; no action"
    return "PASS", "valid response; action remains separately approval-gated"


def run_scenarios() -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for scenario in ("slow", "outage", "malformed"):
        def transport(*, timeout: float) -> dict[str, Any]:
            if scenario == "slow":
                time.sleep(timeout * 4)
                raise socket.timeout("fixture exceeded bounded timeout")
            if scenario == "outage":
                raise _UnavailableError("fixture connection refused")
            return {"pull_requests": [{"number": 7}]}

        status, decision = _bounded_read(transport)
        results.append(
            {
                "scenario": scenario,
                "status": status,
                "decision": decision,
                "write_attempted": False,
            }
        )
    return results


if __name__ == "__main__":
    print(json.dumps(run_scenarios(), indent=2))
