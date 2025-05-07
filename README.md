# BrainXio

A modular, open-source Python CLI for automation and AI-driven tasks.

## Installation
1. Clone the repository: `git clone <repo-url>`
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage
Run the CLI: `python src/brainxio/core/main.py`

### Commands
- `--version`: Display the BrainXio version.
- `config show`: Display the current log_dir configuration.
- `config set <key> <value>`: Set a configuration key (allowed keys: `log_dir`, `cache_dir`, `task_dir`, `plugin_dir`; e.g., `log_dir /new/log`).
- `clear-cache`: Clear the cache file.
- `reset-config`: Reset configuration to defaults.
- `run-task <task_name> [<task_name>...] [--param key=value]...`: Run one or more Python task scripts from the task directory (default: `$HOME/.brainxio/tasks/`) with optional parameters.

### Plugins
Extend BrainXio by adding plugins to the plugin directory (default: `$HOME/.brainxio/plugins/`). A plugin is a Python file defining a `register_command` function that returns a `Command` instance. Example:
```python
# test_plugin.py
from src.brainxio.core.commands import Command
class TestPluginCommand(Command):
    def execute(self, args):
        print('Plugin executed')
def register_command(config, cache):
    return TestPluginCommand()
```
Set the plugin directory with `config set plugin_dir /custom/plugins`.

## Testing
Run tests with coverage: `pytest --cov=src/brainxio`

## Development
Use the Makefile for common tasks:
- `make install`: Install dependencies with Poetry.
- `make test`: Run tests with pytest.
- `make lock`: Update Poetry lock file.
- `make update`: Apply cycle.json with experimental-f2c.
- `make cycle`: Run the full development cycle (update, lock, install, test).

## License
The Unlicense - see `LICENSING.md` for details.
