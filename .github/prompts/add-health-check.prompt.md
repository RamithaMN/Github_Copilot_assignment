# Add a Health Check

Add one repository health check without changing the public status vocabulary.

Requirements:

1. Inspect the existing models and checker patterns first.
2. Keep the check independent and side-effect-free.
3. Add focused tests for pass, missing/negative, and relevant boundary behavior.
4. Update the README only if the user-facing behavior changed.
5. Run the focused test and then the full `pytest` suite.
6. Report files changed, commands run, and any uncertainty.

