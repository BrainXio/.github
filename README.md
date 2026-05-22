# BrainXio Organization Defaults

Organization templates, issue templates, lint defaults, and self-CI for the BrainXio organization.

## What This Repo Provides

| Directory | Purpose | Used By |
|---|---|---|
| `.github/workflows/` | Internal automation (self-CI, cache-hygiene, branch-protection) | This repo only |
| `.githooks/` | Shared git hooks (pre-commit standards guard) | All BrainXio repositories |
| `defaults/` | Org-wide lint configs (.yamllint, .hadolint.yaml, .typos.toml, etc.) | All repositories |
| `ISSUE_TEMPLATE/` | GitHub issue and PR templates | All repositories |
| `profile/` | GitHub organization profile page | github.com/brainxio |

## Related Repositories

| Repository | Purpose | Consumer Syntax |
|---|---|---|
| `brainxio/actions` | Composite setup actions for toolchain installation | `uses: brainxio/actions/...` |
| `brainxio/cicd` | Reusable CI workflows (Python, Go, Rust, TypeScript, publishing, security) | `uses: brainxio/cicd/.github/workflows/...` |
| `brainxio/claude-cli` | Claude Code CLI extensions: hooks, quality gates, and utility commands | `uvx --from git+https://github.com/BrainXio/claude-cli <command>` |
| `brainxio/claude-config` | Framework configuration for Claude Code: rules, agents, skills, and settings | Copy/symlink into `.claude/` |

## Using Defaults

Copy files from `defaults/` into your repository root. Do not symlink in production — symlinks break on fork, offline work, and raw URL access.

## Self-Only Workflows

The following workflows in `.github/workflows/` are internal to this repo only:

- `enforce-branch-protection.yml` — protects `main` on this repo
- `cache-hygiene.yml` — monitors cache usage on this repo
- `self-ci.yml` — validates this repo's own automation

## Security Hardening

All automation in this organization follows these principles:

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
