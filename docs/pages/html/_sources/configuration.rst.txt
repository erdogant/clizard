configuration
==============

The :mod:`clizard_file` module is the single source of truth for persisting project‑specific settings in a lightweight JSON file named ``.clizard``.  It lives at the root of every repository that uses the clizard scaffolding tools and contains information such as the application name, documentation URL, ASCII art banner, accent colour, tips, and an updates log.  The design goal is to keep the API tiny yet robust: callers can load or write configuration without worrying about file‑system errors or malformed data, while still having the flexibility to override defaults on a per‑run basis.

The module exposes three helper functions – :func:`load_clizard_file`, :func:`save_clizard_file` and :func:`ensure_clizard_file`.  All three operate purely on I/O and simple dictionary manipulation; they do not perform semantic validation or business logic.  This separation of concerns allows higher‑level tooling (such as documentation generators, CI pipelines or CLI commands) to focus on their domain while delegating configuration persistence to a well‑tested, fault‑tolerant layer.

The functions are intentionally forgiving: any exception raised during file access is caught and logged, but the caller receives a sane default value instead of an error propagating up the stack.  This behaviour guarantees that downstream code can always merge the returned dictionary with its own defaults without wrapping every call in ``try``/``except`` blocks.  The trade‑off is that silent failures may hide configuration problems; however, the module logs warnings to the standard library’s :mod:`logging` system so that developers are still alerted when something goes wrong.

load_clizard_file
-----------------

The :func:`load_clizard_file` function is the entry point for reading an existing ``.clizard`` file from disk.  It accepts a single path argument that points to the root of the repository or any subdirectory containing the configuration.  Internally, it uses :class:`pathlib.Path` to construct the absolute file location and then attempts to open and parse the JSON payload.  If the file is missing, unreadable due to permission issues, or contains syntactically invalid JSON, the function swallows the exception and returns an empty dictionary instead of propagating an error.  This design choice ensures that callers can safely merge the returned configuration with defaults without having to wrap every load in a try/except block.

The function is deliberately lightweight: it does not perform any validation beyond JSON decoding.  Any semantic checks – such as verifying required keys or value types – are left to higher‑level code that consumes the dictionary.  By returning an empty dict on failure, the function guarantees that downstream logic will always receive a mapping object, simplifying control flow and reducing boilerplate.

The return value is always a plain :class:`dict` instance, which callers can safely modify or merge with other configuration sources.  The function also logs a warning via the standard library's ``logging`` module when it encounters an error, providing visibility into silent failures without interrupting execution.

.. list-table:: Parameters for :func:`load_clizard_file`
   :widths: 20 10 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - repo_path
     - str
     - Directory containing ``.clizard`` (default current working directory)

.. code-block:: python

   from clizard_file import load_clizard_file

   # Load configuration from a specific repository path.
   config = load_clizard_file("/path/to/repo")
   print(config)


save_clizard_file
-----------------

The :func:`save_clizard_file` helper serializes an arbitrary dictionary to JSON and writes it to the ``.clizard`` file in the specified repository directory.  The function enforces a two‑space indentation level, which makes the output human‑readable while keeping the file compact enough for version control diffing.  It overwrites any existing file without prompting or raising an exception, thereby guaranteeing that callers always end up with the latest configuration state.

The implementation uses :class:`pathlib.Path` to resolve the target path and ensures that parent directories exist by calling ``mkdir(parents=True, exist_ok=True)`` before writing.  The function returns the resolved :class:`~pathlib.Path` object pointing at the written file, allowing callers to perform further operations (e.g., adding the file to a git index) if desired.

Because JSON serialization can fail for non‑serializable objects, the function expects that the input dictionary contains only primitive types (strings, numbers, booleans, lists, and nested dictionaries).  If an unsupported type is encountered, ``json.dumps`` will raise a :class:`TypeError`, which propagates to the caller – this is intentional, as silently dropping data would be more harmful.

.. list-table:: Parameters for :func:`save_clizard_file`
   :widths: 20 10 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - data
     - dict
     - Configuration dictionary to persist
   * - repo_path
     - str
     - Directory where ``.clizard`` will be written

.. code-block:: python

   from clizard_file import save_clizard_file

   config = {
       "app_name": "MyApp",
       "docs_url": "https://myapp.readthedocs.io"
   }
   path = save_clizard_file(config, repo_path="/my/project")
   print(f"Configuration written to {path}")


ensure_clizard_file
-------------------

The :func:`ensure_clizard_file` function is the most feature‑rich helper in this module.  It guarantees that a valid ``.clizard`` file exists at the target location, creating one with sensible defaults if necessary.  The function first attempts to load an existing configuration using :func:`load_clizard_file`.  If the result is empty (indicating absence or corruption), it constructs a default dictionary containing keys such as ``app_name``, ``ascii_art`` (set to :data:`DEFAULT_ASCII`), ``docs_url``, ``accent_color`` (defaulting to ``#d97757``), a list of ``tips``, and an empty ``updates`` section.

After establishing the base configuration, the function merges any keyword arguments supplied via ``**overrides`` into the dictionary.  This merge is performed in place so that callers can supply only the values they wish to change while inheriting all other defaults.  The merged configuration is then written back to disk using :func:`save_clizard_file`, ensuring that the file on disk reflects the caller’s intent.

The function returns the final configuration dictionary, allowing callers to inspect or further manipulate it before use.  Because the merge operation overwrites existing keys with supplied values, callers can selectively update parts of the configuration without having to rebuild the entire mapping manually.  The design choice to perform merging in memory rather than on disk keeps file I/O minimal and reduces race conditions when multiple processes might attempt to write concurrently.

.. list-table:: Parameters for :func:`ensure_clizard_file`
   :widths: 20 10 60
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - repo_path
     - str
     - Directory where ``.clizard`` should exist (default current working directory)
   * - **overrides
     - dict
     - Keyword arguments that override default configuration values

.. code-block:: python

   from clizard_file import ensure_clizard_file

   # Ensure a .clizard file exists, overriding the app name.
   config = ensure_clizard_file(repo_path="/my/project", app_name="SuperApp")
   print("Final configuration:", config)

.. include:: add_bottom.add