# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] — 2026-05-20

### Fixed

- Changed all consumer workflow action references from relative (`./.github/actions/...`) to absolute (`brainxio/.github/actions/...@v1.0.0`). Relative paths resolve in the caller's repository, breaking downstream consumers. This was a critical regression in v1.0.0.
- `publish-pypa.yml`:
  - Changed `enable-cache` from `false` to `true`
  - Added `PYPI_API_TOKEN` secret input with fallback to `GITHUB_TOKEN`
  - Added clear token contract documentation (GitHub Packages vs PyPI.org)

### Added

- Consumer warning headers to all 11 reusable workflow files in `workflows/`
- `self-ci.yml` enforcement steps:
  - Fail on deprecated `actions/cache@v[0-3]` usage
  - Fail on relative action paths (`./.github/actions/`) in consumer workflows

## [1.0.2] — 2026-05-20

### Fixed

- Moved cache version and absolute action path enforcement from consumer `workflows/self-ci.yml` to `.github/workflows/self-ci.yml` (the one that actually runs on this repository).

### Added

- `restore-keys` fallback to `actions/setup-rust-deps/action.yml` (`Swatinem/rust-cache@v2`).
- `cache-dependency-path` to `actions/setup-node-deps/action.yml` for monorepo lockfile detection.
- Cache restore-key comments to `actions/setup-python-deps/action.yml` and `actions/setup-go-deps/action.yml` (built-in cache handles this automatically).
- `.github/workflows/cache-hygiene.yml` — weekly cron job that alerts on cache maintenance (GitHub 10 GB limit).

## [1.0.0] — 2026-05-20

### Added

- Consolidated all reusable workflows from `brainxio/workflows` into `workflows/`:
  - `ci-python.yml` — lint, typecheck, test, build for Python projects
  - `ci-go.yml` — lint, vet, test, build for Go projects
  - `ci-rust.yml` — fmt, clippy, test, build for Rust projects
  - `ci-typescript.yml` — lint, typecheck, test, build for TypeScript projects
  - `publish-pypa.yml` — PyPI publishing with attestations
  - `publish-npm.yml` — npm publishing
  - `publish-cargo.yml` — crates.io publishing
  - `starter-checks.yml` — commit message validation, security scan basics
  - `dependabot-auto-merge.yml` — automated dependency management
  - `doc-quality.yml` — documentation linting
  - `sync-defaults.yml` — propagate org defaults to consumer repos
  - `self-ci.yml` — synthetic CI tests for all language workflows
- Consolidated all composite actions from `brainxio/workflows` into `actions/`:
  - `setup-python-deps`
  - `setup-node-deps`
  - `setup-go-deps`
  - `setup-rust-deps`
- `.githooks/pre-commit` with anti-AI manifesto pattern detection, email domain validation (`@brainxio.org` only), and phantom repo link detection

### Changed

- Rewrote root `README.md` to be a public landing page with clear usage instructions
- Rewrote `CONTRIBUTING.md` to remove private repo references and `.claude/` submodule instructions
- Rewrote `defaults/README.md` to explicitly discourage symlinking in production
- Updated `profile/README.md` and `profile/PROFILE.md` to remove private repo links
- Updated `ISSUE_TEMPLATE/bug_report.md` example workflow paths
- Updated `.gitignore` to remove private directory entries

### Removed

- `docs/` directory (threat model moved to `brainxio/docs`)
- `instructions/` directory (private agent configuration)
- `.claude/` directory (private runtime configuration)
- Root-level lint config symlinks (`.hadolint.yaml`, `.mdformat.toml`, `.prettierrc`, `.yamllint`)
- All references to `.agents`, `.ollama`, `.claude` private repositories
- Old CHANGELOG entries referencing deleted files and nested `.github/.github/` structure
