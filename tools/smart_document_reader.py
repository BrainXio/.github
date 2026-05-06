#!/usr/bin/env python3
"""
smart_document_reader.py

Tier-aware, context-window-safe document reader.
Prevents OOM and excessive token usage for lower-capability agents.
"""

import json
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def smart_document_reader(
    doc_path: str, max_tokens: Optional[int] = None, tier: str = "C"
) -> Dict[str, Any]:
    path = Path(doc_path).resolve()
    if not path.exists():
        return {
            "status": "error",
            "error": f"Document not found: {doc_path}",
            "action": "escalate_to_human",
        }

    content = path.read_text(encoding="utf-8")
    total_tokens = estimate_tokens(content)

    tier_limits = {"C": 8000, "B": 32000, "A": 128000}
    safe_limit = tier_limits.get(tier.upper(), 8000)

    if max_tokens is None:
        max_tokens = safe_limit

    if total_tokens <= max_tokens:
        return {
            "status": "full",
            "content": content,
            "tokens_used": total_tokens,
            "note": "Full document safely loaded within tier limits.",
        }

    if tier.upper() == "C":
        truncated = content[:6000]
        return {
            "status": "truncated",
            "content": truncated
            + "\n\n[TRUNCATED: Tier C agent - document exceeds safe limit. Escalate to Tier B+ agent or human if full context is required.]",
            "tokens_used": estimate_tokens(truncated),
            "note": "Tier C: Truncated to safe limit. Consider escalating.",
        }

    sections = [s for s in content.split("\n\n#") if s.strip()]
    safe_content = "#".join(sections[:3])
    return {
        "status": "partial",
        "content": safe_content
        + "\n\n[PARTIAL: Full document exceeds requested limit. Key sections provided.]",
        "tokens_used": estimate_tokens(safe_content),
        "note": f"Tier {tier}: Partial load. Full document had ~{total_tokens} tokens.",
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python smart_document_reader.py <path> [tier] [max_tokens]")
        sys.exit(1)
    result = smart_document_reader(
        sys.argv[1],
        int(sys.argv[3]) if len(sys.argv) > 3 else None,
        sys.argv[2] if len(sys.argv) > 2 else "C",
    )
    print(json.dumps(result, indent=2))
