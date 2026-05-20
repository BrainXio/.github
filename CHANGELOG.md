# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.5] — 2026-05-20

### Changed

- Migrated all `runs-on: ubuntu-22.04` to `ubuntu-24.04` across every workflow.

## [1.0.4] — 2026-05-20

### Fixed

- Deleted zombie consumer copies: `workflows/self-ci.yml` and `workflows/enforce-branch-protection.yml`.
- Corrected `cp` paths in `.github/workflows/self-ci.yml` consumer-simulation job.

### Changed

- Updated all consumer workflow headers to reference `@v1` floating tag.
- Replaced single giant v1.0.3 commit with seven atomic commits.

### Added

- `restore-keys` fallbacks to `setup-go`, `setup-node`, and `setup-python` composite actions.
- `actions/cache-best-practices.md` documenting the cache pattern.
- `actions/README.md` linking to cache best practices.

## [1.0.3] — 2026-05-20

### Fixed

- Removed zombie `workflows/self-ci.yml` that consumers should never call.
- Added explicit `restore-keys` fallbacks to all four setup composite actions.
- Rewrote CHANGELOG to follow Keep a Changelog discipline.

### Added

- `actions/cache-best-practices.md` documenting the restore-keys pattern.
- Security hardening section to README.

## [1.0.2] — 2026-05-20

### Fixed

- Moved enforcement steps to `.github/workflows/self-ci.yml` (the real self-CI).

### Added

- `restore-keys` to `setup-rust-deps`.
- `cache-hygiene.yml` weekly monitor.

## [1.0.1] — 2026-05-20

### Fixed

- Absolute action references in consumer workflows.
- `publish-pypa.yml` caching and token handling.

### Added

- Consumer warning headers to all workflows.

## [1.0.0] — 2026-05-20

### Added

- Initial release: consolidated all reusable workflows and composite actions.
- Pre-commit hooks with security patterns.

### Removed

- Private repo references and documentation.
