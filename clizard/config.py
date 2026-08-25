"""Settings persistence for GenericCLI.

Persisted settings live in the project-local ``.clizard/settings.json``
(not a global ``~/.config`` path), so each repo keeps its own state.
"""
import json
from pathlib import Path

CLIZARD_DIRNAME = ".clizard"
SETTINGS_FILENAME = "settings.json"


def local_settings_path(base_path=".") -> Path:
    """Return ``{base}/.clizard/settings.json``."""
    return Path(base_path).resolve() / CLIZARD_DIRNAME / SETTINGS_FILENAME


class Config:
    """Simple JSON-backed settings store.

    settings dict holds arbitrary key/values (model, path, theme, etc).
    By default the file is written under the project-local ``.clizard/``
    directory (see ``local_settings_path``).
    """

    def __init__(
        self,
        app_name: str,
        defaults: dict = None,
        config_path: str = None,
        base_path: str = None,
    ):
        self.app_name = app_name
        self.defaults = defaults or {}
        if config_path:
            self.path = Path(config_path)
        else:
            # Prefer an explicit base_path, then a "path" key in defaults
            # (injected by build_cli), otherwise the current working directory.
            base = base_path
            if base is None and self.defaults.get("path"):
                base = self.defaults["path"]
            if base is None:
                base = "."
            self.path = local_settings_path(base)
        self.settings = dict(self.defaults)
        self.loaded_from_disk = False
        self.load()

    def load(self):
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    data = json.load(f)
                self.settings.update(data)
                self.loaded_from_disk = True
            except (json.JSONDecodeError, OSError):
                pass
        return self.settings

    def save(self):
        parent = self.path.parent
        # A legacy top-level ``.clizard`` *file* blocks creating the directory.
        if parent.name == CLIZARD_DIRNAME and parent.exists() and parent.is_file():
            try:
                parent.unlink()
            except OSError:
                pass
        parent.mkdir(parents=True, exist_ok=True)
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

    def reset(self):
        """Delete the persisted config file and restore in-memory settings to defaults."""
        if self.path.exists():
            try:
                self.path.unlink()
            except OSError:
                pass
        self.settings = dict(self.defaults)
        self.loaded_from_disk = False
