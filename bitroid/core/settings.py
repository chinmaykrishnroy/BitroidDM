import json
from pathlib import Path

from bitroid.core.paths import app_data_dir, user_files_root


DEFAULT_SETTINGS = {
    "file_manager": {
        "current_dir": str(user_files_root()),
        "sort_by": "Name",
        "show_hidden": False,
    },
    "media_player": {
        "volume": 60,
        "playback_rate": 1.0,
        "repeat_mode": "off",
        "shuffle": False,
        "visible": True,
    },
    "torrent": {
        "download_dir": str(Path.home() / "Downloads"),
        "poll_interval_ms": 1000,
        "active_filter": "all",
        "total_downloaded_bytes": 0,
        "enable_dht": True,
        "enable_lsd": True,
        "enable_upnp": True,
        "enable_natpmp": True,
        "listen_interfaces": "0.0.0.0:6881,[::]:6881",
    },
    "appearance": {
        "theme": "dark",
    },
}


def _deep_merge(defaults, saved):
    result = dict(defaults)
    for key, value in saved.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class AppSettings:
    def __init__(self, path: Path | None = None):
        self.path = path or app_data_dir() / "settings.json"
        self.data = _deep_merge(DEFAULT_SETTINGS, self._read())

    def _read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return data if isinstance(data, dict) else {}
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return {}

    def get(self, section, key, default=None):
        return self.data.get(section, {}).get(key, default)

    def set(self, section, key, value):
        self.data.setdefault(section, {})[key] = value

    def save(self):
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, indent=4)
                file.write("\n")
            temp_path.replace(self.path)
            return True
        except OSError:
            return False
