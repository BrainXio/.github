# How to Use the GitHub CLI Safely

The `gh_safe_wrapper.py` tool enforces C.P.R. role boundaries when interacting with GitHub.

## Basic Usage

```bash
uv run --directory .github/tools python gh_safe_wrapper.py Resonant "repo view brainxio/.github"
uv run --directory .github/tools python gh_safe_wrapper.py Personal "pr create --title 'Fix docs' --body '...'"
```

## Role Permissions

- **Resonant**: Read-only operations (view, list)
- **Personal**: Can create PRs and issues
- **Core**: Full access (including approvals and repo settings)

The wrapper prevents lower roles from performing actions outside their authority.
