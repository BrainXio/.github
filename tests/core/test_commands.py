import logging
import pytest
import sys
from pathlib import Path
from typing import Dict, Any
from src.brainxio.core.commands import Command, ConfigCommand, ClearCacheCommand, ResetConfigCommand, RunTaskCommand, CommandRegistry
from src.brainxio.utils.config import Config
from src.brainxio.utils.cache import Cache
from src.brainxio.errors import BrainXioError


@pytest.fixture
def config(tmp_path: Path):
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    return Config(config_file, cache)


def test_config_command_show(capsys: pytest.CaptureFixture, config: Config) -> None:
    """Test ConfigCommand show action."""
    command = ConfigCommand(config)
    command.execute({"action": "show"})
    captured = capsys.readouterr()
    assert "log_dir = " + str(Path.home() / ".brainxio") in captured.out


def test_config_command_set(capsys: pytest.CaptureFixture, config: Config) -> None:
    """Test ConfigCommand set action."""
    command = ConfigCommand(config)
    command.execute({"action": "set", "key": "log_dir", "value": "/new/log"})
    captured = capsys.readouterr()
    assert "Set log_dir = /new/log" in captured.out


def test_clear_cache_command(caplog: pytest.LogCaptureFixture, config: Config) -> None:
    """Test ClearCacheCommand clears cache."""
    config.cache.set("test", "value")
    command = ClearCacheCommand(config)
    caplog.set_level(logging.INFO)
    command.execute({})
    assert config.cache.get("test") is None
    assert "Cache cleared successfully" in caplog.text


def test_reset_config_command(caplog: pytest.LogCaptureFixture, config: Config) -> None:
    """Test ResetConfigCommand resets config."""
    config.set("log_dir", "/custom/log")
    command = ResetConfigCommand(config)
    caplog.set_level(logging.INFO)
    command.execute({})
    assert config.get("log_dir") is None
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
    command.execute({"task_names": ["test_task"]})
    captured = capsys.readouterr()
    assert "Task executed" in captured.out
    assert "Task test_task executed successfully" in captured.out


def test_run_task_command_with_params(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test RunTaskCommand with parameters."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(key): print(f'Param: {key}')")
    config.set("task_dir", str(task_dir))
    command = RunTaskCommand(config)
    command.execute({"task_names": ["test_task"], "params": {"key": "value"}})
    captured = capsys.readouterr()
    assert "Param: value" in captured.out
    assert "Task test_task executed successfully" in captured.out


