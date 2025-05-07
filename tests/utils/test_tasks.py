import pytest
from pathlib import Path
from src.brainxio.utils.tasks import run_task
from src.brainxio.errors import BrainXioError

def test_run_task_success(tmp_path: Path) -> None:
    """Test run_task executes a valid task script."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): print('Task executed')")
    run_task(task_dir, "test_task")

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
    with pytest.raises(BrainXioError, match="missing run\\(\\) function"):
        run_task(task_dir, "test_task")

def test_run_task_execution_error(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test run_task raises error for task execution failure."""
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): raise ValueError('Task error')")
    with pytest.raises(BrainXioError, match="Task execution failed: Task error"):
        run_task(task_dir, "test_task")
