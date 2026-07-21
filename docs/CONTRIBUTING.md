# Contributing

1. Fork the repository and create a feature branch (`feat/` or `fix/`).
2. Install dependencies: `make install`
3. Run tests: `make test` and `make agent:check`
4. Commit with conventional messages:

```text
<type>(<scope>): <description>
```

5. Open a pull request against `main`.

## Pull request checklist

- [ ] `make test` passes locally
- [ ] `make agent:check` passes locally
- [ ] README/docs updated if behavior or setup changed
