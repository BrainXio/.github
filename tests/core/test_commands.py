import logging
import pytest
from pathlib import Path
from src.brainxio.core.commands import CommandRegistry, ConfigCommand, ClearCacheCommand, ResetConfigCommand
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
