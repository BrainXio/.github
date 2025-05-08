import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional

from ..errors import CacheError

logger = logging.getLogger(__name__)


class Cache:
    """Cache management for BrainXio."""

    def __init__(self, cache_file: str):
        self.cache_file = Path(cache_file)
        self._cache: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load cache from file."""
        try:
            if self.cache_file.exists():
                with self.cache_file.open("r") as f:
                    self._cache = json.load(f)
                logger.debug(f"Loaded cache: {self._cache}")
        except json.JSONDecodeError as e:
            raise CacheError(f"Failed to load cache: {e}")
        except OSError as e:
            raise CacheError(f"Failed to load cache: {e}")

    def save(self) -> None:
        """Save cache to file."""
        try:
            if not os.access(self.cache_file.parent, os.W_OK):
                raise CacheError(f"No write permission for {self.cache_file.parent}")
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            with self.cache_file.open("w") as f:
                json.dump(self._cache, f, indent=2)
        except OSError as e:
            raise CacheError(f"Failed to save cache: {e}")

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """Get cache value by key."""
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set cache value."""
        self._cache[key] = value
        self.save()
        logger.debug(f"Set cache {key} = {value}")

    def clear(self) -> None:
        """Clear cache."""
        self._cache = {}
        self.save()
        logger.debug("Cache cleared")
