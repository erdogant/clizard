Examples
=========

The following sections show concrete usage patterns for *clizard*, from the simplest zero-configuration case to full custom shells. Each example is self-contained and includes runnable code.


Zero-configuration: run clizard on any repo
--------------------------------------------

The simplest usage requires no code at all. Navigate to any Python project that has a ``main()`` function and run:

.. code-block:: console

   cd /path/to/your/project
   clizard

Clizard discovers the entry point automatically, extracts its arguments, and launches the interactive shell. From there:

.. code-block:: console

   ❯ /wizard        # step through every argument interactively
   ❯ /run           # execute main() with the current settings
   ❯ /settings      # view or edit any value directly
   ❯ /scaffold      # generate a standalone clizard_main.py

To generate a standalone wrapper without launching the shell:

.. code-block:: console

   clizardmake
   # clizard main file written to: /path/to/your/project/clizard_main.py


Wrapping an existing argparse script with ``auto_cli``
------------------------------------------------------

The :func:`auto_cli` helper bridges the gap between a legacy ``argparse``-based ``main()`` and the *clizard* interactive shell. It reads argument definitions directly from the existing :class:`~argparse.ArgumentParser` instance and maps them to interactive settings, preserving types, defaults, choices, and help text.

This example wraps a release tool that uploads Python packages to PyPI:

.. list-table:: Parameters of the release tool
   :widths: 15 10 65
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - username
     - ``str``
     - GitHub/GitLab username identifying the target repository.
   * - package
     - ``str``
     - Package name or path to release.
   * - clean
     - ``int``
     - Remove local build artifacts. ``0`` → False, ``1`` → True.
   * - install
     - ``int``
     - Install the package locally before release. Same integer mapping as ``clean``.
   * - twine
     - ``str``
     - Path to a custom Twine executable.
   * - verbosity
     - ``int``
     - Runtime output level (0–5).

.. code-block:: python

   import argparse
   from clizard import auto_cli
   from release_tool import run  # the core release logic

   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument("-u", "--username", type=str,
                           help="Username on Github/Gitlab.")
       parser.add_argument("-p", "--package", type=str,
                           help="Package name to be released.")
       parser.add_argument("-c", "--clean", type=int, choices=[0, 1],
                           help="Remove local builds: [dist], [build] and [x.egg-info].")
       parser.add_argument("-i", "--install", type=int, choices=[0, 1],
                           help="Install this version on local machine.")
       parser.add_argument("-t", "--twine", type=str,
                           help="Path to twine in case you have a custom build.")
       parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2, 3, 4, 5],
                           help="Verbosity level (higher number = more information).")
       args = parser.parse_args()

       def run_callback(cli):
           s = cli.config.settings
           run(
               s["username"],
               s["package"],
               clean=bool(s["clean"]),
               install=bool(s["install"]),
               twine=s["twine"],
               verbose=s["verbosity"],
           )

       cli = auto_cli(parser, args=args,
                      app_name="ReleaseTool",
                      run_callback=run_callback)
       cli.run()

After running this script the user sees a ``rich``-styled welcome screen. Typing ``/wizard`` steps through each argument interactively; ``/run`` calls the release function with the current values.


Building a custom shell with ``GenericCLI``
-------------------------------------------

When you want more control — custom commands, a specific welcome screen, or a free-text handler — use :class:`~clizard.GenericCLI` directly. This example wraps a text summarisation function:

.. list-table:: Settings for the summariser shell
   :widths: 15 10 65
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - input_path
     - ``str``
     - Path to the input text file.
   * - max_words
     - ``int``
     - Maximum number of tokens to extract. Defaults to ``50``.
   * - uppercase
     - ``bool``
     - Convert extracted tokens to uppercase before joining.

