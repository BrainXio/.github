#!/usr/bin/env python3
"""
bootstrap_environment.py

One-command environment bootstrap for agents.
Detects tier, creates .venv if needed, and prints readiness status.
"""

import subprocess
import sys
from pathlib import Path


def bootstrap():
    print("🚀 Bootstrapping BrainXio environment...")

    # Detect tier
    result = subprocess.run(
        [sys.executable, "detect_capability_tier.py"], capture_output=True, text=True
    )
    print(result.stdout)

    # Ensure .venv exists
    venv = Path(".venv")
    if not venv.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

    print(
        "✅ Environment ready. Use 'uv run --directory .github/tools <script>' for all tools."
    )


if __name__ == "__main__":
    bootstrap()
