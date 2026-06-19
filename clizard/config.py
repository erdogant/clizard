"""Settings persistence for GenericCLI."""
import json
import os
from pathlib import Path

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "clizard"


class Config:
    """Simple JSON-backed settings store.

    settings dict holds arbitrary key/values (model, path, theme, etc).
    """

    def __init__(self, app_name: str, defaults: dict = None, config_path: str = None):
        self.app_name = app_name
        self.defaults = defaults or {}
        if config_path:
            self.path = Path(config_path)
        else:
            self.path = DEFAULT_CONFIG_DIR / f"{app_name}.json"
        self.settings = dict(self.defaults)
        self.load()

    def load(self):
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    data = json.load(f)
                self.settings.update(data)
            except (json.JSONDecodeError, OSError):
                pass
        return self.settings

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.settings, f, indent=2)

    def get(self, key, fallback=None):
        return self.settings.get(key, fallback)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def update_from_args(self, args_dict: dict):
        """Override settings with non-None values from parsed CLI args."""
        for k, v in args_dict.items():
            if v is not None:
                self.settings[k] = v
