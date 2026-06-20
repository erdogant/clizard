"""Read/write the project-local .clizard metadata file.

This stores anything that can't be auto-discovered from git/pyproject:
ascii_art, app_name override, docs_url override, accent_color, tips, etc.
"""
import json
from pathlib import Path

DEFAULT_ASCII = r"""
  .-.
 |o o|
 | = |
/|___|\
"""

CLIZARD_FILENAME = ".clizard"


def load_clizard_file(repo_path="."):
    """Return the parsed .clizard JSON dict, or {} if absent/invalid."""
    path = Path(repo_path) / CLIZARD_FILENAME
    if not path.exists():
        return {}
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_clizard_file(data: dict, repo_path="."):
    path = Path(repo_path) / CLIZARD_FILENAME
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def ensure_clizard_file(repo_path=".", **overrides):
    """Create a .clizard file with sane defaults if one doesn't exist yet."""
    path = Path(repo_path) / CLIZARD_FILENAME
    if path.exists():
        return load_clizard_file(repo_path)

    data = {
        "app_name": None,       # None -> auto from pyproject/git
        "ascii_art": DEFAULT_ASCII,
        "docs_url": None,       # None -> auto from pyproject, else docs/index.html
        "accent_color": "#d97757",
        "tips": ["/wizard", "/run", "/settings", "/help"],
        "updates": [],
    }
    data.update(overrides)
    save_clizard_file(data, repo_path)
    return data
