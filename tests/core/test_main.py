import logging
import pytest
import sys
from pathlib import Path
from src.brainxio.core.main import main, parse_args
from src.brainxio.utils.cache import Cache
from src.brainxio.utils.config import Config

def test_main(caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main CLI entry point logs and outputs version."""
    monkeypatch.setattr(sys, "argv", ["brainxio"])
    caplog.set_level(logging.INFO)
    main()
    captured = capsys.readouterr()
    assert "Starting BrainXio CLI" in caplog.text
    assert "CLI arguments: {'command': None}" in caplog.text
    assert "BrainXio CLI v0.1.0" in captured.out

def test_parse_args_version(capsys: pytest.CaptureFixture) -> None:
    """Test --version argument displays version and exits."""
    with pytest.raises(SystemExit):
        parse_args(["--version"])
    captured = capsys.readouterr()
    assert "BrainXio 0.1.0" in captured.out

def test_parse_args_help(capsys: pytest.CaptureFixture) -> None:
    """Test --help argument displays usage and exits."""
    with pytest.raises(SystemExit):
        parse_args(["--help"])
    captured = capsys.readouterr()
    assert "BrainXio CLI for automation and AI tasks" in captured.out

def test_config_show(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test config show command displays log_dir."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    cache = Cache(cache_file)
    cache.set("config", {"log_dir": str(Path.home() / ".brainxio")})
    cache.save()
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "config", "show"])
    main()
    captured = capsys.readouterr()
    assert ".brainxio" in captured.out

def test_config_set(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test config set command updates configuration."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "config", "set", "log_dir", "/new/log"])
    main()
    captured = capsys.readouterr()
    assert "Set log_dir to /new/log" in captured.out

def test_clear_cache(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test clear-cache command clears cache."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "clear-cache"])
    main()
    captured = capsys.readouterr()
    assert "Cache cleared successfully" in captured.out

def test_reset_config(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test reset-config command resets configuration."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "reset-config"])
    main()
    captured = capsys.readouterr()
    assert "Configuration reset to defaults" in captured.out

def test_run_task(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test run-task command executes task."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(): print('Task executed')")
    cache = Cache(cache_file)
    config = Config(config_file, cache)
    config.set("task_dir", str(task_dir))
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "run-task", "test_task"])
    main()
    captured = capsys.readouterr()
    assert "Task executed" in captured.out
    assert "Task test_task executed successfully" in captured.out

def test_run_task_with_params(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test run-task command with parameters."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file = task_dir / "test_task.py"
    task_file.write_text("def run(key): print(f'Param: {key}')")
    cache = Cache(cache_file)
    config = Config(config_file, cache)
    config.set("task_dir", str(task_dir))
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "run-task", "test_task", "--param", "key=value"])
    main()
    captured = capsys.readouterr()
    assert "Param: value" in captured.out
    assert "Task test_task executed successfully" in captured.out

def test_run_task_multiple(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test run-task command with multiple tasks."""
    config_file = tmp_path / "config.yaml"
    cache_file = tmp_path / "cache.json"
    task_dir = tmp_path / "tasks"
    task_dir.mkdir()
    task_file1 = task_dir / "task1.py"
    task_file1.write_text("def run(): print('Task1 executed')")
    task_file2 = task_dir / "task2.py"
    task_file2.write_text("def run(): print('Task2 executed')")
    cache = Cache(cache_file)
    config = Config(config_file, cache)
    config.set("task_dir", str(task_dir))
    monkeypatch.setattr("config.settings.CONFIG_FILE", config_file)
    monkeypatch.setattr("config.settings.CACHE_FILE", cache_file)
    monkeypatch.setattr(sys, "argv", ["brainxio", "run-task", "task1", "task2"])
    main()
    captured = capsys.readouterr()
    assert "Task1 executed" in captured.out
    assert "Task2 executed" in captured.out
    assert "Task task1 executed successfully" in captured.out
    assert "Task task2 executed successfully" in captured.out
