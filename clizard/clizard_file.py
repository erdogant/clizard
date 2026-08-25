"""Read/write project-local clizard metadata.

Metadata (ascii_art, app_name, docs_url, accent_color, tips, updates) lives
in ``.clizard/meta.json``.  Settings persistence uses ``.clizard/settings.json``
(see config.py).

Legacy support: if an old top-level ``.clizard`` *file* exists (from earlier
versions), it is still read.  New writes always go to ``.clizard/meta.json``.
"""
import json
from pathlib import Path

DEFAULT_ASCII = r"""
  .-.
 |o o|
 | = |
/|___|\
"""

CLIZARD_DIRNAME = ".clizard"
META_FILENAME = "meta.json"
LEGACY_FILENAME = ".clizard"  # old single-file layout


def _meta_path(repo_path=".") -> Path:
    return Path(repo_path) / CLIZARD_DIRNAME / META_FILENAME


def _legacy_path(repo_path=".") -> Path:
    return Path(repo_path) / LEGACY_FILENAME


def load_clizard_file(repo_path="."):
    """Return the parsed metadata dict, or {} if absent/invalid.

    Prefers ``.clizard/meta.json``; falls back to a legacy top-level
    ``.clizard`` file when the directory layout is not present yet.
    """
    meta = _meta_path(repo_path)
    if meta.exists() and meta.is_file():
        try:
            with open(meta, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    legacy = _legacy_path(repo_path)
    # Only treat as legacy file if it is a regular file (not our directory).
    if legacy.exists() and legacy.is_file():
        try:
            with open(legacy, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

    return {}


def _ensure_clizard_dir(repo_path=".") -> Path:
    """Ensure ``.clizard/`` exists as a directory.

    If a legacy top-level ``.clizard`` *file* is present, remove it first so
    the directory can be created.
    """
    parent = Path(repo_path) / CLIZARD_DIRNAME
    legacy = _legacy_path(repo_path)
    if legacy.exists() and legacy.is_file():
        try:
            legacy.unlink()
        except OSError:
            pass
    parent.mkdir(parents=True, exist_ok=True)
    return parent


def save_clizard_file(data: dict, repo_path="."):
    """Write metadata to ``.clizard/meta.json`` (creates the directory)."""
    _ensure_clizard_dir(repo_path)
    path = _meta_path(repo_path)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    return path


def ensure_clizard_file(repo_path=".", create=True, **overrides):
    """Return metadata, merged with sane defaults if absent.

    If `create` is True (default) and no metadata exists yet, one is
    written under ``.clizard/meta.json``.  If `create` is False, the
    defaults are returned without touching disk -- used by callers
    (e.g. the interactive clizard CLI) that should work fine with no
    metadata file present.
    """
    existing = load_clizard_file(repo_path)
    if existing:
        return existing

    data = {
        "app_name": None,       # None -> auto from pyproject/git
        "ascii_art": DEFAULT_ASCII,
        "docs_url": None,       # None -> auto from pyproject, else docs/index.html
        "accent_color": "#d97757",
        "tips": ["/wizard", "/run", "/settings", "/reset", "/home", "/help"],
        "updates": [],
    }
    data.update(overrides)
    if create:
        save_clizard_file(data, repo_path)
    return data
