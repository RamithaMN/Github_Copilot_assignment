# Setup Failure Receipts

Only failures with literal output are treated as receipts. Other historical setup
notes are not used as scored evidence.

## Git index permission failure

Observed while staging the current repository in the managed workspace:

```text
$ git add ...
fatal: Unable to create '/Users/rohitsundaram/PycharmProjects/Github_copilot_assignment/.git/index.lock': Operation not permitted
```

The same staging operation succeeded after the environment granted the required
filesystem permission. This is a workspace permission receipt, not a Copilot approval
transcript.

The earlier notes about Python 3.12 and pytest availability varied by environment but
their literal terminal output was not preserved in the repository. They are therefore
not presented as independent evidence; the preserved test receipts are the focused
and full-suite outputs in the Q2 transcript and `latest-verification.md`.
