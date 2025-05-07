import json
import logging
import os
import pytest
from pathlib import Path
from src.brainxio.utils.logging import setup_logging, JSONFormatter
from src.brainxio.errors import LoggingError

def test_setup_logging(tmp_path: Path) -> None:
    """Test logging setup creates JSON log file."""
    os.environ["LOG_DIR"] = str(tmp_path / "logs")
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Test log")
    log_file = tmp_path / "logs" / "log.json"
    assert log_file.exists()
    with log_file.open() as f:
        log_entry = json.load(f)
        assert log_entry["message"] == "Test log"
        assert log_entry["level"] == "INFO"

def test_setup_logging_permission_error(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test logging setup raises LoggingError on permission error."""
    os.environ["LOG_DIR"] = str(tmp_path / "logs")
    (tmp_path / "logs").mkdir()
    monkeypatch.setattr(os, "access", lambda x, y: False)
    with pytest.raises(LoggingError, match="Failed to setup logging"):
        setup_logging()

def test_setup_logging_oserror(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Test logging setup raises LoggingError on OSError."""
    os.environ["LOG_DIR"] = str(tmp_path / "logs")
    (tmp_path / "logs").mkdir()
    def mock_filehandler(*args, **kwargs):
        raise OSError("Mocked file error")
    monkeypatch.setattr(logging, "FileHandler", mock_filehandler)
    with pytest.raises(LoggingError, match="Failed to setup logging"):
        setup_logging()

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
