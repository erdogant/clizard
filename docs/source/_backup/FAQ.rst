FAQ
=====

Frequently Asked Questions
---------------------------

This page gathers the most common questions that arise when working with **clizard**.  Each section is written as a self‑contained narrative: we first describe why the issue matters, then explain how it manifests in practice, and finally provide concrete steps to resolve it.

Installation Issues
*******************

When you try to install clizard via pip or from source, you may run into a handful of pitfalls that are easy to overlook.  Understanding *why* these problems occur is key to troubleshooting them efficiently.  

First, the library contains optional C extensions that accelerate parsing.  If your environment lacks the necessary build tools (for example, `setuptools‑build` or a compiler), pip will silently fall back to pure Python but may emit warnings or fail outright.  This explains why you sometimes see an error message about missing headers even though the package appears to install.  

Second, installing from source requires that the current working directory contains a valid `setup.py` (or `pyproject.toml`).  Running `python -m pip install .` without being in the repository root will cause pip to look for these files and fail.  The error message is often cryptic: “No such file or directory: ‘setup.cfg’”, which can mislead users into thinking the source tree is corrupted.  

Finally, clizard’s configuration system expects a JSON file named `.clizard` in the project root.  If you install globally but later run commands from a different directory, the library will search for this file and silently fall back to defaults, producing confusing “missing configuration” errors.

The following table lists the two most frequently used functions that influence installation behaviour, along with their key parameters:

.. list-table:: Installation‑related functions
   :widths: 20 20 60
   :header-rows: 1

   * - Function
     - Parameter
     - Description
   * - ``build_parser``
     - ``--model`` (str, default: ``None``)
     - Path to a model file; missing if not provided.
   * - ``auto_cli``
     - ``--config`` (str, default: ``None``)
     - Path to a custom configuration JSON; ignored if absent.

The following console snippets show the recommended commands for each installation method:

.. code-block:: console

    pip install clizard
    # or from source
    python -m pip install .

If you encounter a failure due to missing C extensions, make sure that ``setuptools-build`` is installed and that your compiler toolchain (gcc/clang/MSVC) is available in the PATH.  For source installs, double‑check that you are executing the command from the repository root where ``setup.py`` resides.

Common Errors
*************

Runtime errors frequently stem from malformed configuration files or incorrect usage of helper functions.  Knowing *why* these errors surface helps prevent them and speeds up debugging.  

The function ``load_clizard_file`` is responsible for reading the `.clizard` JSON file.  If the file contains invalid JSON, the parser will catch the exception and return an empty dictionary instead of crashing.  This silent failure can lead to subtle bugs where downstream code assumes configuration values exist.  The helper ``ensure_clizard_file`` guarantees that a valid file is present by creating one with default settings if it does not already exist.

A typical error message looks like:

```
ValueError: Invalid JSON in .clizard
```

but the library swallows this and proceeds, which can be confusing for users who expect an explicit failure.  The recommended practice is to call ``ensure_clizard_file`` before any operation that relies on configuration data.

The following table documents the key parameters of these functions:

.. list-table:: Runtime error‑related functions
   :widths: 30 70
   :header-rows: 1

   * - Function
     - Parameter
   * - ``load_clizard_file``
     - ``repo_path`` (str, default: ``"."``)
       Directory to look for .clizard file; defaults to current working directory.
   * - ``ensure_clizard_file``
     - ``repo_path`` (str, default: ``"."``)
       Same as above.

Below is a minimal example that demonstrates how to safely load configuration data:

.. code-block:: python

    from clizard import load_clizard_file, ensure_clizard_file

    # Ensure a .clizard file exists before reading
    ensure_clizard_file('.')
    config = load_clizard_file('.')
    print(config)

If the output is an empty dictionary, run ``ensure_clizard_file('.')`` to generate a template and then edit it manually or via the CLI.

Parameter Choices
*****************

Choosing the right command‑line options can dramatically simplify your workflow.  The helper function ``auto_cli`` bridges argparse parsers with clizard’s generic CLI infrastructure, automatically registering common commands such as `/run` when a `main()` function is detected.

The first parameter, ``parser``, accepts an existing :class:`argparse.ArgumentParser`.  If you pass ``None``, the helper will create a new parser internally.  This flexibility allows you to integrate clizard into complex applications without rewriting your argument handling logic.

The second parameter, ``handler``, is a callable that receives free‑text input from the user.  By default it simply echoes back the prompt, but you can supply any custom function—such as a language model inference routine—to process the input and produce output on the fly.

Because clizard stores configuration in JSON files, you can override defaults at runtime with ``--config``.  This is especially useful when experimenting with different models or settings without modifying source code.

The table below lists the parameters for ``auto_cli``:

.. list-table:: auto_cli parameters
   :widths: 30 70
   :header-rows: 1

   * - Parameter
     - Type / Default / Description
   * - ``parser``
     - :class:`argparse.ArgumentParser`, default: ``None``
       Existing parser to wrap; if None, a new one is created.
   * - ``handler``
     - callable, default: ``None``
       Custom function for free‑text input; defaults to echoing the prompt.

Below is an example that shows how to use ``auto_cli`` in a simple script:

.. code-block:: python

    import argparse
    from clizard import auto_cli

    def my_handler(text):
        # Simple echo handler – replace with your own logic
        return f"You said: {text}"

    parser = argparse.ArgumentParser(description="Demo CLI")
    auto_cli(parser=parser, handler=my_handler)

    args = parser.parse_args()
    print("CLI started successfully.")

.. include:: add_bottom.add