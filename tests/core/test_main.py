import logging
import pytest
import sys
from src.brainxio.core.main import main, parse_args

def test_main(caplog: pytest.LogCaptureFixture, capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test main CLI entry point logs and outputs version."""
    monkeypatch.setattr(sys, "argv", ["brainxio"])
    caplog.set_level(logging.INFO)
    main()
    captured = capsys.readouterr()
    assert "Starting BrainXio CLI" in caplog.text
    assert "CLI arguments: {'command': None}" in caplog.text
    assert "BrainXio CLI v0.1.0" in captured.out

def test_parse_args_version(capsys: pytest.CaptureFixture) -> None:
    """Test --version argument displays version and exits."""
    with pytest.raises(SystemExit):
        parse_args(["--version"])
    captured = capsys.readouterr()
    assert "BrainXio 0.1.0" in captured.out

def test_parse_args_help(capsys: pytest.CaptureFixture) -> None:
    """Test --help argument displays usage and exits."""
    with pytest.raises(SystemExit):
        parse_args(["--help"])
    captured = capsys.readouterr()
    assert "BrainXio CLI for automation and AI tasks" in captured.out

def test_config_show(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test config show command displays log_dir."""
    monkeypatch.setattr(sys, "argv", ["brainxio", "config", "show"])
    main()
    captured = capsys.readouterr()
    assert ".brainxio" in captured.out

def test_config_set(capsys: pytest.CaptureFixture, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test config set command updates configuration."""
    monkeypatch.setattr(sys, "argv", ["brainxio", "config", "set", "log_dir", "/new/log"])
    main()
    captured = capsys.readouterr()
    assert "Set log_dir to /new/log" in captured.out
