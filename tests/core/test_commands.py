import logging
import pytest
from pathlib import Path
from typing import Dict, Any
from src.brainxio.core.commands import CommandRegistry, ConfigCommand, ClearCacheCommand, ResetConfigCommand, RunTaskCommand, Command
from src.brainxio.utils.cache import Cache
from src.brainxio.utils.config import Config
from src.brainxio.errors import BrainXioError

def test_config_command_show(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    """Test ConfigCommand show action."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    command = ConfigCommand(config)
    command.execute({"action": "show"})
    captured = capsys.readouterr()
    assert ".brainxio" in captured.out

def test_config_command_set(capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
    """Test ConfigCommand set action."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    command = ConfigCommand(config)
    command.execute({"action": "set", "key": "log_dir", "value": "/new/log"})
    captured = capsys.readouterr()
    assert "Set log_dir to /new/log" in captured.out

def test_clear_cache_command(caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    """Test ClearCacheCommand clears cache."""
    cache_file = tmp_path / "cache.json"
    cache = Cache(cache_file)
    cache.set("test", "value")
    command = ClearCacheCommand(cache)
    caplog.set_level(logging.INFO)
    command.execute({})
    assert cache.get("test") is None
    assert "Cache cleared" in caplog.text

def test_reset_config_command(caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    """Test ResetConfigCommand resets config."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    config.set("log_dir", "/custom/log")
    command = ResetConfigCommand(config)
    caplog.set_level(logging.INFO)
    command.execute({})
    assert config.get("log_dir").endswith(".brainxio")
    assert "Configuration reset to defaults" in caplog.text

def test_run_task_command(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test RunTaskCommand executes task."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): print('Task executed')")
    config.set("task_dir", str(task_dir))
    command = RunTaskCommand(config)
    command.execute({"task_name": "test_task"})
    captured = capsys.readouterr()
    assert "Task executed" in captured.out
    assert "Task test_task executed successfully" in captured.out

def test_run_task_command_missing_task(tmp_path: Path) -> None:
    """Test RunTaskCommand raises error for missing task."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    command = RunTaskCommand(config)
    with pytest.raises(BrainXioError, match="Task not found"):
        command.execute({"task_name": "missing_task"})

def test_run_task_command_no_task_name(tmp_path: Path) -> None:
    """Test RunTaskCommand raises error for no task name."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    command = RunTaskCommand(config)
    with pytest.raises(BrainXioError, match="Task name required"):
        command.execute({})

def test_command_registry_execute(tmp_path: Path) -> None:
    """Test CommandRegistry executes registered commands."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    registry = CommandRegistry()
    registry.register("config", ConfigCommand(config))
    registry.execute("config", {"action": "show"})

def test_command_registry_unknown_command() -> None:
    """Test CommandRegistry raises error for unknown command."""
    registry = CommandRegistry()
    with pytest.raises(BrainXioError, match="Unknown command: invalid"):
        registry.execute("invalid", {})

def test_command_execute_signature() -> None:
    """Test Command execute method signature coverage."""
    class MockCommand(Command):
        def execute(self, args: Dict[str, Any]) -> None:
            pass
    command = MockCommand()
    command.execute({})
