import json
import logging
from datetime import datetime, UTC
import pytest
from pathlib import Path
import time
from src.brainxio.utils.tasks import run_task, run_tasks_parallel, log_task, Timeout
from src.brainxio.errors import BrainXioError


logger = logging.getLogger(__name__)


def test_run_task_success(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Test run_task executes a valid task script."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): print('Task executed')")
    run_task(task_dir, "test_task")
    captured = capsys.readouterr()
    assert "Task executed" in captured.out
    log_file = tmp_path / "logs" / "tasks.json"
    assert log_file.exists()
    with log_file.open() as f:
        logs = [json.loads(line) for line in f]
    assert any(log["task_name"] == "test_task" and log["status"] == "completed" for log in logs)


def test_run_task_with_params(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Test run_task with parameters."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(key): print(f'Param: {key}')")
    run_task(task_dir, "test_task", {"key": "value"})
    captured = capsys.readouterr()
    assert "Param: value" in captured.out
    log_file = tmp_path / "logs" / "tasks.json"
    with log_file.open() as f:
        logs = [json.loads(line) for line in f]
    assert any(log["task_name"] == "test_task" and log["status"] == "completed" for log in logs)


def test_run_task_with_dependencies(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Test run_task with dependencies."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "dep_task.py"
    task_file1.write_text("def run(): print('Dependency executed')")
    task_file2 = task_dir / "main_task.py"
    task_file2.write_text("dependencies = ['dep_task']\ndef run(): print('Main task executed')")
    run_task(task_dir, "main_task")
    captured = capsys.readouterr()
    assert "Dependency executed" in captured.out
    assert "Main task executed" in captured.out
    log_file = tmp_path / "logs" / "tasks.json"
    with log_file.open() as f:
        logs = [json.loads(line) for line in f]
    assert any(log["task_name"] == "dep_task" and log["status"] == "completed" for log in logs)
    assert any(log["task_name"] == "main_task" and log["status"] == "completed" for log in logs)


def test_run_task_circular_dependency(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Test run_task handles circular dependencies."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("dependencies = ['task2']\ndef run(): print('Task1 executed')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("dependencies = ['task1']\ndef run(): print('Task2 executed')")
    run_task(task_dir, "task1")
    captured = capsys.readouterr()
    assert "Task1 executed" in captured.out
    assert "Task2 executed" in captured.out
    log_file = tmp_path / "logs" / "tasks.json"
    with log_file.open() as f:
        logs = [json.loads(line) for line in f]
    assert any(log["task_name"] == "task1" and log["status"] == "completed" for log in logs)


def test_run_task_missing_file(tmp_path: Path) -> None:
    """Test run_task raises error for missing task file."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    with pytest.raises(BrainXioError, match="Task not found"):
        run_task(task_dir, "missing_task")


def test_run_task_missing_run_function(tmp_path: Path) -> None:
    """Test run_task raises error for missing run function."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def other(): pass")
    with pytest.raises(BrainXioError, match="Task test_task missing run function"):
        run_task(task_dir, "test_task")


def test_run_task_execution_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_task raises error for task execution failure."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): raise ValueError('Task error')")
    with pytest.raises(BrainXioError, match="Task test_task failed to complete: Task error"):
        run_task(task_dir, "test_task", max_retries=1)


def test_run_task_load_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_task raises error for task load failure."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): pass")
    monkeypatch.setattr("importlib.util.spec_from_file_location", lambda name, path: None)
    with pytest.raises(BrainXioError, match="Failed to load task module"):
        run_task(task_dir, "test_task", max_retries=1)


def test_log_task_write_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture) -> None:
    """Test log_task handles write errors gracefully."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    def raise_oserror(*args, **kwargs):
        raise OSError("Write error")
    monkeypatch.setattr(Path, "open", raise_oserror)
    caplog.set_level(logging.ERROR)
    log_task(task_dir, "test_task", "running", time.time(), 0.1, None, False)
    assert "Failed to log task test_task: Write error" in caplog.text


def test_run_task_retry_success(tmp_path: Path, capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_task retries and succeeds after initial failure."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    count_file = task_dir / "count.txt"
    count_file.write_text("0")
    task_file = task_dir / "test_task.py"
    task_file.write_text(f"def run():\n    with open('{count_file}', 'r+') as f:\n        count = int(f.read())\n        count += 1\n        f.seek(0)\n        f.write(str(count))\n        if count < 2: raise ValueError('Retry error')\n        print('Task executed')")
    run_task(task_dir, "test_task", max_retries=2)
    captured = capsys.readouterr()
    assert "Task executed" in captured.out
    log_file = tmp_path / "logs" / "tasks.json"
    assert log_file.exists()
    with log_file.open() as f:
        logs = [json.loads(line) for line in f]
    assert any(log["task_name"] == "test_task" and log["status"] == "completed" for log in logs)


def test_run_task_timeout(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_task raises error for timeout."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("import time\ndef run(): time.sleep(5)")
    with pytest.raises(BrainXioError, match="Task test_task failed to complete: Operation timed out"):
        run_task(task_dir, "test_task", max_retries=0, timeout=1)


def test_run_tasks_parallel_success(tmp_path: Path, capsys: pytest.CaptureFixture) -> None:
    """Test run_tasks_parallel executes tasks successfully."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("def run(): print('Task1 executed')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("def run(): print('Task2 executed')")
    run_tasks_parallel(task_dir, ["task1", "task2"], {}, max_retries=0, timeout=10)
    captured = capsys.readouterr()
    assert "Task1 executed" in captured.out
    assert "Task2 executed" in captured.out


def test_run_tasks_parallel_failure(tmp_path: Path) -> None:
    """Test run_tasks_parallel raises error for task failure."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("def run(): raise ValueError('Task1 error')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("def run(): print('Task2 executed')")
    with pytest.raises(BrainXioError, match="Task task1 failed to complete: Task1 error"):
        run_tasks_parallel(task_dir, ["task1", "task2"], {}, max_retries=0, timeout=10)
