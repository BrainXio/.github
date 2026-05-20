# Consumer Workflow Reference

These files are the only workflows intended to be called by external repositories via `uses:`.

> **Scope:** `workflows/*.yml` in this directory are the public, versioned contract.  
> The nested `.github/workflows/` directory inside this repository contains internal automation not meant for consumers.

## Table of Consumer-Safe Workflows

| Name | Purpose | Language / Ecosystem | Example usage |
|---|---|---|---|
| [ci-python.yml](ci-python.yml) | Run lint, typecheck, test, and coverage for Python projects. | Python | `uses: brainxio/.github/workflows/ci-python.yml@v1` |
| [ci-go.yml](ci-go.yml) | Run format check, build, vet, and test for Go projects. | Go | `uses: brainxio/.github/workflows/ci-go.yml@v1` |
| [ci-rust.yml](ci-rust.yml) | Run format check, clippy, test, and optional audit for Rust projects. | Rust | `uses: brainxio/.github/workflows/ci-rust.yml@v1` |
| [ci-typescript.yml](ci-typescript.yml) | Run install, lint, format check, typecheck, and test for TypeScript projects. | TypeScript / Node.js | `uses: brainxio/.github/workflows/ci-typescript.yml@v1` |
| [publish-pypa.yml](publish-pypa.yml) | Build and publish a Python package to PyPI or GitHub Packages. | Python | `uses: brainxio/.github/workflows/publish-pypa.yml@v1` |
| [publish-npm.yml](publish-npm.yml) | Build and publish an npm package to GitHub Packages or npm registry. | Node.js / npm | `uses: brainxio/.github/workflows/publish-npm.yml@v1` |
| [publish-cargo.yml](publish-cargo.yml) | Build and publish a Rust crate to crates.io or a private registry. | Rust / Cargo | `uses: brainxio/.github/workflows/publish-cargo.yml@v1` |
| [starter-checks.yml](starter-checks.yml) | Run secret-scan, license-check, and conventional-commit validation. | Any | `uses: brainxio/.github/workflows/starter-checks.yml@v1` |
| [dependabot-auto-merge.yml](dependabot-auto-merge.yml) | Auto-merge low-risk Dependabot PRs with branch protection compliance. | GitHub Actions | `uses: brainxio/.github/workflows/dependabot-auto-merge.yml@v1` |
| [doc-quality.yml](doc-quality.yml) | Run markdown formatting, YAML linting, typo checks, and link validation. | Documentation | `uses: brainxio/.github/workflows/doc-quality.yml@v1` |
| [sync-defaults.yml](sync-defaults.yml) | Synchronize repository defaults (labels, files, settings) across repos. | GitHub Management | `uses: brainxio/.github/workflows/sync-defaults.yml@v1` |

## Internal Workflows

The `.github/workflows/` directory nested inside this repository contains internal automation (e.g., CI for this repo itself, release orchestration, and housekeeping). These files are **not** part of the public consumer contract and may change without notice.

## Security Note

Always pin consumer workflows to a **stable release tag** such as `@v1`. Never reference `@main` or a branch name in production repositories. Floating tags are periodically moved to new patch releases; if you require immutability, pin to the full semantic version (e.g., `@v1.2.3`).
