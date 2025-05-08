import importlib.util
import logging
import json
import multiprocessing
import queue
import io
from contextlib import redirect_stdout
from datetime import datetime, UTC
from pathlib import Path
from typing import Dict, Any, List, Set, Optional, Tuple, Union
from ..errors import BrainXioError

logger = logging.getLogger(__name__)

def task_wrapper(args: Tuple[Path, str, Dict[str, Any], List[str], int, int, multiprocessing.Queue, bool]) -> Tuple[str, Optional[Exception]]:
    """Wrapper for running tasks in a multiprocessing pool."""
    task_dir, task_name, params, executed, max_retries, timeout, output_queue, is_parallel = args
    return run_task(task_dir, task_name, params, executed, max_retries, timeout, set(), output_queue, is_parallel)

def run_task(
    task_dir: Path,
    task_name: str,
    params: Optional[Dict[str, Any]] = None,
    executed: Optional[Set[str]] = None,
    max_retries: int = 3,
    timeout: int = 60,
    dependency_chain: Optional[Set[str]] = None,
    output_queue: Optional[multiprocessing.Queue] = None,
    is_parallel: bool = False
) -> Union[Tuple[str, Optional[Exception]], None]:
    """Run a Python task script with retries, parameters, dependencies, and timeout."""
    params = params or {}
    executed = executed or set()
    dependency_chain = dependency_chain or set()
    output_queue = output_queue or multiprocessing.Manager().Queue() if is_parallel else None

    if task_name in executed:
        logger.debug(f"Task {task_name} already executed, skipping in process {multiprocessing.current_process().pid}")
        return task_name, None if is_parallel else None
    if task_name in dependency_chain:
        logger.warning(f"Skipping circular dependency: {task_name} in process {multiprocessing.current_process().pid}")
        return task_name, None if is_parallel else None
    dependency_chain.add(task_name)
    task_file = task_dir / f"{task_name}.py"
    if not task_file.exists():
        exc = BrainXioError(f"Task not found: {task_file}")
        if is_parallel:
            return task_name, exc
        raise exc
    task_log = {
        "task_name": task_name,
        "start_time": datetime.now(UTC).isoformat(),
        "params": params,
        "status": "running",
        "attempts": 0
    }
    for attempt in range(max_retries + 1):
        task_log["attempts"] += 1
        log_task(task_dir, task_log)
        exception = None
        try:
            output = io.StringIO()
            with redirect_stdout(output):
                spec = importlib.util.spec_from_file_location(task_name, task_file)
                if spec is None or spec.loader is None:
                    raise BrainXioError(f"Failed to load task: {task_name}")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                dependencies = getattr(module, "dependencies", [])
                for dep in dependencies:
                    if dep not in executed:
                        dep_result, dep_exception = run_task(task_dir, dep, params, executed, max_retries, timeout, dependency_chain.copy(), output_queue, is_parallel)
                        if dep_exception:
                            raise dep_exception
                if hasattr(module, "run"):
                    module.run(**params)
                else:
                    raise BrainXioError(f"Task {task_name} missing run() function")
            with multiprocessing.Lock():
                executed.add(task_name)
            logger.debug(f"Task {task_name} marked as executed in process {multiprocessing.current_process().pid}")
            output_value = output.getvalue()
            if is_parallel:
                output_queue.put(output_value)
            else:
                print(output_value, end="", flush=True)
            logger.debug(f"Task {task_name} output handled: {output_value.strip()}")
            task_log["status"] = "completed"
            task_log["end_time"] = datetime.now(UTC).isoformat()
            log_task(task_dir, task_log)
            return task_name, None if is_parallel else None
        except Exception as e:
            exception = e
            logger.debug(f"Task {task_name} raised exception: {e} in process {multiprocessing.current_process().pid}")
            task_log["status"] = "failed"
            task_log["error"] = str(exception)
            task_log["end_time"] = datetime.now(UTC).isoformat()
            logger.error(f"Task {task_name} attempt {attempt + 1} failed: {exception}")
            if attempt == max_retries:
                log_task(task_dir, task_log)
                exc = BrainXioError(f"Task {task_name} failed after {max_retries + 1} attempts: {exception}")
                if is_parallel:
                    return task_name, exc
                raise exc
            log_task(task_dir, task_log)

def run_tasks_parallel(task_dir: Path, task_names: List[str], params: Dict[str, Any], max_retries: int, timeout: int) -> None:
    """Run multiple tasks in parallel using multiprocessing.Pool."""
    manager = multiprocessing.Manager()
    executed = manager.list()
    output_queue = manager.Queue()
    exceptions = []

    with multiprocessing.Pool(processes=len(task_names)) as pool:
        results = pool.map_async(task_wrapper, [(task_dir, name, params, executed, max_retries, timeout, output_queue, True) for name in task_names])
        results.wait(timeout=120)
        if not results.ready():
            pool.terminate()
            raise BrainXioError("Parallel tasks timed out after 120 seconds")
        for task_name, exception in results.get():
            if exception:
                exceptions.append((task_name, exception))

    while not output_queue.empty():
        output = output_queue.get()
        print(output, end="", flush=True)

    for task_name, exception in exceptions:
        raise BrainXioError(f"Task {task_name} failed to complete: {exception}") from exception

    for task_name in task_names:
        if task_name not in executed:
            raise BrainXioError(f"Task {task_name} failed to complete")

def log_task(task_dir: Path, task_log: Dict[str, Any]) -> None:
    """Log task execution details to a JSON file with file locking."""
    log_dir = task_dir.parent / "logs"
    log_file = log_dir / "tasks.json"
    lock_file = log_dir / "tasks.json.lock"
    try:
        log_dir.mkdir(exist_ok=True)
        with open(lock_file, "w") as f:
            try:
                import fcntl
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                logs = []
                if log_file.exists():
                    with log_file.open("r") as rf:
                        logs = json.load(rf)
                logs.append(task_log)
                with log_file.open("w") as wf:
                    json.dump(logs, wf, indent=2)
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except (OSError, json.JSONDecodeError, ImportError) as e:
        logger.warning(f"Failed to log task: {e}")
