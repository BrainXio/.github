import json
import os
import pytest
from pathlib import Path
from src.brainxio.utils.cache import Cache
from src.brainxio.errors import CacheError

def test_cache_init(tmp_path: Path) -> None:
    """Test cache initialization."""
    cache_file = tmp_path / "cache.json"
    cache = Cache(cache_file)
    assert cache.get("test") is None

def test_cache_load(tmp_path: Path) -> None:
    """Test loading cache from disk."""
    cache_file = tmp_path / "cache.json"
    with cache_file.open("w") as f:
        json.dump({"key": "value"}, f)
    cache = Cache(cache_file)
    assert cache.get("key") == "value"

def test_cache_save(tmp_path: Path) -> None:
    """Test saving cache to disk."""
    cache_file = tmp_path / "cache.json"
    cache = Cache(cache_file)
    cache.set("key", "value")
    cache.save()
    with cache_file.open("r") as f:
        assert json.load(f) == {"key": "value"}

def test_cache_load_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test cache load raises CacheError on invalid JSON."""
    cache_file = tmp_path / "cache.json"
    with cache_file.open("w") as f:
        f.write("invalid json")
    with pytest.raises(CacheError, match="Failed to load cache"):
        Cache(cache_file)

def test_cache_save_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test cache save raises CacheError on write permission error."""
    cache_file = tmp_path / "cache.json"
    cache = Cache(cache_file)
    monkeypatch.setattr(os, "access", lambda x, y: False)
    with pytest.raises(CacheError, match="No write permission"):
        cache.save()

def test_cache_save_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test cache save raises CacheError on OSError."""
    cache_file = tmp_path / "cache.json"
    cache = Cache(cache_file)
    cache.set("key", "value")
    def mock_open(self, *args, **kwargs):
        raise OSError("Mocked file error")
    monkeypatch.setattr(Path, "open", mock_open)
    with pytest.raises(CacheError, match="Failed to save cache: Mocked file error"):
        cache.save()
