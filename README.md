# BrainXio Framework & Setup

This is the central home for how we actually run BrainXio.

It describes the expected environment layout, our documentation framework, working attitudes, and the practical foundations that keep everything coherent across human, agents, local hardware, and cloud resources.

---

<p align="center">
  <a href="https://github.com/brainxio/docs">Documentation</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/tools">Tools</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/issues/new?template=bug_report.md">Report Bug</a>
  &nbsp;·&nbsp;
  <a href="https://github.com/brainxio/.github/issues/new?template=feature_request.md&labels=enhancement">Request Feature</a>
</p>

---

## How We Expect the Environment to Be Set Up

We keep things intentionally simple, sovereign, and observable. Every development or runtime environment must follow the exact same baseline structure so agents and humans can move between machines without friction or confusion.

Core expectations:

- All projects live under a main workspace (usually `~/brainxio/` or `/opt/brainxio/`)
- Each repository follows the standard layout defined in our standards
- Local models and guardrails run where hardware allows
- Cloud sessions respect subscription tiers and never exceed them without explicit Core approval
- Everything stays local-first by default, with clear separation between development containers and runtime containers
- The `gh` CLI is the only allowed management interface for GitHub organisation resources
- SSH keypairs and GPG keys for commits are managed exclusively through the `tools/` directory — agents never see or handle sensitive key material

Our operating model adapts to the resources available — from lightweight hardware through cloud-assisted to full local autonomy — so everyone always knows the current operating boundaries. Fun is never optional — even clean professional work must stay **fun**ctional.

## Related Repositories

| Repository | Purpose |
| ---------- | ------- |
| [brainxio/docs](https://github.com/brainxio/docs) | Diátaxis documentation framework (protocols, roles, rules, skills) |
| [brainxio/tools](https://github.com/brainxio/tools) | Agent capability tools (bootstrap, tier detection, safe operations) |

This repository contains org-level defaults and agent entry points only.

---

We move at our own pace, with clarity, care, and a lot of quiet joy.

Welcome to the inside of BrainXio.
