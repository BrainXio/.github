# Tools Directory — Agent Capability & Workflow Utilities

This directory contains executable tools that agents use to operate safely within their declared capability tier.

**How to run any tool (recommended):**

```bash
uv run --directory .github/tools python detect_capability_tier.py
uv run --directory .github/tools python smart_document_reader.py docs/reference/cpr-procedure.md A 32000
```

All tools are designed to be called by agents of any tier. Lower-tier agents receive graceful degradation (summaries, truncated output, clear escalation messages).

## Available Tools

| Tool                        | Purpose                                           | Min Worker Tier | Min Trainer Tier |
|-----------------------------|---------------------------------------------------|-----------------|------------------|
| `detect_capability_tier.py` | Detect current hardware + tier                    | C               | 3                |
| `smart_document_reader.py`  | Context-window-safe document loading              | C               | 3                |
| `gh_safe_wrapper.py`        | Role-aware `gh` CLI wrapper                       | C               | 3                |
| `threshold_enforcer.py`     | Check if task is allowed for current tier         | C               | 3                |
| `bootstrap_environment.py`  | One-command environment setup                     | C               | 3                |

## Capability Gates

Every tool begins with (or respects) a capability gate. Agents running on **Tier C / Free** receive safe, limited output and are encouraged to escalate when complexity exceeds their tier.

## Adding New Tools

1. Create `new_tool.py` with a clear docstring and `if __name__ == "__main__":` block.
2. Add a short how-to or reference page in `docs/tools/`.
3. Update this index.
4. Commit via the snapshot system.
