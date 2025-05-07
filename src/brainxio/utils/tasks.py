import importlib.util
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Set
from ..errors import BrainXioError

logger = logging.getLogger(__name__)

def run_task(task_dir: Path, task_name: str, params: Dict[str, Any] = None, executed: Set[str] = None) -> None:
    """Run a Python task script from the task directory with optional parameters and dependencies."""
    params = params or {}
    executed = executed or set()
    if task_name in executed:
        return
    executed.add(task_name)  # Add before recursion to prevent infinite loops
    task_file = task_dir / f"{task_name}.py"
    if not task_file.exists():
        raise BrainXioError(f"Task not found: {task_file}")
    task_log = {
        "task_name": task_name,
        "start_time": datetime.utcnow().isoformat(),
        "params": params,
        "status": "running"
    }
    log_task(task_dir, task_log)
    try:
        spec = importlib.util.spec_from_file_location(task_name, task_file)
        if spec is None or spec.loader is None:
            raise BrainXioError(f"Failed to load task: {task_name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        dependencies = getattr(module, "dependencies", [])
        for dep in dependencies:
            run_task(task_dir, dep, params, executed)
        if hasattr(module, "run"):
            module.run(**params)
            task_log["status"] = "completed"
            task_log["end_time"] = datetime.utcnow().isoformat()
        else:
            raise BrainXioError(f"Task {task_name} missing run() function")
    except Exception as e:
        task_log["status"] = "failed"
        task_log["error"] = str(e)
        task_log["end_time"] = datetime.utcnow().isoformat()
        logger.error(f"Task {task_name} failed: {e}")
        raise BrainXioError(f"Task execution failed: {e}") from e
    finally:
        log_task(task_dir, task_log)

def log_task(task_dir: Path, task_log: Dict[str, Any]) -> None:
    """Log task execution details to a JSON file."""
    log_dir = task_dir.parent / "logs"
    log_file = log_dir / "tasks.json"
    try:
        log_dir.mkdir(exist_ok=True)
        logs = []
        if log_file.exists():
            with log_file.open("r") as f:
                logs = json.load(f)
        logs.append(task_log)
        with log_file.open("w") as f:
            json.dump(logs, f, indent=2)
    except (OSError, json.JSONDecodeError) as e:
        logger.warning(f"Failed to log task: {e}")
