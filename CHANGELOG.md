# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
- All references to `.agents`, `.ollama`, `.claude` private repositories
- Old CHANGELOG entries referencing deleted files and nested `.github/.github/` structure

## [0.0.1] - 2026-05-09

### Fixed

- Move community files out of nested `.github/.github/` to repo root

### Changed

- Clean up repo, move org defaults to root, add `.typos.toml`
- Remove AGENTS.md (moved to brainxio/docs)
