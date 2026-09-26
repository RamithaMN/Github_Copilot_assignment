"""Typed data models shared by checks, services, and report rendering."""

from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    """The only statuses a health check may emit."""

    PASS = "PASS"
    WARNING = "WARNING"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class CheckResult:
    """A normalized, human-readable result for one health check."""

    check: str
    status: Status
    message: str


@dataclass(frozen=True)
class PullRequestSummary:
    """The minimum pull-request data needed for stale detection."""

    number: int
    title: str
    updated_at: str

