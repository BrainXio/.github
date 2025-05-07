from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()
LOG_DIR = Path(os.getenv("LOG_DIR", Path.home() / ".brainxio"))
LOG_FILE = LOG_DIR / "log.json"
