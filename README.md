# BrainXio Organization Defaults

Reusable GitHub Actions workflows, composite actions, issue templates, and lint defaults for the BrainXio organization.

## What This Repo Provides

| Directory | Purpose | Used By |
|---|---|---|
| `workflows/` | Reusable CI/CD workflows (Python, Go, Rust, TypeScript, publishing, security) | All BrainXio repositories |
| `actions/` | Composite setup actions for toolchain installation | Reusable workflows |
| `defaults/` | Org-wide lint configs (.yamllint, .hadolint.yaml, .typos.toml, etc.) | All repositories |
| `ISSUE_TEMPLATE/` | GitHub issue and PR templates | All repositories |
| `profile/` | GitHub organization profile page | github.com/brainxio |

## Using Reusable Workflows

Consumer repositories call workflows via `uses:` with a version tag:

```yaml
jobs:
  test:
    uses: BrainXio/.github/workflows/ci-python.yml@v1
    with:
      python-version: "3.12"
```

Pin to a tag (e.g., `@v1`) — never `main`.

## Using Defaults

Copy files from `defaults/` into your repository root. Do not symlink in production — symlinks break on fork, offline work, and raw URL access.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit style, PR requirements, and local setup.

## Security

See [SECURITY.md](SECURITY.md) for vulnerability reporting.
