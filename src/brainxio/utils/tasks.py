import importlib.util
import logging
from pathlib import Path
from typing import Dict, Any, List
from ..errors import BrainXioError

logger = logging.getLogger(__name__)

def run_task(task_dir: Path, task_name: str, params: Dict[str, Any] = None, executed: set = None) -> None:
    """Run a Python task script from the task directory with optional parameters and dependencies."""
    params = params or {}
    executed = executed or set()
    if task_name in executed:
        return
    task_file = task_dir / f"{task_name}.py"
    if not task_file.exists():
        raise BrainXioError(f"Task not found: {task_file}")
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
            executed.add(task_name)
        else:
            raise BrainXioError(f"Task {task_name} missing run() function")
    except Exception as e:
        logger.error(f"Task {task_name} failed: {e}")
        raise BrainXioError(f"Task execution failed: {e}") from e
