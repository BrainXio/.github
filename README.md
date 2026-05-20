# BrainXio Organization Defaults

Shared workflows, composite actions, issue templates, and lint configs for all BrainXio repositories.

## Provided Assets

| Directory              | Purpose                                      | Consumers                  |
|------------------------|----------------------------------------------|----------------------------|
| .github/workflows/     | Reusable CI/CD workflows                     | All repositories           |
| .github/actions/       | Composite setup actions                      | Reusable workflows         |
| defaults/              | Org-wide lint configs (copied via sync)     | All repositories           |
| ISSUE_TEMPLATE/        | GitHub issue & PR templates                  | All repositories           |
| profile/               | GitHub organization profile                  | Org page                   |

## Standards Enforcement

All rules are enforced via CI (starter-checks + self-ci), branch protection, and Claude Code hooks. See [CONTRIBUTING.md](CONTRIBUTING.md) for commit style, PR requirements, and local setup.