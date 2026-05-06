#!/usr/bin/env python3
"""
threshold_enforcer.py

Checks if current agent tier is allowed to perform a given task/skill.
"""

import json
import sys
from typing import Dict, Any


def check_threshold(skill: str, worker_tier: str, trainer_tier: str) -> Dict[str, Any]:
    requirements = {
        "commit": ("C", None),
        "pull_request": ("B", None),
        "review": ("B", None),
        "project_kanban": ("B", None),
        "project_roadmap": ("A", None),
        "core_decision": ("A", None),
        "trainer_task": (None, "1"),
        "fine_tune": (None, "1"),
        "smart_document_reader": ("C", None),
    }

    req_worker, req_trainer = requirements.get(skill.lower(), ("C", None))

    worker_ok = True
    if req_worker:
        tier_order = {"C": 0, "B": 1, "A": 2}
        worker_ok = tier_order.get(worker_tier, 0) >= tier_order.get(req_worker, 0)

    trainer_ok = True
    if req_trainer:
        trainer_ok = int(trainer_tier) <= int(req_trainer)

    allowed = worker_ok and trainer_ok

    return {
        "allowed": allowed,
        "required_worker_tier": req_worker,
        "required_trainer_tier": req_trainer,
        "current_worker_tier": worker_tier,
        "current_trainer_tier": trainer_tier,
        "action": "proceed" if allowed else "escalate",
    }


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(
            "Usage: python threshold_enforcer.py <skill> <worker_tier> <trainer_tier>"
        )
        sys.exit(1)
    print(json.dumps(check_threshold(sys.argv[1], sys.argv[2], sys.argv[3]), indent=2))
