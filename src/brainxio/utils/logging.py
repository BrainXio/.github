import json
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from ..errors import LoggingError

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module
        }
        return json.dumps(log_entry)

def setup_logging() -> None:
    """Configure JSON logging to path from .env or default."""
    load_dotenv()
    log_dir = Path(os.getenv("LOG_DIR", Path.home() / ".brainxio"))
    log_file = log_dir / "log.json"

    try:
        if not os.access(log_dir.parent, os.W_OK):
            raise LoggingError(f"No write permission for {log_dir.parent}")
        log_dir.mkdir(exist_ok=True)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(JSONFormatter())

        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
    except (OSError, PermissionError) as e:
        raise LoggingError(f"Failed to setup logging: {e}") from e
