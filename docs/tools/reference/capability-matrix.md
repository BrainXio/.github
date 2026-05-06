# Capability Matrix — Tools vs Agent Tiers

This matrix shows which tools each agent tier can safely use.

## Worker Tier Matrix

| Tool                        | Tier C (Free)      | Tier B (Pro)       | Tier A (Max)       |
|-----------------------------|--------------------|--------------------|--------------------|
| detect_capability_tier      | Full               | Full               | Full               |
| smart_document_reader       | Truncated (8k)     | Partial (32k)      | Full (128k+)       |
| gh_safe_wrapper             | Read-only          | Read + limited write | Full               |
| threshold_enforcer          | Full               | Full               | Full               |
| bootstrap_environment       | Full               | Full               | Full               |

## Trainer Tier Matrix

| Tool                        | Tier 3 (No training) | Tier 2 (Assisted) | Tier 1 (Full)     |
|-----------------------------|----------------------|-------------------|-------------------|
| trainer-related tasks       | Blocked              | Allowed           | Allowed           |
| fine_tune / QLoRA           | Blocked              | Blocked           | Allowed           |

**Rule**: Always run `detect_capability_tier.py` before accepting work that may exceed your tier.
