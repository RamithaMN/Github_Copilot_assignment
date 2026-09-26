# Health Check Evidence

Command:

```bash
.venv/bin/python -m src.main \
  --path ../Family-office-IC-agent \
  --repo rohitsundaram/Family-office-IC-agent
```

Observed result on 2026-09-26:

```text
[PASS   ] README: README.md found
[PASS   ] .gitignore: .gitignore found
[PASS   ] Tests: test directory or test files found
[PASS   ] Dependencies: dependency configuration found: package.json
[WARNING] CI: no GitHub Actions workflow found
[PASS   ] Documentation: documentation found
[PASS   ] Open issues: 0 open issue(s)
[PASS   ] Stale pull requests: no open pull requests inactive for more than 30 days
```

The first sandboxed run could not resolve GitHub DNS. The same command succeeded
with network access after the adapter was updated to use the dependency-managed
`certifi` CA bundle.

