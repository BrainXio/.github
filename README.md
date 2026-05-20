# BrainXio Organization Defaults

Shared workflows, issue templates, and configuration files consumed by all BrainXio repositories.

## What This Repository Provides

| Directory | Contents | Consumers |
|-----------|----------|-----------|
| `.github/workflows/` | Reusable workflows (CI, branch protection, release automation) | All BrainXio repos |
| `.github/actions/` | Composite actions (setup-* helpers) | Reusable workflows above |
| `defaults/` | Lint configs (yamllint, hadolint, mdformat, prettier) | Copied to consumer repos via sync-defaults |
| `ISSUE_TEMPLATE/` | GitHub issue templates | All BrainXio repos |
| `profile/` | Public organization profile | GitHub org page |

## Related Repositories

| Repository | Purpose |
| ---------- | ------- |
| [brainxio/.claude](https://github.com/brainxio/.claude) | Runtime: hooks, rules, skills, agents, profiles, settings |
| [brainxio/.agents](https://github.com/brainxio/.agents) | Knowledge base and documentation |
| [brainxio/.ollama](https://github.com/brainxio/.ollama) | Model definitions and modelfiles |
| [brainxio/.containers](https://github.com/brainxio/.containers) | Container stack and orchestration |
| [brainxio/workflows](https://github.com/brainxio/workflows) | Reusable workflow callers |
| [brainxio/tools](https://github.com/brainxio/tools) | Python MCP servers and composite actions |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branch naming, commit style, and CI requirements.
