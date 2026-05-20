# Contributing to BrainXio Projects

## Development Setup

### Prerequisites

| Tool | Version | Purpose |
| --- | --- | --- |
| `git` | any recent | Version control |
| Node.js | 20+ | TypeScript tooling, GitHub Actions |
| Python | 3.10+ | Scripts, CI utilities |
| `uv` | latest | Python package manager |
| Go | 1.22+ | CLI tooling |
| Rust | 1.87+ | Low-level tooling |

### Clone

```bash
git clone --recurse-submodules https://github.com/BrainXio/workspace.git
cd workspace
```

If you already cloned without submodules:

```bash
git submodule update --init --recursive
```

### Local Commands

```bash
# Lint (in .claude/ submodule)
cd .claude && uv run ruff check . && cd ..

# Type check (in .claude/ submodule)
cd .claude && uv run mypy src/ && cd ..

# Run bootstrap
uvx --from git+https://github.com/brainxio/.claude.git claude-bootstrap

# Sign commits non-interactively
bin/gpg-sign
```

---

## Making Changes

### Branch Naming

```
feat/description     # New feature
fix/description      # Bug fix
docs/description     # Documentation only
refactor/description # Code restructure, no behavior change
```

### Conventional Commits

Format: `<type>: <description>`

```
feat: add Prometheus exporter to economy-service
fix: handle nil pointer in config loader
docs: update CI pipeline reference
chore: bump ruff to 0.9.0
```

Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `test`, `perf`

### Pre-commit Hooks

The workspace includes hooks that run automatically on `git commit`:

- **.githooks/pre-commit**: blocks AI attribution patterns, checks submodule/workspace alignment, runs `.claude/` pre-commit via `uvx`
- **.githooks/commit-msg**: blocks AI attribution in commit messages

If hooks fail, fix the reported issue and re-commit. Do not use `--no-verify`.

---

## Testing

### Validate Workflow Syntax

`.github/defaults/self-ci.yml` validates the syntax of all CI workflow files. Run it locally:

```yaml
# .github/workflows/my-workflow.yml
name: My Workflow
on: push

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Validate workflows
        uses: ./.github/.defaults/self-ci.yml
```

### Test Composite Actions

Each composite action can be called via `uses:` from any consumer repo. See the action's `action.yml` for required inputs.

Example — call `ci-python.yml` from a consumer repo:

```yaml
jobs:
  test:
    uses: BrainXio/.github/.github/workflows/ci-python.yml@v1
    with:
      python-version: "3.12"
     uv-lock: true
```

---

## Pull Request Checklist

Before merging:

- [ ] Branch name follows `feat/`, `fix/`, `docs/` convention
- [ ] Commit message uses Conventional Commits format
- [ ] `starter-checks` job passes (lint, type check, security scan)
- [ ] Relevant docs updated if behavior changed
- [ ] No secrets or credentials in diff
- [ ] PR description explains *why*, not just *what*

All PRs are squash-merged into `main`.

---

## Reusable Workflows

Consumer repos call workflows via `uses:` with a version tag. Pin to a tag (e.g., `@v1`) — never `main`.

### ci-python.yml

```yaml
jobs:
  test:
    uses: BrainXio/.github/.github/workflows/ci-python.yml@v1
    with:
      python-version: "3.12"
      uv-lock: true
```

### ci-typescript.yml

```yaml
jobs:
  test:
    uses: BrainXio/.github/.github/workflows/ci-typescript.yml@v1
    with:
      node-version: "20"
```

### ci-go.yml

```yaml
jobs:
  test:
    uses: BrainXio/.github/.github/workflows/ci-go.yml@v1
    with:
      go-version: "1.22"
```

### pr-stale.yml

```yaml
jobs:
  housekeeping:
    uses: BrainXio/.github/.github/workflows/pr-stale.yml@v1
    with:
      days-before-stale: 30
      days-before-close: 7
```

---

## Signed Commits

GPG signing is required for all commits. Setup instructions:

```
docs/ci-gpg-signing.md
```

Non-interactive signing is available via `bin/gpg-sign` in the workspace root.