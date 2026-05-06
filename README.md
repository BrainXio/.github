# BrainXio Shared Defaults

This directory contains the canonical source of truth for organization-wide configuration files.

These files are copied into each disorder-family repository (`ocd`, future `adhd`, etc.) with minimal local overrides only when necessary.

## Files

- `.yamllint` – YAML linting rules
- `.hadolint.yaml` – Dockerfile linting rules
- `.mdformat.toml` – Markdown formatting (load-bearing)
- `.prettierrc` – JavaScript/TypeScript/etc. formatting (advisory only)

## Governance

- **Edit here first** for any generic change.
- Local copies in individual repos may exist with a short header pointing back to this location.
- Never recreate or significantly modify these files locally without checking the source of truth.

See `docs/explanation/org-defaults.md` in any project repository for full usage rules.
