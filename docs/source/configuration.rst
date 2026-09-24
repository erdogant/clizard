configuration
==============

The :mod:`clizard.clizard_file` module manages project-specific display metadata in a lightweight JSON file. It lives under ``.clizard/meta.json`` at the repository root and contains information such as the application name, documentation URL, ASCII art banner, accent colour, tip commands, and an updates log. A separate file, ``.clizard/settings.json``, stores the persisted runtime settings (managed by :class:`clizard.config.Config`); the two files are independent.

.. note::

   Earlier versions of clizard stored metadata in a single top-level ``.clizard`` file. The current layout uses a ``.clizard/`` directory. The module handles legacy single-file layouts transparently on read, and always writes to ``.clizard/meta.json``.

The module exposes three helper functions — :func:`load_clizard_file`, :func:`save_clizard_file`, and :func:`ensure_clizard_file` — plus a :func:`ensure_clizard_file` variant with a ``create`` flag that controls whether a missing file is written to disk. All three operate on plain dictionaries and perform no semantic validation beyond JSON decoding. This separation of concerns lets higher-level code (the CLI shell, documentation generators, CI pipelines) focus on their domain while delegating persistence to a tested, fault-tolerant layer.

The functions are intentionally forgiving: file-access errors are caught and an empty dictionary is returned, so downstream code can always merge the result with its own defaults without wrapping every call in ``try``/``except``. When something goes wrong, a warning is logged via the standard library's :mod:`logging` system.


load_clizard_file
-----------------

Reads ``.clizard/meta.json`` from the specified repository directory. Falls back to a legacy top-level ``.clizard`` file if the directory layout is not present. Returns an empty dict on any error (missing file, permission error, invalid JSON) so that callers always receive a mapping object.

.. list-table:: Parameters for :func:`load_clizard_file`
   :widths: 20 10 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - repo_path
     - str
     - Path to the repository root. Defaults to ``"."`` (current working directory).

**Returns:** ``dict`` — the parsed metadata, or ``{}`` on failure.

.. code-block:: python

   from clizard.clizard_file import load_clizard_file

   # Load metadata from the current repository.
   meta = load_clizard_file(".")
   print(meta.get("app_name"))   # "MyTool" or None if not set
   print(meta.get("accent_color"))  # "#d97757" or None if not set

   # Load from a specific path.
   meta = load_clizard_file("/path/to/myproject")


save_clizard_file
-----------------

Serialises a dictionary to JSON and writes it to ``.clizard/meta.json``. Creates the ``.clizard/`` directory if it does not exist. If a legacy top-level ``.clizard`` *file* is present, it is removed first so the directory can be created. Overwrites any existing ``meta.json`` without prompting.

The function expects the input dictionary to contain only JSON-serialisable types (strings, numbers, booleans, lists, nested dicts). Non-serialisable types will raise a ``TypeError`` from ``json.dumps`` — this is intentional, as silently dropping data would be more harmful than an explicit error.

.. list-table:: Parameters for :func:`save_clizard_file`
   :widths: 20 10 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - data
     - dict
     - Metadata dictionary to persist. Must contain only JSON-serialisable values.
   * - repo_path
     - str
     - Repository root where ``.clizard/meta.json`` will be written. Defaults to ``"."``.

**Returns:** :class:`pathlib.Path` — the resolved path of the written file.

.. code-block:: python

   from clizard.clizard_file import save_clizard_file

   meta = {
       "app_name": "BN Pipeline",
       "accent_color": "#5b9bd5",
       "docs_url": "https://erdogant.github.io/bnlearn/",
       "tips": ["/wizard", "/run", "/settings", "/reset", "/help"],
       "updates": [
           "v0.3.0 — Added Snakemake config support",
           "v0.2.1 — Fixed discretization edge cases",
       ],
   }
   path = save_clizard_file(meta, repo_path=".")
   print(f"Metadata written to {path}")
   # Metadata written to /your/repo/.clizard/meta.json


ensure_clizard_file
-------------------

The most commonly used helper. Checks whether a ``meta.json`` file already exists; if it does, returns its contents. If not, constructs a default metadata dictionary, optionally merges caller-supplied keyword overrides, and — when ``create=True`` — writes the result to disk.

This is the function used by ``build_cli`` at startup. Passing ``create=False`` (the default when running the interactive shell) means clizard works in a fresh repository with no files on disk at all.

Default values applied when no ``meta.json`` is found:

.. code-block:: python

   {
       "app_name": None,          # auto-derived from pyproject.toml or git remote
       "ascii_art": "  .-.\n |o o|\n | = |\n/|___|\\",
       "docs_url": None,          # auto-derived from pyproject.toml urls
       "accent_color": "#d97757",
       "tips": ["/wizard", "/run", "/settings", "/reset", "/home", "/help"],
       "updates": [],
   }

.. list-table:: Parameters for :func:`ensure_clizard_file`
   :widths: 20 10 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - repo_path
     - str
     - Repository root to check. Defaults to ``"."``.
   * - create
     - bool
     - Write defaults to disk if no file is found. Defaults to ``True``.
   * - **overrides
     - dict
     - Keyword arguments that override specific default values before saving.

**Returns:** ``dict`` — the final metadata dictionary (from disk or freshly constructed).

.. code-block:: python

   from clizard.clizard_file import ensure_clizard_file

   # Use defaults, but override the app name and accent colour.
   # Creates .clizard/meta.json if it does not exist.
   meta = ensure_clizard_file(
       repo_path=".",
       app_name="BN Pipeline",
       accent_color="#5b9bd5",
   )
   print(meta["app_name"])     # "BN Pipeline"
   print(meta["accent_color"]) # "#5b9bd5"

   # Read-only mode: return defaults without touching disk.
   meta = ensure_clizard_file(repo_path=".", create=False)


Configuration reference
-----------------------

The full set of keys recognised in ``.clizard/meta.json``:

.. list-table::
   :widths: 20 15 55
   :header-rows: 1

   * - Key
     - Type
     - Description
   * - ``app_name``
     - str or null
     - Display name shown in the welcome screen header. ``null`` falls back to the name in ``pyproject.toml``, then the GitHub repo name, then ``"clizard"``.
   * - ``ascii_art``
     - str
     - Multi-line ASCII art shown in the welcome panel. Use ``\n`` for line breaks.
   * - ``docs_url``
     - str or null
     - URL opened by ``/docs``. ``null`` falls back to the ``Documentation`` URL in ``pyproject.toml``, then ``docs/index.html`` in the repo root.
   * - ``accent_color``
     - str
     - Rich-compatible colour string (hex or named) used for borders, headings, and the prompt. Default ``"#d97757"``.
   * - ``tips``
     - list of str
     - Slash commands shown in the "Use Commands" panel on the home screen. Controls which commands are surfaced, not which ones are registered.
   * - ``updates``
     - list of str
     - Changelog entries shown on the welcome screen. Most recent entry first.

A minimal example that gives a project its own identity:

.. code-block:: json

   {
     "app_name": "BN Pipeline",
     "accent_color": "#5b9bd5",
     "tips": ["/wizard", "/run", "/settings", "/help"],
     "updates": [
       "v1.2.0 — Bayesian discretisation now uses distfit",
       "v1.1.0 — Snakemake config support added"
     ]
   }

.. include:: add_bottom.add
