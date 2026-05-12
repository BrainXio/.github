---
applyTo: [**]
description: All agents must use canonical documentation in ~/.brainxio/docs/
---
# BrainXio Docs Rule

All agents MUST abide by the documents in `~/.brainxio/docs/`. These documents
are the canonical source of truth for standards, conventions, procedures, and
architectural decisions.

## MCP Server

The preferred access method is the `brainxio-agent-docs` MCP server, configured
in `.mcp.json`:

```json
{
  "mcpServers": {
    "brainxio-agent-docs": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/BrainXio/.agents.git",
        "brainxio-agent-docs",
        "mcp"
      ]
    }
  }
}
```

## Available Tools

| Tool             | Description                                                     |
| ---------------- | --------------------------------------------------------------- |
| `get_document`   | Retrieve any document by relative path from `~/.brainxio/docs/` |
| `list_documents` | List all available documents with titles and tags               |

Setup operations (bootstrap and rule injection) run automatically when the
MCP server starts.

## Fallback

If the MCP server is unavailable, agents may read documents directly from
`~/.brainxio/docs/`. Documents are plain markdown files with YAML frontmatter,
organized by category:

- `master-plans/` — strategic plans and architectural decisions
- `error-handling/` — error patterns, symptoms, root causes, fixes
- `industry-standards/` — external standards and specifications
- `best-practices/` — internal conventions, rationale, and patterns
- `rules-and-regulations/` — public rules and compliance requirements

## When to Use

- **Before starting any task** — check `~/.brainxio/docs/` for relevant standards or master plans
- **When encountering an error** — search error-handling/ for known patterns and mitigations
- **When making architectural decisions** — consult master-plans/ for existing decisions and rationale
- **When unsure about conventions** — best-practices/ documents project-specific conventions
