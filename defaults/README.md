# BrainXio Shared Defaults

This directory contains the canonical source of truth for organization-wide configuration files.

These files are copied into each disorder-family repository (`ocd`, future `adhd`, etc.) with minimal local overrides only when necessary.

## Files

| File | Purpose | Enforcement |
| ---- | ------- | ----------- |
| `.yamllint` | YAML linting rules | Required |
| `.hadolint.yaml` | Dockerfile linting rules | Required |
| `.mdformat.toml` | Markdown formatting | Required |
| `.prettierrc` | JavaScript/TypeScript/etc. formatting | Opt-in |
| `.typos.toml` | Spell-checking ignore list | Required |

**`.prettierrc`** is opt-in. Consumer repos should symlink or copy it if they use Prettier, but it is not enforced. Other files are required and applied automatically by CI.

## Governance

- **Edit here first** for any generic change.
- Local copies in individual repos may exist with a short header pointing back to this location.
- Never recreate or significantly modify these files locally without checking the source of truth.

These files are copied into consumer repositories. Do not symlink in production.
