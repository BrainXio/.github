import json
import logging
import os
import pytest
from pathlib import Path
from src.brainxio.utils.logging import setup_logging, JSONFormatter

def test_setup_logging(tmp_path: Path) -> None:
    """Test logging setup creates JSON log file."""
    os.environ["HOME"] = str(tmp_path)
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Test log")
    log_file = tmp_path / ".brainxio" / "log.json"
    assert log_file.exists()
    with log_file.open() as f:
        log_entry = json.load(f)
        assert log_entry["message"] == "Test log"
        assert log_entry["level"] == "INFO"

def test_json_formatter() -> None:
    """Test JSONFormatter formats logs correctly."""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test", level=logging.INFO, pathname="", lineno=0,
        msg="Test message", args=(), exc_info=None
    )
    output = formatter.format(record)
    log_entry = json.loads(output)
    assert log_entry["message"] == "Test message"
    assert log_entry["level"] == "INFO"
