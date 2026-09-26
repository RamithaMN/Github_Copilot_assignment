"""Terminal report rendering."""

from collections.abc import Iterable

from .models import CheckResult


def render_report(repository: str, results: Iterable[CheckResult]) -> str:
    lines = [f"GitHub Repository Health: {repository}", "=" * 40]
    for result in results:
        lines.append(f"[{result.status.value:<7}] {result.check}: {result.message}")
    return "\n".join(lines)

