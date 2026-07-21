# CI workflow

Workflow file: [`.github/workflows/ci.yml`](../../../.github/workflows/ci.yml)

## Jobs

| Job | Purpose |
|-----|---------|
| `CI` | Install deps, run `verify_setup.py`, pytest smoke tests |
| `secret-scan` | Grep for high-signal secret patterns |

## Triggers

- Push and pull request to `main`
- Manual `workflow_dispatch`

## Local parity

```bash
make test
```

Uses the same verification and pytest suite as CI.
