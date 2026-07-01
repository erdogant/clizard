Examples
=========

The following sections provide concrete usage patterns that illustrate how the :mod:`clizard` framework can be leveraged to build powerful command‑line interfaces for a variety of tasks.  Each example is self‑contained, demonstrates key design decisions, and includes runnable code snippets that show the full interaction flow from argument parsing to execution.

Release Tool CLI Example
------------------------

The release tool example showcases how to wrap an existing :mod:`argparse` parser with :func:`clizard.auto_cli`.  By delegating the heavy lifting of mapping command‑line arguments into a structured configuration object, developers can focus on the business logic of releasing artifacts while still providing a polished user experience.

In this pattern, the ``auto_cli`` helper automatically extracts values from the parsed arguments and stores them in ``cli.config.settings``.  The ``run_callback`` function then pulls those settings out and forwards them to the underlying release routine.  This separation of concerns keeps the CLI layer thin and testable while preserving the flexibility of a traditional argparse interface.

Because the release workflow often involves side effects such as cleaning build directories, installing dependencies, or invoking external tools like Twine, the example demonstrates how optional integer flags can be converted into boolean semantics within the callback.  The verbosity level is also propagated to give users fine‑grained control over output noise.

.. list-table:: Parameters of :func:`auto_cli`
   :widths: 15 10 65
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - username
     - ``str``
     - Username on Github/Gitlab used to identify the target repository.
   * - package
     - ``str``
     - Package name or path that should be released.
   * - clean
     - ``int | None``
     - Flag to remove local build artifacts; ``0`` maps to ``False``, ``1`` to ``True``.
   * - install
     - ``int | None``
     - Flag to install the package locally before release; same integer mapping as ``clean``.
   * - twine
     - ``str | None``
     - Custom path to a Twine executable if the default is unsuitable.
   * - verbosity
     - ``int | None``
     - Verbosity level controlling the amount of runtime information emitted.

.. code-block:: python

    import argparse
    from clizard import auto_cli
    from release_tool import run  # The core release logic

    def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-u", "--username", type=str,
                            help="Username on Github/Gitlab…")
        parser.add_argument("-p", "--package", type=str,
                            help="Package name to be released.")
        parser.add_argument(
            "-c",
            "--clean",
            type=int,
            choices=[0, 1],
            help="Remove local builds: [dist], [build] and [x.egg-info]."
        )
        parser.add_argument(
            "-i",
            "--install",
            type=int,
            choices=[0, 1],
            help="Install this version on local machine."
        )
        parser.add_argument("-t", "--twine", type=str,
                            help="Path to twine in case you have a custom build.")
        parser.add_argument(
            "-v",
            "--verbosity",
            type=int,
            choices=[0, 1, 2, 3, 4, 5],
            help="Verbosity level (higher number tends to more information)."
        )
        args = parser.parse_args()

        def run_callback(cli):
            s = cli.config.settings
            run(
                s["username"],
                s["package"],
                clean=s["clean"],
                install=s["install"],
                twine=s["twine"],
                verbose=s["verbosity"]
            )

        cli = auto_cli(parser, args=args,
                       app_name="ReleaseTool",
                       run_callback=run_callback)
        cli.run()

Summarizer CLI Wrapper
-----------------------

This example demonstrates how a simple text summarization function can be exposed through an interactive GenericCLI.  The wrapper adds slash commands and free‑text handling, allowing users to trigger summarization either via explicit `/run` commands or by simply typing the path of a document.

The ``GenericCLI`` instance is configured with default settings derived from command‑line arguments.  The ``/run`` command reads those settings, validates that an input file exists, and then calls :func:`summarize`.  Free‑text prompts are interpreted as file paths, enabling quick one‑liner usage without needing to remember the exact syntax of a slash command.

By exposing both a structured command interface and a flexible free‑text handler, this pattern provides an intuitive user experience that scales from casual experimentation to scripted automation.

.. list-table:: Parameters of :func:`summarize`
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
     - Maximum number of whitespace‑delimited tokens to extract from the start of the document. Defaults to 50.
   * - uppercase
     - ``bool``
     - If True, all extracted tokens are converted to uppercase before joining.

.. code-block:: python

    def build_cli(args):
        cli = GenericCLI(
            app_name="Summarizer CLI",
            settings={
                "input_path": args.input_path,
                "max_words": args.max_words,
                "uppercase": args.uppercase,
            },
            tips=["/run", "/settings", "/docs", "/help"],
        )

        @cli.command("/run", "Run the summarizer with current settings")
        def cmd_run(prompt):
            path = cli.config.get("input_path")
            if not path:
                cli.error(
                    "No input_path set. Use: /settings set input_path <file>"
                )
                return
            cli.status(f"Summarizing {path}...")
            result = summarize(
                input_path=path,
                max_words=cli.config.get("max_words"),
                uppercase=cli.config.get("uppercase"),
            )
            cli.assistant_message(result)

        def handler(prompt, cli):
            return summarize(
                input_path=prompt,
                max_words=cli.config.get("max_words"),
                uppercase=cli.config.get("uppercase"),
            )

        cli.handler = handler
        return cli

LLMlight Custom CLI
--------------------

The LLMlight example illustrates how to extend :class:`clizard.GenericCLI` with custom commands, ASCII art, and a user‑defined handler that would normally interface with an LLM backend.  The design showcases project‑specific logic in the `/init` command while keeping the core CLI loop lightweight.

In this pattern, the ``GenericCLI`` is instantiated with a multi‑line ASCII banner that gives the tool a distinctive visual identity.  Settings such as model identifier, local path, and temperature are supplied via both command‑line arguments and an optional configuration file.  The handler function, ``my_handler``, acts as a placeholder for real LLM calls; in practice it would forward prompts to a language model API and return the generated response.

The example also demonstrates how to update settings from parsed arguments after CLI construction, ensuring that defaults can be overridden at runtime without modifying the original configuration dictionary.

.. list-table:: Parameters of :func:`my_handler`
   :widths: 15 10 65
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - model
     - ``str``
     - Model identifier to be used for inference.
   * - path
     - ``str``
     - Local filesystem path where the model resides.
   * - temperature
     - ``float``
     - Sampling temperature controlling output randomness.

.. code-block:: python

    def main():
        args = parse_args(app_name="LLMlight", extra_args=EXTRA_ARGS)

        cli = GenericCLI(
            app_name=args.name or "LLMlight",
            ascii_art=r'''
    /\_/\
    ( o.o )
    > ^ <
    '''

    settings={
                "model": "google/gemma-26B-a4B",
                "path": "C:/LLMlight",
                "temperature": 0.7,
            },
            config_path=args.config,
            handler=my_handler,
            tips=["/init", "/help", "generate documentation"],
            updates=[
                "Agent system improvements",
                "Documentation generation",
                "Local model support",
            ],
        )
        cli.config.update_from_args(
            {"model": args.model, "path": args.path, "temperature": args.temperature}
        )

        @cli.command("/init", "Initialize a new project")
        def cmd_init(prompt):
            cli.assistant_message(f"Initialized project at `{cli.config.get('path')}`")

        cli.run()

Important Notes
-----------------

* All examples rely on the :class:`clizard.GenericCLI` base class from the *clizard* package; ensure it is installed and importable.
* The ``auto_cli`` helper automatically maps argparse arguments to CLI settings, simplifying integration with legacy parsers.
* Free‑text handlers allow users to type arbitrary prompts that are interpreted as input paths or commands, providing a natural interaction model for exploratory workflows.

.. include:: add_bottom.add
