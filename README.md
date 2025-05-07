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
- `config set <key> <value>`: Set a configuration key (e.g., `log_dir /new/log`).
- `clear-cache`: Clear the cache file.
- `reset-config`: Reset configuration to defaults.

## Testing
Run tests with coverage: `pytest --cov=src/brainxio`

## License
The Unlicense - see `LICENSING.md` for details.
