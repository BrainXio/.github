# How to Use the Smart Document Reader

The `smart_document_reader.py` tool is the primary way for agents to safely load documentation without causing OOM or exceeding their context window.

## Basic Usage

```bash
# Full auto (uses agent's declared tier)
uv run --directory .github/tools python smart_document_reader.py docs/reference/cpr-procedure.md

# Force a specific tier and token limit
uv run --directory .github/tools python smart_document_reader.py docs/reference/cpr-procedure.md A 32000
```

## What It Returns

- `status`: `full`, `partial`, or `truncated`
- `content`: the (possibly summarized/truncated) text
- `tokens_used`: estimated token count
- `note`: human-readable explanation and escalation guidance

## When to Escalate

If the reader returns a `truncated` or `partial` result and the agent still cannot complete its task, it should escalate to a higher-tier agent or to the human (Core Role).

**Example escalation message:**

> Task requires full `cpr-procedure.md` (est. 18k tokens). Current tier C limit reached. Requesting Tier B or human assistance.
