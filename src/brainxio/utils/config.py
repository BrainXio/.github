import yaml
import os
from pathlib import Path
from typing import Any, Dict
from ..errors import ConfigError
from ..utils.cache import Cache

class Config:
    """Manages configuration from YAML file and cache."""
    def __init__(self, config_file: Path, cache: Cache) -> None:
        self._config_file = config_file
        self._cache = cache
        self._config: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load configuration from cache or YAML file."""
        cached_config = self._cache.get("config")
        if cached_config is not None:
            self._config = cached_config
            return
        try:
            if self._config_file.exists():
                with self._config_file.open("r") as f:
                    self._config = yaml.safe_load(f) or {}
            else:
                self._config = {"log_dir": str(Path.home() / ".brainxio"), "cache_dir": str(Path.home() / ".brainxio")}
            self._cache.set("config", self._config)
            self._cache.save()
        except (OSError, yaml.YAMLError) as e:
            raise ConfigError(f"Failed to load config: {e}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save."""
        self._config[key] = value
        self._cache.set("config", self._config)
        try:
            self._config_file.parent.mkdir(exist_ok=True)
            with self._config_file.open("w") as f:
                yaml.safe_dump(self._config, f)
            self._cache.save()
        except (OSError, yaml.YAMLError) as e:
            raise ConfigError(f"Failed to save config: {e}") from e
