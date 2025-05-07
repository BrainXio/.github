import json
import os
from pathlib import Path
from typing import Any, Dict
from ..errors import CacheError

class Cache:
    """Manages in-memory and disk-based caching."""
    def __init__(self, cache_file: Path) -> None:
        self._cache_file = cache_file
        self._cache: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        """Load cache from disk if it exists."""
        try:
            if self._cache_file.exists():
                with self._cache_file.open("r") as f:
                    self._cache = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise CacheError(f"Failed to load cache: {e}") from e

    def save(self) -> None:
        """Save cache to disk."""
        try:
            if not os.access(self._cache_file.parent, os.W_OK):
                raise CacheError(f"No write permission for {self._cache_file.parent}")
            self._cache_file.parent.mkdir(exist_ok=True)
            with self._cache_file.open("w") as f:
                json.dump(self._cache, f, indent=2)
        except OSError as e:
            raise CacheError(f"Failed to save cache: {e}") from e

    def get(self, key: str, default: Any = None) -> Any:
        """Get value from cache."""
        return self._cache.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set value in cache."""
        self._cache[key] = value