def test_run_task_command_multiple_tasks(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test RunTaskCommand with multiple tasks."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("def run(): print('Task1 executed')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("def run(): print('Task2 executed')")
    config.set("task_dir", str(task_dir))
    command = RunTaskCommand(config)
    command.execute({"task_names": ["task1", "task2"]})
    captured = capsys.readouterr()
    assert "Task1 executed" in captured.out
    assert "Task2 executed" in captured.out
    assert "Task task1 executed successfully" in captured.out
    assert "Task task2 executed successfully" in captured.out


def test_run_task_command_with_max_retries(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test RunTaskCommand respects max_retries configuration."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    count_file = task_dir / "count.txt"
    count_file.write_text("0")
    task_file = task_dir / "test_task.py"
    task_file.write_text(f"def run():\n    with open('{count_file}', 'r+') as f:\n        count = int(f.read())\n        count += 1\n        f.seek(0)\n        f.write(str(count))\n        if count < 2: raise ValueError('Retry error')\n        print('Task executed')")
    config.set("task_dir", str(task_dir))
    config.set("max_retries", "1")
    command = RunTaskCommand(config)
    command.execute({"task_names": ["test_task"]})
    captured = capsys.readouterr()
    assert "Task executed" in captured.out
    with count_file.open("r") as f:
        assert int(f.read()) == 2
    assert "Task test_task executed successfully" in captured.out


def test_run_task_command_parallel(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test RunTaskCommand with parallel execution."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("def run(): print('Task1 executed')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("def run(): print('Task2 executed')")
    config.set("task_dir", str(task_dir))
    command = RunTaskCommand(config)
    command.execute({"task_names": ["task1", "task2"], "parallel": True})
    captured = capsys.readouterr()
    assert "Task1 executed" in captured.out
    assert "Task2 executed" in captured.out


def test_run_task_command_parallel_failure(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test RunTaskCommand with parallel execution and failure."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("def run(): raise ValueError('Task1 error')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("def run(): print('Task2 executed')")
    config.set("task_dir", str(task_dir))
    config.set("max_retries", "0")
    command = RunTaskCommand(config)
    with pytest.raises(BrainXioError, match="Task task1 failed to complete: Task1 error"):
        command.execute({"task_names": ["task1", "task2"], "parallel": True})
    captured = capsys.readouterr()
    assert "Task2 executed" in captured.out


def test_run_task_command_missing_task(tmp_path: Path) -> None:
    """Test RunTaskCommand raises error for missing task."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    command = RunTaskCommand(config)
    with pytest.raises(BrainXioError, match="Task not found"):
        command.execute({"task_names": ["missing_task"]})


def test_run_task_command_no_task_name(tmp_path: Path) -> None:
    """Test RunTaskCommand raises error for no task name."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    command = RunTaskCommand(config)
    with pytest.raises(BrainXioError, match="At least one task name required"):
        command.execute({})


def test_plugin_loading_success(capsys: pytest.CaptureFixture, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading a valid plugin."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    plugin_file = plugin_dir / "test_plugin.py"
    plugin_file.write_text("""
from src.brainxio.core.commands import Command, CommandRegistry
class TestPluginCommand(Command):
    def execute(self, args):
        print('Plugin executed')
def register_command(registry: CommandRegistry):
    registry.register_command('test-plugin', TestPluginCommand(registry.config))
    """)
    config.set("plugin_dir", str(plugin_dir))
    sys.path.append(str(plugin_dir))
    try:
        registry = CommandRegistry(config)
        registry.execute("test-plugin", {})
        captured = capsys.readouterr()
        assert "Plugin executed" in captured.out
    finally:
        sys.path.remove(str(plugin_dir))


def test_plugin_loading_missing_register(tmp_path: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Test loading a plugin without register_command function."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    plugin_file = plugin_dir / "test_plugin.py"
    plugin_file.write_text("def other(): pass")
    config.set("plugin_dir", str(plugin_dir))
    caplog.set_level(logging.WARNING)
    sys.path.append(str(plugin_dir))
    try:
        registry = CommandRegistry(config)
        assert "Plugin test_plugin missing register_command function" in caplog.text
    finally:
        sys.path.remove(str(plugin_dir))


def test_plugin_loading_error(tmp_path: Path, caplog: pytest.LogCaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test loading a plugin with execution error."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    plugin_file = plugin_dir / "test_plugin.py"
    plugin_file.write_text("raise ValueError('Plugin error')")
    config.set("plugin_dir", str(plugin_dir))
    caplog.set_level(logging.ERROR)
    sys.path.append(str(plugin_dir))
    try:
        registry = CommandRegistry(config)
        assert "Failed to load plugin test_plugin" in caplog.text
    finally:
        sys.path.remove(str(plugin_dir))


def test_command_registry_execute(tmp_path: Path) -> None:
    """Test CommandRegistry executes registered commands."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    registry = CommandRegistry(config)
    registry.execute("config", {"action": "show"})


def test_command_registry_unknown_command(config: Config) -> None:
    """Test CommandRegistry raises error for unknown command."""
    registry = CommandRegistry(config)
    with pytest.raises(BrainXioError, match="Unknown command: unknown"):
        registry.execute("unknown", {})


def test_command_execute_signature(config: Config) -> None:
    """Test Command execute method signature coverage."""
    class MockCommand(Command):
        def execute(self, args: Dict[str, Any]) -> None:
            pass
    command = MockCommand(config)
    command.execute({})
