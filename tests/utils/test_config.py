import os
import yaml
import pytest
from pathlib import Path
from src.brainxio.utils.config import Config
from src.brainxio.utils.cache import Cache
from src.brainxio.errors import ConfigError

def test_config_init(tmp_path: Path) -> None:
    """Test config initialization with default values."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    assert config.get("log_dir").endswith(".brainxio")

def test_config_load_from_file(tmp_path: Path) -> None:
    """Test loading config from YAML file."""
    config_file = tmp_path / "config.yaml"
    with config_file.open("w") as f:
        yaml.safe_dump({"log_dir": "/custom/log"}, f)
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    assert config.get("log_dir") == "/custom/log"

def test_config_load_from_cache(tmp_path: Path) -> None:
    """Test loading config from cache."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    cache.set("config", {"log_dir": "/cached/log"})
    cache.save()
    config = Config(config_file, cache)
    assert config.get("log_dir") == "/cached/log"

def test_config_set_and_save(tmp_path: Path) -> None:
    """Test setting and saving config."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    config.set("log_dir", "/new/log")
    config = Config(config_file, cache)  # Reload to verify
    assert config.get("log_dir") == "/new/log"

def test_config_load_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test config load raises ConfigError on invalid YAML."""
    config_file = tmp_path / "config.yaml"
    with config_file.open("w") as f:
        f.write("invalid: yaml: here")
    cache = Cache(tmp_path / "cache.json")
    with pytest.raises(ConfigError, match="Failed to load config"):
        Config(config_file, cache)

def test_config_save_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test config save raises ConfigError on write permission error."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    monkeypatch.setattr(os, "access", lambda x, y: False)
    monkeypatch.setattr(Cache, "save", lambda self: None)  # Mock cache.save to succeed
    with pytest.raises(ConfigError, match="No write permission"):
        config.set("log_dir", "/new/log")

def test_config_save_yaml_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test config save raises ConfigError on YAML error."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    def mock_dump(*args, **kwargs):
        raise yaml.YAMLError("Mocked YAML error")
    monkeypatch.setattr(yaml, "safe_dump", mock_dump)
    with pytest.raises(ConfigError, match="Failed to save config: Mocked YAML error"):
        config.set("log_dir", "/new/log")

def test_config_invalid_key(tmp_path: Path) -> None:
    """Test setting invalid config key raises ConfigError."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    with pytest.raises(ConfigError, match="Invalid configuration key: invalid_key"):
        config.set("invalid_key", "value")

def test_config_plugin_dir(tmp_path: Path) -> None:
    """Test setting and retrieving plugin_dir."""
    config_file = tmp_path / "config.yaml"
    cache = Cache(tmp_path / "cache.json")
    config = Config(config_file, cache)
    config.set("plugin_dir", "/custom/plugins")
    assert config.get("plugin_dir") == "/custom/plugins"
