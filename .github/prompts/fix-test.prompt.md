# Fix a Failing Test

Investigate the failing test before editing production code.

Requirements:

1. Reproduce the failure with the narrowest pytest command.
2. Determine whether the defect is in the test, implementation, or environment.
3. Preserve the intended contract and add a regression assertion when appropriate.
4. Do not weaken an assertion merely to make the suite pass.
5. Run the focused test, then the complete suite.
6. Summarize the original failure and the verified fix.

