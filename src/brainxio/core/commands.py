import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List
import importlib.util
import importlib.metadata
import sys

logger = logging.getLogger(__name__)
from ..utils.tasks import run_task, run_tasks_parallel
from ..utils.config import Config
from ..errors import BrainXioError


class Command(ABC):
    """Base class for commands."""

    def __init__(self, config: Config):
        self.config = config

    @abstractmethod
    def execute(self, args: Dict[str, Any]) -> None:
        pass


class ConfigCommand(Command):
    """Command to manage configuration settings."""

    def execute(self, args: Dict[str, Any]) -> None:
        key = args.get("key")
        value = args.get("value")
        if key and value:
            self.config.set(key, value)
            print(f"Set {key} = {value}")
            logger.info(f"Set configuration: {key} = {value}")
        elif key:
            print(f"{key} = {self.config.get(key)}")
        else:
            for k, v in self.config.items():
                print(f"{k} = {v}")


class ClearCacheCommand(Command):
    """Command to clear cache."""

    def execute(self, args: Dict[str, Any]) -> None:
        self.config.clear()
        print("Cache cleared successfully")
        logger.info("Cache cleared successfully")


class ResetConfigCommand(Command):
    """Command to reset configuration to defaults."""

    def execute(self, args: Dict[str, Any]) -> None:
        self.config.reset()
        print("Configuration reset to defaults")
        logger.info("Configuration reset to defaults")


class RunTaskCommand(Command):
    """Command to run tasks."""

    def execute(self, args: Dict[str, Any]) -> None:
        task_names = args.get("task_names", [])
        params = args.get("params", {})
        parallel = args.get("parallel", False)
        if not task_names:
            raise BrainXioError("At least one task name required")
        task_dir = Path(self.config.get("task_dir", Path.home() / ".brainxio" / "tasks"))
        max_retries = int(self.config.get("max_retries", 3))
        timeout = int(self.config.get("timeout", 60))
        if parallel:
            run_tasks_parallel(task_dir, task_names, params, max_retries, timeout)
        else:
            for task_name in task_names:
                logger.info(f"Running task: {task_name}")
                task_result, task_exception = run_task(task_dir, task_name, params, max_retries=max_retries, timeout=timeout)
                if task_exception:
                    raise task_exception
                print(f"Task {task_name} executed successfully")


class CommandRegistry:
    """Registry for managing commands."""

    def __init__(self, config: Config):
        self.config = config
        self.commands: Dict[str, Command] = {}
        self.register_command("config", ConfigCommand(config))
        self.register_command("clear-cache", ClearCacheCommand(config))
        self.register_command("reset-config", ResetConfigCommand(config))
        self.register_command("run-task", RunTaskCommand(config))
        self.load_plugins()

    def register_command(self, name: str, command: Command) -> None:
        self.commands[name] = command

    def execute(self, name: str, args: Dict[str, Any]) -> None:
        if name not in self.commands:
            raise BrainXioError(f"Unknown command: {name}")
        self.commands[name].execute(args)

    def load_plugins(self) -> None:
        """Load plugins from entry_points and plugin_dir."""
        # Load from entry_points
        try:
            for plugin in importlib.metadata.entry_points().select(group="brainxio.plugins"):
                try:
                    plugin_module = plugin.load()
                    if hasattr(plugin_module, "register_command"):
                        plugin_module.register_command(self)
                    else:
                        logger.warning(f"Plugin {plugin.name} missing register_command function")
                except Exception as e:
                    logger.error(f"Failed to load plugin {plugin.name}: {e}")
        except Exception as e:
            logger.error(f"Error discovering plugins: {e}")

        # Load from plugin_dir
        plugin_dir = self.config.get("plugin_dir")
        if plugin_dir:
            plugin_dir = Path(plugin_dir)
            if plugin_dir.exists():
                sys.path.append(str(plugin_dir))
                for plugin_file in plugin_dir.glob("*.py"):
                    plugin_name = plugin_file.stem
                    try:
                        spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
                        if spec and spec.loader:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                            if hasattr(module, "register_command"):
                                module.register_command(self)
                            else:
                                logger.warning(f"Plugin {plugin_name} missing register_command function")
                        else:
                            logger.error(f"Failed to load plugin {plugin_name}: Invalid module spec")
                    except Exception as e:
                        logger.error(f"Failed to load plugin {plugin_name}: {e}")
                sys.path.remove(str(plugin_dir))
