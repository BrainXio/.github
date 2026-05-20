# BrainXio Framework & Setup

Org-level defaults and agent entry points.

## Environment Structure

All projects live under a main workspace (`~/brainxio/` or `/opt/brainxio/`).

Each repository follows the standard layout defined in the BrainXio standards.

## Core Expectations

- Local models and guardrails run where hardware allows
- Cloud sessions respect subscription tiers and never exceed them without explicit Core approval
- Local-first by default; clear separation between development and runtime containers
- `gh` CLI is the only allowed management interface for GitHub organisation resources
- SSH keypairs and GPG keys for commits are managed exclusively through the `tools/` directory

## Related Repositories

| Repository | Purpose |
| ---------- | ------- |
| [brainxio/docs](https://github.com/brainxio/docs) | Diátaxis documentation framework (protocols, roles, rules, skills) |
| [brainxio/tools](https://github.com/brainxio/tools) | Agent capability tools (bootstrap, tier detection, safe operations) |
