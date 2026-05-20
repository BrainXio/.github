---
applyTo: [**]
description: All agents must use the KB Engine MCP tools
---
# KB Engine Rule

All agents MUST use the KB Engine MCP tools for knowledge management operations.
The KB Engine is the systematizing memory layer for the BrainXio stack.

## MCP Server

The preferred access method is the `brainxio-knowledge-engine` MCP server, configured
in `.mcp.json`:

```json
{
  "mcpServers": {
    "brainxio-agent-knowledge": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/BrainXio/knowledge-engine.git",
        "brainxio-knowledge-engine"
      ]
    }
  }
}
```

## Available Tools

| Tool                  | Purpose                                   |
| --------------------- | ----------------------------------------- |
| `set_mode`            | Switch active operational mode            |
| `get_mode`            | Return current mode and thresholds        |
| `ingest`              | Raw markdown → processed artifacts        |
| `compile`             | Daily logs → structured articles          |
| `query`               | TF-IDF semantic search (version-filtered) |
| `validate`            | Structural consistency checks (6 checks)  |
| `status`              | KB health report                          |
| `scan_prototypes`     | Scan for projects to ingest next          |
| `get_shortlist`       | Load prototype ingestion shortlist        |
| `get_rules`           | Return structured KB rules and schema     |
| `create_article`      | Create articles with frontmatter scaffolding |
| `stub_broken_links`   | Auto-generate stubs for broken [[wikilinks]] |
| `get_template`        | Return article type template sections     |

## Data Architecture

All KB data lives under `~/.brainxio/data/`:

- `knowledge/` — KB articles organized by type (concepts, mechanisms, outcomes, decisions, references, connections)
- `daily/` — Raw session logs (YYYY-MM-DD.md)
- `ingest_state.json` — Ingestion change tracking
- `compile_state.json` — Compilation state tracking
- `mode_state.json` — Current operational mode
- `index_cache.json` — TF-IDF search index cache
- `shortlist.json` — Prototype scan shortlist

## When to Use

- **Before ingesting new content** — call `get_mode` to check thresholds
- **After writing daily logs** — call `compile` to convert logs to articles
- **When searching for information** — call `query` for semantic search
- **Periodically** — call `validate` to check KB health
- **Before architectural decisions** — call `get_rules` for schema reference
