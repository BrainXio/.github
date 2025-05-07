import json
import logging
import os
from pathlib import Path

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
    """Configure JSON logging to $HOME/.brainxio/log.json."""
    log_dir = Path.home() / ".brainxio"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "log.json"

    handler = logging.FileHandler(log_file)
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
