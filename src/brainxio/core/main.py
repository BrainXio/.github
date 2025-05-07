import argparse
import logging
import sys
from config import settings
from ..utils.cache import Cache
from ..utils.config import Config
from ..utils.logging import setup_logging

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
    return parser.parse_args(args)

def main() -> None:
    """Entry point for BrainXio CLI."""
    setup_logging()
    cache = Cache(settings.CACHE_FILE)
    config = Config(settings.CONFIG_FILE, cache)
    logger.info("Starting BrainXio CLI", extra={"cache_hit": cache.get("last_command") is not None})
    args = parse_args()
    cache.set("last_command", vars(args))
    cache.save()
    if args.command == "config":
        if args.action == "show":
            print(config.get("log_dir", "No log_dir set"))
        elif args.action == "set" and args.key and args.value:
            config.set(args.key, args.value)
            print(f"Set {args.key} to {args.value}")
    else:
        logger.info(f"CLI arguments: {vars(args)}")
        print("BrainXio CLI v0.1.0")

if __name__ == "__main__":  # pragma: no cover
    main()
