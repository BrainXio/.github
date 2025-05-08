import logging
import signal
import time
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Set, Tuple, Union
from zoneinfo import ZoneInfo


logger = logging.getLogger(__name__)
from ..errors import BrainXioError


class Timeout:
    """Context manager for timeout using SIGALRM."""

    def __init__(self, seconds: int):
        self.seconds = seconds

    def handle_timeout(self, signum, frame):
        raise TimeoutError(f"Operation timed out after {self.seconds} seconds")

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


def run_task(
    task_dir: Path,
    task_name: str,
    params: Optional[Dict[str, Any]] = None,
    executed: Optional[Dict[str, bool]] = None,
    max_retries: int = 3,
    timeout: int = 60,
    dependency_chain: Optional[Set[str]] = None,
    output_queue: Optional[List[str]] = None,
    is_parallel: bool = False
) -> Union[Tuple[str, Optional[Exception]], None]:
    """Run a Python task script with retries, parameters, dependencies, and timeout."""
    params = params or {}
    executed = executed or {}
    dependency_chain = dependency_chain or set()
    output_queue = output_queue or [] if is_parallel else None

    logger.debug(f"Task {task_name} starting")
    if task_name in executed:
        logger.debug(f"Task {task_name} already executed, skipping")
        return task_name, None if is_parallel else None
    if task_name in dependency_chain:
        logger.warning(f"Skipping circular dependency: {task_name}")
        return task_name, None if is_parallel else None
    dependency_chain.add(task_name)
    task_file = task_dir / f"{task_name}.py"
    if not task_file.exists():
        exc = BrainXioError(f"Task not found: {task_file}")
        if is_parallel:
            return task_name, exc
        raise exc

    # Load dependencies if any
    spec = importlib.util.spec_from_file_location(task_name, task_file)
    if not spec or not spec.loader:
        raise BrainXioError(f"Failed to load task module: {task_file}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    dependencies = getattr(module, "dependencies", [])
    for dep in dependencies:
        if dep not in executed:
            run_task(task_dir, dep, params, executed, max_retries, timeout, dependency_chain, output_queue, is_parallel)

    for attempt in range(max_retries + 1):
        start_time = time.time()
        duration = 0
        try:
            if not hasattr(module, "run"):
                raise BrainXioError(f"Task {task_name} missing run function")

            with Timeout(timeout):
                result = module.run(**params)
                duration = time.time() - start_time

            executed[task_name] = True
            log_task(task_dir, task_name, "completed", start_time, duration, output_queue, is_parallel)

            if output_queue and is_parallel:
                output = getattr(result, "__str__", str)()
                output_queue.append(output + "\n")
            return task_name, None if is_parallel else None
        except (TimeoutError, Exception) as e:
            logger.error(f"Task {task_name} attempt {attempt + 1} failed: {e}")
            duration = time.time() - start_time
            if attempt == max_retries:
                log_task(task_dir, task_name, "failed", start_time, duration, output_queue, is_parallel)
                if is_parallel:
                    return task_name, e
                raise BrainXioError(f"Task {task_name} failed to complete: {e}") from e
            time.sleep(1)


def log_task(task_dir: Path, task_name: str, status: str, start_time: float, duration: float, output_queue: Optional[List[str]], is_parallel: bool) -> None:
    """Log task execution details to a JSON file."""
    log_dir = task_dir.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "tasks.json"
    log_entry = {
        "task_name": task_name,
        "status": status,
        "start_time": datetime.fromtimestamp(start_time, tz=ZoneInfo("UTC")).isoformat(),
        "duration": duration,
        "timestamp": datetime.now(tz=ZoneInfo("UTC")).isoformat(),
        "pid": 0
    }
    try:
        with log_file.open("a") as f:
            json.dump(log_entry, f)
            f.write("\n")
    except Exception as e:
        logger.error(f"Failed to log task {task_name}: {e}")


def run_tasks_parallel(task_dir: Path, task_names: List[str], params: Dict[str, Any], max_retries: int, timeout: int) -> None:
    """Run multiple tasks sequentially to simplify execution."""
    executed = {}
    output_queue = []
    exceptions = []

    for task_name in task_names:
        task_result, task_exception = run_task(task_dir, task_name, params, executed, max_retries, timeout, set(), output_queue, True)
        if task_exception:
            exceptions.append((task_name, task_exception))

    for output in output_queue:
        sys.stdout.write(output)
        sys.stdout.flush()

    if exceptions:
        for task_name, exception in exceptions:
            raise BrainXioError(f"Task {task_name} failed to complete: {exception}") from exception
