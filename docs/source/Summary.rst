Summary
========

Background
**********

The *clizard* library is a lightweight toolkit that wraps any existing Python project in a rich, interactive terminal interface — with no changes to the project's own code required. Its core philosophy is that most Python tools share a common problem: the logic is solid, but running it requires knowing the right flags, paths, and defaults. *clizard* solves this by auto-discovering the project's entry point, extracting its arguments, and presenting them through a guided shell with settings persistence and one-click execution.

The library was conceived for data science and research workflows, where scripts frequently evolve into production tools yet keep accumulating CLI boilerplate. Rather than asking developers to adopt a new framework, *clizard* meets existing code where it is: it can introspect a bare function signature, an internal ``argparse.ArgumentParser``, or a Snakemake ``config.yaml`` — and produce a consistent interactive interface from any of them.

A second motivation is reproducibility. Settings edited through the shell are persisted to ``.clizard/settings.json`` between sessions. This means a colleague who configures ``--input-path`` on Monday finds that value waiting on Tuesday, and a CI pipeline can inspect the last-used configuration without re-running the tool.


Output
******

When *clizard* starts in a repository it produces two primary runtime artifacts:

1. **An interactive shell** — a ``rich``-based terminal application with built-in slash commands (``/wizard``, ``/run``, ``/settings``, ``/reset``, ``/install``, ``/docs``, ``/help``) and an optional free-text handler for project-specific prompts.

2. **A ``.clizard/`` directory** at the repository root, containing:

   * ``settings.json`` — the persisted runtime configuration (written on every ``/settings set`` or ``/wizard`` completion).
   * ``meta.json`` — optional display customisation: app name, ASCII art banner, accent colour, tips menu, and an updates log.

Optionally, the ``/scaffold`` command (or the ``clizardmake`` console entry point) generates a standalone ``clizard_main.py`` that bakes the current settings and argument metadata into a self-contained file. This file runs without any discovery step and is suitable for distribution alongside the project.


Schematic Overview
******************

The high-level workflow of *clizard* from startup to execution:

.. code-block:: text

   ┌─────────────────────────────────────┐
   │  Repository root                    │
   │  (contains main.py / __main__.py /  │
   │   Snakefile / pyproject.toml)       │
   └──────────────────┬──────────────────┘
                      │
              find_main() / find_snakemake_config()
                      │
   ┌──────────────────▼──────────────────┐
   │  Entry point discovered             │
   │  (module, main_func, file_path)     │
   └──────────────────┬──────────────────┘
                      │
         settings_from_main() or
         settings_from_snakemake_config()
                      │
   ┌──────────────────▼──────────────────┐
   │  Settings dict + arg metadata       │
   │  (defaults, types, choices, help)   │
   └──────────────────┬──────────────────┘
                      │
               GenericCLI(...)
                      │
   ┌──────────────────▼──────────────────┐
   │  Interactive shell                  │
   │  /wizard  /run  /settings  /reset   │
   └──────────────────┬──────────────────┘
                      │
             /run invoked
                      │
   ┌──────────────────▼──────────────────┐
   │  main(**settings)                   │
   │  — or —                             │
   │  sys.argv rebuilt → main()          │
   │  — or —                             │
   │  snakemake --configfile config.yaml │
   └─────────────────────────────────────┘

Each step is intentionally lightweight. *clizard* does not require changes to the underlying project and imposes no framework constraints on how ``main()`` is structured.

.. include:: add_bottom.add
