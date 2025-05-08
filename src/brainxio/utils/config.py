import logging
import yaml
import re
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union

from ..errors import ConfigError

logger = logging.getLogger(__name__)


class Config:
    """Configuration management for BrainXio."""

    VALID_KEYS = {'log_dir', 'task_dir', 'plugin_dir', 'max_retries', 'timeout'}

    def __init__(self, config_file: Union[str, Path], cache: 'Cache'):
        self.config_file = Path(config_file)
        self.cache = cache
        self._config: Dict[str, Any] = {"log_dir": str(Path.home() / ".brainxio")}
        self.load()

    def load(self) -> None:
        """Load configuration from file or cache."""
        try:
            cached_config = self.cache.get("config", {})
            if cached_config:
                self._config = cached_config
                logger.debug(f"Loaded config from cache: {self._config}")
                return
            if self.config_file.exists():
                with self.config_file.open("r") as f:
                    self._config = yaml.safe_load(f) or {}
                logger.debug(f"Loaded config from file: {self._config}")
                self.cache.set("config", self._config)
                self.cache.save()
        except yaml.YAMLError as e:
            raise ConfigError(f"Failed to load config: {e}")
        except OSError as e:
            raise ConfigError(f"Failed to load config: {e}")

    def save(self) -> None:
        """Save configuration to file and cache, converting Path objects to strings."""
        try:
            if not os.access(self.config_file.parent, os.W_OK):
                raise ConfigError(f"No write permission for {self.config_file.parent}")
            config_copy = {k: str(v) if isinstance(v, Path) else v for k, v in self._config.items()}
            with self.config_file.open("w") as f:
                yaml.safe_dump(config_copy, f)
            self.cache.set("config", config_copy)
            self.cache.save()
        except yaml.YAMLError as e:
            raise ConfigError(f"Failed to save config: {e}")
        except OSError as e:
            raise ConfigError(f"Failed to save config: {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value by key."""
        value = self._config.get(key, default)
        return value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save."""
        if key not in self.VALID_KEYS:
            raise ConfigError(f"Invalid configuration key: {key}")
        if not re.match(r"^[a-z][a-z0-9_-]*$", key):
            raise ConfigError(f"Invalid configuration key format: {key}")
        if key == "plugin_dir":
            value = str(Path(value).expanduser().resolve())
        elif key == "max_retries":
            try:
                value = int(value)
                if value < 0:
                    raise ConfigError(f"Invalid max_retries value: max_retries must be non-negative")
            except ValueError:
                raise ConfigError(f"Invalid max_retries value: {value}")
        elif key == "timeout":
            try:
                value = int(value)
                if value <= 0:
                    raise ConfigError(f"Invalid timeout value: timeout must be positive")
            except ValueError:
                raise ConfigError(f"Invalid timeout value: {value}")
        self._config[key] = value
        self.save()
        logger.debug(f"Set config {key} = {value}")

    def items(self) -> Dict[str, Any].items:
        """Return configuration items."""
        return self._config.items()

    def reset(self) -> None:
        """Reset configuration to empty state."""
        self._config = {}
        self.save()
        logger.debug("Configuration reset to empty state")

    def clear(self) -> None:
        """Clear configuration cache."""
        self.cache.clear()
        logger.debug("Configuration cache cleared")
