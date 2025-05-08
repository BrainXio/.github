import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)
from .commands import CommandRegistry
from ..utils.config import Config
from ..utils.cache import Cache


def parse_args(args: Optional[List[str]] = None) -> Dict[str, any]:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="BrainXio CLI for automation and AI tasks", exit_on_error=False)
    parser.add_argument("--version", action="version", version="BrainXio 0.1.0")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration")
    config_parser.add_argument("action", choices=["show", "set"], help="Action to perform")
    config_parser.add_argument("key", nargs="?", help="Configuration key (e.g., log_dir, cache_dir)")
    config_parser.add_argument("value", nargs="?", help="Configuration value")

    # Clear-cache command
    subparsers.add_parser("clear-cache", help="Clear the cache file")

    # Reset-config command
    subparsers.add_parser("reset-config", help="Reset configuration to defaults")

    # Run-task command
    run_task_parser = subparsers.add_parser("run-task", help="Run one or more tasks")
    run_task_parser.add_argument("task_names", nargs="+", help="Names of tasks to run")
    run_task_parser.add_argument("--param", action="append", default=[], help="Task parameters in key=value format", dest="param")
    run_task_parser.add_argument("--parallel", action="store_true", help="Run tasks in parallel")

    try:
        parsed_args = parser.parse_args(args)
    except argparse.ArgumentError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)
    args_dict = vars(parsed_args)

    # Validate parameters for run-task
    if args_dict.get("command") == "run-task":
        params = {}
        for param in args_dict.get("param", []):
            if "=" not in param:
                print(f"Invalid parameter format: {param}; expected key=value", file=sys.stderr)
                sys.exit(1)
            key, value = param.split("=", 1)
            params[key] = value
        args_dict["params"] = params

    logger.debug(f"CLI arguments: {args_dict}")
    return args_dict


def main() -> None:
    """Main CLI entry point."""
    logger.info("Starting BrainXio CLI")
    args = parse_args()
    config_file = Path.home() / ".brainxio" / "config.yaml"
    cache = Cache(Path.home() / ".brainxio" / "cache.json")
    config = Config(config_file, cache)
    registry = CommandRegistry(config)

    command = args.get("command")
    if command is None:
        print("BrainXio CLI version 0.1.0", file=sys.stderr)
        print("Use --help for usage information", file=sys.stderr)
        sys.exit(1)

    try:
        registry.execute(command, args)
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":  # pragma: no cover
    main()
