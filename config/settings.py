from pathlib import Path

# Deprecated: Use Config class from src.brainxio.utils.config
CONFIG_FILE = Path.home() / ".brainxio" / "config.yaml"
LOG_DIR = Path.home() / ".brainxio"
LOG_FILE = LOG_DIR / "log.json"
CACHE_FILE = LOG_DIR / "cache.json"
