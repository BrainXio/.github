# Threat Model: GitHub Actions Infrastructure

## Scope

All reusable workflows and composite actions in this repository, plus their consumption pattern across the BrainXio organization.

## Assumptions

- GitHub Actions runners are ephemeral `ubuntu-22.04` VMs managed by GitHub.
- Repository write access is restricted to organization members with 2FA enforced.
- Branch protection is applied programmatically via `enforce-branch-protection.yml`.

## Threats and Mitigations

### Supply Chain — Compromised Third-Party Actions

**Risk**: A popular action is compromised (account takeover, malicious commit). Consumers auto-update via floating tags.

**Mitigations**:
- All actions are pinned to immutable commit SHAs, not tags.
- SHAs are verified via `git ls-remote --tags <repo>^{}` dereferencing before pinning.
- Dependabot monitors for outdated actions; updates require PR review.
- No `curl | sudo bash` or `wget | sh` installations in any workflow.

### Supply Chain — Cache Poisoning

**Risk**: A poisoned build cache injects malicious artifacts into subsequent builds.

**Mitigations**:
- Cache keys include lockfile hashes where available (`uv.lock`, `package-lock.json`, `Cargo.lock`).
- `Swatinem/rust-cache` and `actions/setup-node` cache paths are scoped to the repository.
- No shared cross-repository caches.

### Template Injection

**Risk**: `${{ inputs.* }}` or `${{ github.* }}` expressions expanded inside `run:` blocks permit shell injection.

**Mitigations**:
- All workflow inputs consumed in `run:` steps are moved to `env:` blocks with shell-declared variables.
- Inputs are validated against allowlist regexes (`^[a-zA-Z0-9_/.-]+$`) before use.
- No `${{ }}` expressions remain inside `run:` scripts except `env:` indirection.

### Secret Exposure

**Risk**: Secrets leaked via logs, workflow artifacts, or compromised runner state.

**Mitigations**:
- `persist-credentials: false` on all `actions/checkout` steps.
- Secrets are never passed as CLI arguments or inline in `run:` blocks; only via `${{ secrets.* }}` in `env:` or action inputs.
- `.gitleaks.toml` scans every commit for accidental secret inclusion.
- Pre-commit hook blocks commits with detected secrets; `--no-verify` does not bypass.

### Runner Compromise

**Risk**: Malicious PR code executes arbitrary commands on a runner with `GITHUB_TOKEN` access.

**Mitigations**:
- Workflows triggered by `pull_request` (untrusted fork code) do not have `contents: write` or access to organization secrets.
- `permissions:` blocks explicitly declare the minimum required scope (`contents: read` for CI, `contents: write` only for deployment workflows).
- `ubuntu-22.04` is pinned explicitly; no `ubuntu-latest` drift.
- No self-hosted runners in the default CI path.

### Branch Protection Bypass

**Risk**: Force-push, deletion, or unreviewed merge to `main` bypasses policy.

**Mitigations**:
- `enforce-branch-protection.yml` codifies settings: required status checks, required reviews, no force-push, no deletion.
- Branch protection is checked idempotently before application.
- `required_conversation_resolution: true` ensures all review threads are resolved.

## Token Scope

| Token | Scope | Where Used |
|-------|-------|------------|
| `GITHUB_TOKEN` (workflow) | `contents: read` (default) | CI checkout, lint, test |
| `GITHUB_TOKEN` (workflow) | `contents: write` | Branch protection enforcement |
| `secrets.GITHUB_TOKEN` | `security-events: write` | `rustsec/audit-check` only |

No long-lived personal access tokens (PATs) are used in CI.

## Audit and Detection

- `zizmor` static analysis runs in `self-ci.yml` on every push to detect template injection, cache poisoning, and impostor commits.
- `actionlint` validates workflow syntax and expression semantics.
- Quarterly SHA refresh ritual: verify all pinned SHAs still point to expected tags.

## Out of Scope

- Social engineering or phishing against maintainers.
- GitHub platform compromise (handled by GitHub).
- Third-party SaaS integrations outside GitHub Actions.
