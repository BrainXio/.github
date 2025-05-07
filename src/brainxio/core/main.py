import argparse
import logging
import sys
from config import settings
from ..utils.cache import Cache
from ..utils.config import Config
from ..utils.logging import setup_logging
from ..core.commands import CommandRegistry, ConfigCommand, ClearCacheCommand, ResetConfigCommand, RunTaskCommand

logger = logging.getLogger(__name__)

def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="BrainXio CLI for automation and AI tasks")
    parser.add_argument("--version", action="version", version="BrainXio 0.1.0")
    subparsers = parser.add_subparsers(dest="command")
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("action", choices=["show", "set"])
    config_parser.add_argument("key", nargs="?", help="Config key to set")
    config_parser.add_argument("value", nargs="?", help="Config value to set")
    subparsers.add_parser("clear-cache", help="Clear the cache")
    subparsers.add_parser("reset-config", help="Reset configuration to defaults")
    task_parser = subparsers.add_parser("run-task", help="Run a user-defined task")
    task_parser.add_argument("task_name", help="Name of the task to run")
    return parser.parse_args(args)

def main() -> None:
    """Entry point for BrainXio CLI."""
    setup_logging()
    cache = Cache(settings.CACHE_FILE)
    config = Config(settings.CONFIG_FILE, cache)
    registry = CommandRegistry()
    registry.register("config", ConfigCommand(config))
    registry.register("clear-cache", ClearCacheCommand(cache))
    registry.register("reset-config", ResetConfigCommand(config))
    registry.register("run-task", RunTaskCommand(config))
    logger.info("Starting BrainXio CLI", extra={"cache_hit": cache.get("last_command") is not None})
    args = parse_args()
    cache.set("last_command", vars(args))
    cache.save()
    if args.command:
        registry.execute(args.command, vars(args))
    else:
        logger.info(f"CLI arguments: {vars(args)}")
        print("BrainXio CLI v0.1.0")

if __name__ == "__main__":  # pragma: no cover
    main()
