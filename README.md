# BrainXio .github

<p align="center">
  <a href="https://github.com/brainxio">
    <img src="https://github.com/brainxio.png" alt="BrainXio Logo" width="80" height="80">
  </a>

  <h3 align="center">BrainXio Shared Defaults</h3>

  <p align="center" style="font-size: 1.1em; font-style: italic; max-width: 800px; margin: 1.5em auto;">
    Curiosity. Freedom. Creation.
  </p>
</p>

## Purpose

This repository is the **single source of truth** for organization-wide defaults and coordination patterns across BrainXio.

It provides minimal, high-quality, self-policing configurations that all current and future disorder-family repositories (starting with `ocd`) can inherit. The goal is maximum consistency with minimum surface area — sub-repositories keep only the overrides they truly need.

## Inherited Defaults

The following files live here and are automatically available to every BrainXio repository (unless locally overridden):

- **CODE_OF_CONDUCT.md** — Organization-wide contributor standards
- **CONTRIBUTING.md** — Guidelines for contributing to any BrainXio project
- **SECURITY.md** — Responsible vulnerability disclosure policy
- **dependabot.yml** + **dependabot-auto-merge.yml** — Dependency update configuration
- **bug_report.md**, **feature_request.md**, **pull_request_template.md** — Issue and PR templates

Additional shared configurations (security tooling, linting, workflows, etc.) are being consolidated here as part of the current cleanup.

## Philosophy

- **Minimal Surface Area** — Only what is needed for consistency.
- **Structural Honesty** — Defaults reflect reality, not aspirational scope.
- **Consistent Defaults** — One place to update patterns across the entire org.
- **Single Source of Truth** — Production behavior draws from here; local copies stay minimal.

Sub-repositories are encouraged to reference these files directly rather than duplicating them.

---

<p align="center">
  <a href="https://github.com/brainxio"><strong>Visit BrainXio →</strong></a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/issues/new?template=bug_report.md">Report Bug</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/issues/new?template=feature_request.md&labels=enhancement">Request Feature</a>
</p>
