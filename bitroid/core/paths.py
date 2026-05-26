import os
import sys
from pathlib import Path


APP_NAME = "BitroidDM"


def user_files_root() -> Path:
    return Path.home()


def app_data_dir() -> Path:
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home()))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    path = base / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path
