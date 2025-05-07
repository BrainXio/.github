import logging
import pytest
from src.brainxio.core.main import main

def test_main(caplog: pytest.LogCaptureFixture) -> None:
    """Test main CLI entry point logs and runs."""
    caplog.set_level(logging.INFO)
    main()
    assert "Starting BrainXio CLI" in caplog.text
