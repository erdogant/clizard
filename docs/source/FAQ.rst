FAQ
=====

Frequently Asked Questions
---------------------------

This page gathers the most common questions that arise when working with **clizard**.  
Each section is written as a self‑contained narrative: we first describe why the issue matters, then explain how it manifests in practice, and finally provide concrete steps to resolve it.

How do I install clizard?
*************************

Installing a command‑line tool can feel intimidating if you are not familiar with Python packaging.  The reason this question is asked so often is that many users expect a single binary to appear on the system path after installation.  **clizard** deliberately avoids shipping external binaries; instead it relies on pure Python and optional compiled extensions that are built automatically by pip when possible.  This design choice keeps the package lightweight and ensures that it works out of the box in most virtual‑environment setups.

When you run ``pip install clizard`` from a clean environment, pip downloads the source distribution, resolves dependencies such as *rich* for terminal styling, and compiles any C extensions if your compiler is available.  If compilation fails, pip falls back to a pure‑Python implementation without raising an error, which explains why the installation often succeeds even on systems lacking build tools.  The optional binary approach also means that you can install **clizard** from source by cloning the repository and running ``python -m pip install .`` in the project root; this will honour any local modifications or additional dependencies defined in ``pyproject.toml``.

After installation, the entry‑point script ``clizard`` is automatically added to your environment’s executable directory.  You can verify that it works by invoking the help command:

.. code-block:: python

   pip install clizard
   python -m clizard --help

The output will display a Rich‑styled usage message and list available subcommands, confirming that the installation was successful.

What if I get an error about missing .clizard file?
**************************************************

When **clizard** starts up it looks for a configuration file named ``.clizard`` in the current working directory or any parent directories.  This file is expected to contain JSON that specifies project‑specific defaults such as model names, paths, and custom command definitions.  If the file is absent or contains malformed JSON, **clizard** falls back to an empty dictionary and uses built‑in defaults for all settings.  The fallback behaviour is intentional: it allows developers to run the tool in a new repository without first creating configuration files, while still enabling advanced customization when desired.

The function ``load_clizard_file`` encapsulates this logic.  It attempts to open the file, parse its contents with ``json.load``, and return the resulting dictionary.  If any exception occurs—whether due to missing file or invalid JSON—the function logs a warning (using Rich) and returns an empty dict.  The helper ``ensure_clizard_file`` guarantees that a configuration file exists by creating one with an empty object if necessary, which is useful when initializing a new project.

A typical usage pattern looks like this:

.. code-block:: python

   data = load_clizard_file('.')
   print(data)  # {} when missing

The printed output demonstrates the graceful degradation: an empty dictionary indicates that **clizard** will rely on defaults until you provide your own configuration.

How does clizard discover my project?
*************************************

Project discovery is a core feature of **clizard**.  The ``build_cli`` function in ``__main__.py`` orchestrates this process by inspecting the repository root (defaulting to ``"."``) for a variety of indicators that signal how the tool should behave.  It first checks for a ``main()`` function defined at the top level, which signals that the project is a Python script.  If found, it automatically creates a corresponding command that calls this function with parsed arguments.

Next, the discovery logic searches for Snakemake workflow files such as ``Snakefile`` or ``workflow/Snakefile``.  When a configuration directive (``configfile: config.yaml``) is present, the YAML file is parsed and merged into the CLI settings, allowing users to edit workflow parameters interactively through **clizard**.

The function also looks for Git metadata (e.g., ``.git/``), a ``pyproject.toml`` that defines project dependencies, and any existing ``.clizard`` overrides.  If none of these cues are found, ``build_cli`` falls back to creating a bare ``GenericCLI`` instance that still offers basic command handling but without project‑specific enhancements.

The following example shows how to build the CLI for the current directory and immediately run it:

.. code-block:: python

   cli = build_cli('.')
   cli.run()

Because the function accepts both string paths and :class:`pathlib.Path` objects, you can pass a custom repository root if your project lives elsewhere.

Can I use clizard with an existing argparse script?
****************************************************

Many developers have legacy scripts that already use ``argparse`` to parse command‑line arguments.  Refactoring these scripts to adopt **clizard**’s interactive interface would normally require significant code changes.  The ``auto_cli`` helper bridges this gap by extracting the argument definitions from an existing :class:`argparse.ArgumentParser` instance and converting them into a ``GenericCLI`` that preserves type casting, default values, and validation logic.

The function iterates over each action in the parser’s ``_actions`` list, mapping argument names to settings keys.  It then constructs a new CLI where each option becomes an interactive prompt when the user invokes the tool without specifying it on the command line.  The original parsing semantics are retained: if the user supplies a value on the command line, that value overrides any stored configuration.

Because ``auto_cli`` does not modify your original parser or its ``main()`` function, you can keep your existing code untouched and still enjoy **clizard**’s features.  A minimal example:

