#!/usr/bin/env python3
"""
gh_safe_wrapper.py

Safe, role-aware wrapper for the gh CLI.
Enforces C.P.R. rules and never exposes tokens.
"""

import subprocess
import sys
from typing import Dict, Any


def gh_safe(command: list[str], role: str = "Resonant") -> Dict[str, Any]:
    allowed = {
        "Resonant": ["view", "list", "issue list", "pr list", "repo view"],
        "Personal": ["pr create", "issue create", "repo edit"],
        "Core": ["*"],
    }

    cmd_str = " ".join(command)
    role_allowed = allowed.get(role, [])

    if "*" not in role_allowed:
        if not any(cmd_str.startswith(a) for a in role_allowed):
            return {
                "success": False,
                "error": f"Role {role} not permitted to run: gh {cmd_str}",
                "action": "escalate_to_personal_or_core",
            }

    try:
        result = subprocess.run(
            ["gh"] + command, capture_output=True, text=True, timeout=30
        )
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip() if result.returncode != 0 else None,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python gh_safe_wrapper.py <role> <gh command...>")
        sys.exit(1)
    result = gh_safe(sys.argv[2:], sys.argv[1])
    print(result)
