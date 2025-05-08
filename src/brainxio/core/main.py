import logging
import argparse
import sys
from typing import Optional, Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)
from .commands import CommandRegistry, Command
from ..utils.logging import setup_logging
from ..utils.config import Config
from ..utils.cache import Cache


class Settings:
    CONFIG_FILE: Path = Path.home() / ".brainxio" / "config.yaml"
    CACHE_FILE: Path = Path.home() / ".brainxio" / "cache.json"


settings = Settings()


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="BrainXio CLI", prog="brainxio")
    parser.add_argument("--version", action="version", version="0.1.0")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("action", choices=["show", "set"], default="show", nargs="?", help="Action to perform")
    config_parser.add_argument("key", nargs="?", help="Configuration key")
    config_parser.add_argument("value", nargs="?", help="Configuration value")

    subparsers.add_parser("clear-cache", help="Clear cache")
    subparsers.add_parser("reset-config", help="Reset configuration to defaults")

    run_task_parser = subparsers.add_parser("run-task", help="Run tasks")
    run_task_parser.add_argument("task_names", nargs="+", help="Names of tasks to run")
    run_task_parser.add_argument("--param", action="append", help="Task parameter in key=value format", default=[])
    run_task_parser.add_argument("--parallel", action="store_true", help="Run tasks in parallel")

    return parser.parse_args(args)


def main() -> None:
    """Entry point for BrainXio CLI."""
    setup_logging()
    cache = Cache(settings.CACHE_FILE)
    config = Config(settings.CONFIG_FILE, cache)
    registry = CommandRegistry(config)
    args = parse_args()
    logger.info("Starting BrainXio CLI")

    if not args.command:
        print(f"BrainXio CLI version 0.1.0")
        return

    params: Dict[str, Any] = {}
    if hasattr(args, "param"):
        for param in args.param:
            try:
                key, value = param.split("=", 1)
                params[key] = value
            except ValueError:
                logger.warning(f"Invalid parameter format: {param}")

    registry.execute(args.command, vars(args) | {"params": params})


if __name__ == "__main__":
    main()