.. code-block:: python

   import argparse
   from pathlib import Path
   from clizard import GenericCLI

   def summarize(input_path, max_words=50, uppercase=False):
       text = Path(input_path).read_text().split()[:max_words]
       result = " ".join(text)
       return result.upper() if uppercase else result

   def build_cli(args):
       cli = GenericCLI(
           app_name="Summarizer CLI",
           settings={
               "input_path": args.input_path,
               "max_words":  args.max_words,
               "uppercase":  args.uppercase,
           },
           tips=["/run", "/settings", "/docs", "/help"],
       )

       @cli.command("/run", "Summarise the file at input_path")
       def cmd_run(prompt):
           path = cli.config.get("input_path")
           if not path:
               cli.error("No input_path set. Use: /settings set input_path <file>")
               return
           with cli.status(f"Summarising {path}..."):
               result = summarize(
                   input_path=path,
                   max_words=cli.config.get("max_words"),
                   uppercase=cli.config.get("uppercase"),
               )
           cli.assistant_message(result)

       # Free-text handler: typing a path directly runs the summariser.
       def handler(prompt, cli):
           return summarize(
               input_path=prompt,
               max_words=cli.config.get("max_words"),
               uppercase=cli.config.get("uppercase"),
           )

       cli.handler = handler
       return cli

   if __name__ == "__main__":
       parser = argparse.ArgumentParser()
       parser.add_argument("--input-path", type=str, default=None)
       parser.add_argument("--max-words",  type=int, default=50)
       parser.add_argument("--uppercase",  action="store_true", default=False)
       build_cli(parser.parse_args()).run()


Custom ASCII art, tips, and a project-specific command
------------------------------------------------------

This example shows how to give a project its own visual identity and add a domain-specific slash command. The pattern is used by tools like `LLMlight <https://github.com/erdogant/llmlight>`_ that wrap a local LLM backend:

.. code-block:: python

   from clizard import GenericCLI, parse_args

   EXTRA_ARGS = [
       {"flags": ["--model"],       "kwargs": {"type": str,   "default": None}},
       {"flags": ["--path"],        "kwargs": {"type": str,   "default": None}},
       {"flags": ["--temperature"], "kwargs": {"type": float, "default": None}},
   ]

   def my_handler(prompt, cli):
       # Replace with a real LLM call in your project.
       model = cli.config.get("model")
       return f"[{model}] Echo: {prompt}"

   def main():
       args = parse_args(app_name="LLMlight", extra_args=EXTRA_ARGS)

       cli = GenericCLI(
           app_name=args.name or "LLMlight",
           ascii_art=r"""
    /\_/\
   ( o.o )
    > ^ <
   """,
           settings={
               "model":       "google/gemma-2-6b",
               "path":        "C:/LLMlight",
               "temperature": 0.7,
           },
           config_path=args.config,
           handler=my_handler,
           tips=["/init", "/run", "/settings", "/help"],
           updates=[
               "Agent system improvements",
               "Documentation generation",
               "Local model support",
           ],
       )

       # Override defaults with any values supplied on the command line.
       cli.config.update_from_args({
           "model":       args.model,
           "path":        args.path,
           "temperature": args.temperature,
       })

       @cli.command("/init", "Initialise a new project at the configured path")
       def cmd_init(prompt):
           path = cli.config.get("path")
           cli.assistant_message(f"Initialised project at `{path}`")

       cli.run()

   if __name__ == "__main__":
       main()


Snakemake workflow integration
------------------------------

If your repository contains a ``Snakefile`` with a ``configfile:`` directive, clizard detects the YAML automatically and exposes its keys as editable settings (prefixed ``sm_``). No code changes are needed — just run ``clizard`` in the repo root.

For programmatic access to the same discovery logic:

.. code-block:: python

   from clizard.discover import find_snakemake_config, settings_from_snakemake_config

   config_path = find_snakemake_config(".")
   if config_path:
       settings = settings_from_snakemake_config(config_path)
       print(settings)
       # {"sm_samples": "data/samples.tsv",
       #  "sm_reference": "data/ref.fa",
       #  "sm_threads": 8,
       #  "sm_output_dir": "results/"}

When ``/run`` is invoked in the shell, clizard writes the current ``sm_``-prefixed values back to the YAML and then calls:

.. code-block:: console

   snakemake --configfile config/config.yaml --cores all


Important notes
---------------

* All examples require *clizard* to be installed (``pip install clizard``) and importable.
* :func:`auto_cli` maps argparse arguments to interactive settings automatically; existing ``main()`` functions do not need to be modified.
* Free-text handlers receive the raw prompt string and can return any string, which is rendered as Markdown in the assistant panel.
* Settings are persisted to ``.clizard/settings.json`` after every change; delete this file or run ``/reset`` to restore defaults.

.. include:: add_bottom.add
