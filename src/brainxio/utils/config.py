import logging
import yaml
import re
from pathlib import Path
from typing import Dict, Any, Optional, Union

logger = logging.getLogger(__name__)


class Config:
    """Configuration management for BrainXio."""

    def __init__(self, config_file: Union[str, Path], cache: 'Cache'):
        self.config_file = Path(config_file)
        self.cache = cache
        self._config: Dict[str, Any] = {}
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
        except (yaml.YAMLError, OSError) as e:
            logger.warning(f"Failed to load config: {e}")
            self._config = {}

    def save(self) -> None:
        """Save configuration to file and cache."""
        try:
            with self.config_file.open("w") as f:
                yaml.safe_dump(self._config, f)
            self.cache.set("config", self._config)
            self.cache.save()
        except (yaml.YAMLError, OSError) as e:
            logger.warning(f"Failed to save config: {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get configuration value by key."""
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value and save."""
        if not re.match(r"^[a-z][a-z0-9_-]*$", key):
            raise ValueError(f"Invalid config key: {key}")
        if key == "plugin_dir":
            value = Path(value).expanduser().resolve()
        elif key == "max_retries":
            try:
                value = int(value)
                if value < 0:
                    raise ValueError
            except ValueError:
                raise ValueError(f"Invalid max_retries: {value}")
        self._config[key] = value
        self.save()
        logger.debug(f"Set config {key} = {value}")

    def items(self) -> Dict[str, Any].items:
        """Return configuration items."""
        return self._config.items()

    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = {}
        self.save()
        logger.debug("Configuration reset to defaults")

    def clear(self) -> None:
        """Clear configuration cache."""
        self.cache.clear()
        logger.debug("Configuration cache cleared")