.. code-block:: python

   import argparse
   p = argparse.ArgumentParser()
   p.add_argument('--foo', type=int)
   cli = auto_cli(p)
   cli.run()

After running this script, you will see a Rich‑styled prompt asking for ``--foo`` if it was not supplied on the command line.

How do I persist configuration changes?
***************************************

Configuration persistence is handled by the :class:`Config` class.  Each instance represents a JSON file stored under the default configuration directory (typically ``$XDG_CONFIG_HOME/clizard/``).  The constructor accepts an ``app_name`` string that uniquely identifies the config file; this allows multiple applications to coexist without clashing.

The ``set`` method writes a key/value pair immediately to the in‑memory dictionary and then flushes it to disk.  This is useful for one‑off changes such as toggling a flag or updating a path.  For batch updates, you can use ``update_from_args`` which merges a dictionary of CLI overrides into the current settings but does not automatically persist them.  After making multiple modifications, call ``config.save()`` to write all changes to disk in one operation.

The following snippet demonstrates creating a configuration object, setting a value, and retrieving it:

.. code-block:: python

   cfg = Config('myapp')
   cfg.set('foo', 42)
   print(cfg.get('foo'))

When you run this code, the console will display ``42`` and the JSON file will contain an entry for ``"foo": 42``.

What are the common command options?
************************************

The ``build_parser`` function is responsible for assembling the top‑level argument parser that **clizard** presents to users.  It accepts a ``name`` parameter identifying the tool, as well as an optional ``extra_args`` list that allows callers to inject additional flags.

Among the most frequently used options are:

* ``--model`` – selects the language model backend (e.g., “gpt‑3.5” or “llama”).  
* ``--path`` – specifies a working directory for relative file references.  
* ``--config`` – points to an external configuration file, overriding the default ``.clizard`` location.  
* ``--name`` – assigns a unique identifier to the current session, useful when running multiple instances concurrently.

Additional arguments can be added by passing dictionaries with ``flags`` and ``kwargs`` keys.  For example, to add a ``--verbose`` flag that stores a boolean value:

.. code-block:: python

   p = build_parser('tool', extra=[{'flags':['--verbose'],'kwargs':{'action':'store_true'}}])

This pattern keeps the parser flexible while maintaining a clean API for developers.

How do I add custom slash commands?
***********************************

Custom slash commands are defined by decorating functions with ``@cli.command``.  The decorator registers the function under a specified command name and an optional description that appears in help output.  When the user types the command at the prompt, **clizard** passes the current prompt string as the sole argument to the function.

The signature of the decorated function is intentionally simple: it receives only the prompt text, allowing developers to focus on implementing business logic rather than parsing arguments.  The decorator internally stores metadata such as the command name and description in the ``GenericCLI`` instance’s registry.

A typical example:

.. code-block:: python

   @cli.command('/hello','Greet user')
   def greet(prompt):
       print('Hello!')

When the user types ``/hello`` at the prompt, the function executes and prints “Hello!”.  This pattern encourages rapid prototyping of interactive features without boilerplate.

What if I want to run my script directly from the CLI?
******************************************************

The ``auto_cli`` helper also supports a special callback mechanism.  By providing a ``run_callback`` callable, **clizard** automatically registers a ``/run`` command that invokes this function with the current :class:`GenericCLI` instance as its argument.  This is particularly useful for scripts that perform a single action and traditionally exit after parsing arguments.

The callback receives the CLI object, giving it full access to parsed settings, configuration values, and the ability to trigger further interactions if needed.  The following example shows how to expose a ``/run`` command that calls your original main function:

.. code-block:: python

   cli = auto_cli(p, run_callback=lambda c: my_main(**c.settings))

After running this script, you can type ``/run`` at the prompt and the original ``my_main`` function will execute with all current settings applied.

How does clizard handle Snakemake workflows?
********************************************

Snakemake integration is achieved through the ``find_snakemake_config`` helper.  The function scans the repository for a ``Snakefile`` that contains a ``configfile: <path>`` directive.  When such a file is found, it parses the referenced YAML configuration and merges its contents into **clizard**’s internal settings dictionary.

This merging process allows users to edit workflow parameters interactively via **clizard**, while still preserving the original Snakemake semantics.  For example, if your Snakefile expects a parameter ``samples: 100``, you can change this value at the prompt and then run the workflow without editing the YAML file manually.

A simple usage pattern:

.. code-block:: python

   config = find_snakemake_config('.')
   print(config)

The printed output will show the merged configuration dictionary, making it easy to verify that **clizard** has correctly interpreted the Snakemake settings.

Important notes
***************

* clizard uses Rich for terminal styling; output may vary across terminals.  
* All configuration files are JSON; manual edits are supported and will be respected on subsequent runs.

.. include:: add_bottom.add