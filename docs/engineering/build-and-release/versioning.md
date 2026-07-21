# Versioning and release

This repo follows [Semantic Versioning](https://semver.org/).

## Current version

**1.0.0** — see README badge and [CHANGELOG.md](../../CHANGELOG.md).

## Bump rules

| Bump | When |
|------|------|
| PATCH | Bug fixes, docs-only |
| MINOR | Backward-compatible features |
| MAJOR | Breaking API or experiment output schema changes |

## Release checklist

1. Update `docs/CHANGELOG.md` and root `CHANGELOG.md`
2. Bump version in README badge
3. `git tag -a vX.Y.Z -m "vX.Y.Z"` and push the tag
4. Open GitHub Release from changelog notes
