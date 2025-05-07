from abc import ABC, abstractmethod
import logging
import importlib.util
from pathlib import Path
from typing import Any, Dict
from ..utils.cache import Cache
from ..utils.config import Config
from ..utils.tasks import run_task
from ..errors import BrainXioError

logger = logging.getLogger(__name__)

class Command(ABC):
    """Abstract base class for CLI commands."""
    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> None:
        pass

class ConfigCommand(Command):
    """Handles config show and set commands."""
    def __init__(self, config: Config) -> None:
        self.config = config

    def execute(self, args: Dict[str, Any]) -> None:
        if args["action"] == "show":
            print(self.config.get("log_dir", "No log_dir set"))
        elif args["action"] == "set" and args.get("key") and args.get("value"):
            self.config.set(args["key"], args["value"])
            print(f"Set {args['key']} to {args['value']}")

class ClearCacheCommand(Command):
    """Clears the cache file."""
    def __init__(self, cache: Cache) -> None:
        self.cache = cache

    def execute(self, args: Dict[str, Any]) -> None:
        self.cache._cache.clear()
        self.cache.save()
        logger.info("Cache cleared")
        print("Cache cleared successfully")

class ResetConfigCommand(Command):
    """Resets configuration to defaults."""
    def __init__(self, config: Config) -> None:
        self.config = config

    def execute(self, args: Dict[str, Any]) -> None:
        self.config._config = {"log_dir": str(Path.home() / ".brainxio"), "cache_dir": str(Path.home() / ".brainxio")}
        self.config._cache.set("config", self.config._config)
        self.config._cache.save()
        logger.info("Configuration reset to defaults")
        print("Configuration reset to defaults")

class RunTaskCommand(Command):
    """Runs a user-defined task script."""
    def __init__(self, config: Config) -> None:
        self.config = config

    def execute(self, args: Dict[str, Any]) -> None:
        task_name = args.get("task_name")
        if not task_name:
            raise BrainXioError("Task name required")
        task_dir = Path(self.config.get("task_dir", Path.home() / ".brainxio" / "tasks"))
        logger.info(f"Running task: {task_name}")
        run_task(task_dir, task_name)
        print(f"Task {task_name} executed successfully")

class CommandRegistry:
    """Manages CLI command registration and execution."""
    def __init__(self) -> None:
        self.commands: Dict[str, Command] = {}

    def register(self, name: str, command: Command) -> None:
        self.commands[name] = command

    def execute(self, name: str, args: Dict[str, Any]) -> None:
        command = self.commands.get(name)
        if not command:
            raise BrainXioError(f"Unknown command: {name}")
        command.execute(args)

    def load_plugins(self, plugin_dir: Path, config: Config, cache: Cache) -> None:
        """Load plugins from the plugin directory."""
        if not plugin_dir.exists():
            return
        for plugin_file in plugin_dir.glob("*.py"):
            try:
                spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
                if spec is None or spec.loader is None:
                    logger.warning(f"Failed to load plugin: {plugin_file}")
                    continue
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                if hasattr(module, "register_command"):
                    command = module.register_command(config, cache)
                    self.register(plugin_file.stem, command)
                    logger.info(f"Loaded plugin: {plugin_file.stem}")
                else:
                    logger.warning(f"Plugin {plugin_file.stem} missing register_command function")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_file.stem}: {e}")
