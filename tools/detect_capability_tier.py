#!/usr/bin/env python3
"""
detect_capability_tier.py

Auto-detects current hardware + subscription tier for safe operation.
Outputs worker tier (A/B/C) and trainer tier (1/2/3).
"""

import json
import subprocess
from typing import Any, Dict


def detect_capability_tier() -> Dict[str, Any]:
    worker_tier = "C"
    trainer_tier = "3"

    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.total", "--format=csv,noheader,nounits"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            vram = int(result.stdout.strip())
            if vram >= 23000:
                worker_tier = "A"
                trainer_tier = "1"
            elif vram >= 8000:
                worker_tier = "B"
                trainer_tier = "2"
    except Exception:
        pass

    return {
        "worker_tier": worker_tier,
        "trainer_tier": trainer_tier,
        "note": f"Detected Worker Tier {worker_tier} | Trainer Tier {trainer_tier}",
    }


if __name__ == "__main__":
    print(json.dumps(detect_capability_tier(), indent=2))
