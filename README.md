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

**Always pin to `@v1`** — this floating tag points to the latest v1.x release and is updated after every patch release. Never use `@main` in production.

## Using Defaults

Copy files from `defaults/` into your repository root. Do not symlink in production — symlinks break on fork, offline work, and raw URL access.

## Self-Only Workflows

The following workflows are internal to `brainxio/.github` and are **not** published for consumer use:

- `enforce-branch-protection.yml` — protects `main` on this repo only
- `cache-hygiene.yml` — monitors cache usage on this repo only

## Cache Best Practices

All composite actions use explicit `restore-keys` fallbacks. See [actions/cache-best-practices.md](actions/cache-best-practices.md) for the pattern.

## Security Hardening for Reusable Workflows

All workflows in this repository follow these principles:

- **Minimal permissions**: `permissions: contents: read` by default; elevated permissions granted only per-job.
- **No `pull_request_target`**: Workflows do not use `pull_request_target` to avoid untrusted code execution.
- **Pinned action versions**: Every external action is pinned to a full-length commit SHA.
- **`persist-credentials: false`** on all `actions/checkout` steps.
- **Input validation**: Regex validation on all string inputs that reach shell commands.
- **No secrets in inputs**: Workflows never echo or log secret values.
- **Trusted publishing**: Where supported, workflows prefer OIDC over long-lived tokens.

See [SECURITY.md](SECURITY.md) for vulnerability reporting.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for commit style, PR requirements, and local setup.

## Maintenance

This repo is maintained by `@brainxio/core`. PRs from org members are welcome — the stricter standards exist precisely because this repo affects every other repository in the organization.
