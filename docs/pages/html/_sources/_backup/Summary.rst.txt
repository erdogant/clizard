Summary
========

Background
**********

The *clizard* library is a lightweight toolkit designed to simplify the creation and management of command‑line interfaces (CLIs) in Python projects. Its core philosophy is that most CLI applications share a common set of options—such as verbosity, configuration file paths, and help flags—and that these can be generated automatically without repetitive boilerplate code. By providing a small API surface around `argparse`, *clizard* allows developers to focus on business logic while still delivering a polished user experience.

The library was conceived in response to the growing need for reproducible data‑science workflows. Researchers often prototype scripts that later become production tools, yet they repeatedly write similar CLI scaffolding. *clizard* eliminates this duplication by offering functions like `build_parser` and `auto_cli`, which introspect existing parsers or configuration files and generate fully functional command lines on the fly. This not only speeds up development but also enforces consistency across projects.

Another motivation behind *clizard* is to bridge the gap between code and documentation. The library can load a `.clizard.json` file that contains metadata about the CLI, such as default values and help messages. Functions like `load_clizard_file` and `ensure_clizard_file` provide robust handling of these files, ensuring that even if a user forgets to supply one, sensible defaults are applied automatically.

Finally, *clizard* embraces modern Python packaging practices. It is distributed on PyPI (`pip install clizard`) and hosted on GitHub, making it easy for teams to integrate into continuous‑integration pipelines. The accompanying documentation site demonstrates how to set up a virtual environment with conda or pip, ensuring that new users can get started quickly.

Output
******

When combined, the components of *clizard* produce a fully‑featured command‑line interface that is both user‑friendly and maintainable. Users can invoke their scripts with standard flags such as `--help`, `--verbose`, or `--config`, and the library automatically parses these options into a configuration dictionary. This dictionary can then be passed to any function in the application, allowing downstream code to remain agnostic of how parameters were supplied.

Beyond simple flag parsing, *clizard* also supports loading structured JSON configuration files (`.clizard.json`). These files can define default values for arguments, specify mutually exclusive groups, or even embed documentation snippets that are rendered by `auto_cli`. As a result, the output of the library is not just parsed arguments but a coherent, self‑documenting CLI that reduces friction for both developers and end users.

Because *clizard* operates on top of `argparse`, it inherits all of its extensibility. Developers can add custom argument types, subparsers, or even integrate with other libraries such as Click or Typer if needed. The library’s design encourages incremental adoption: a project may start by wrapping an existing parser with `auto_cli` and later evolve to use the full configuration management features.

Schematic Overview
******************

The high‑level workflow of *clizard* can be visualised as follows:

.. code-block:: text

   ┌───────────────────────┐
   │  User invokes script   │
   │     with CLI flags      │
   └────────────▲───────────┘
                │
                ▼
   ┌───────────────────────┐
   │  build_parser() creates│
   │  an ArgumentParser    │
   │  with common options   │
   └────────────▲───────────┘
                │
                ▼
   ┌───────────────────────┐
   │  auto_cli() attaches   │
   │  the parser to a      │
   │  function or class    │
   └────────────▲───────────┘
                │
                ▼
   ┌───────────────────────┐
   │  load_clizard_file()  │
   │  reads .clizard.json  │
   │  (if present)         │
   └────────────▲───────────┘
                │
                ▼
   ┌───────────────────────┐
   │  ensure_clizard_file()│
   │  merges defaults with │
   │  user overrides       │
   └────────────▲───────────┘
                │
                ▼
   ┌───────────────────────┐
   │  Config() stores      │
   │  configuration in a   │
   │  JSON‑backed dict     │
   └────────────▲───────────┘
                │
                ▼
   ┌───────────────────────┐
   │  update_from_args()   │
   │  updates Config with  │
   │  parsed CLI arguments │
   └───────────────────────┘

Each step is implemented by a dedicated function or class, and the diagram illustrates how they cooperate to transform raw command‑line input into a structured configuration object ready for use in an application.

Example Usage
-------------

Below is a minimal example that demonstrates how *clizard* can be used to build a CLI around a simple function:

.. code-block:: python

   from clizard import build_parser, auto_cli, load_clizard_file, ensure_clizard_file, Config, update_from_args

   def greet(name: str, times: int = 1):
       """Prints a greeting multiple times."""
       for _ in range(times):
           print(f"Hello, {name}!")

   # Create a parser with common options
   parser = build_parser()

   # Attach the parser to the function
   cli = auto_cli(greet, parser=parser)

   if __name__ == "__main__":
       # Load optional configuration file
       cfg_data = load_clizard_file()
       cfg = ensure_clizard_file(cfg_data)
       config = Config(data=cfg)

       # Parse command‑line arguments and update the config
       args = cli.parse_args()
       update_from_args(args, config)

       # Call the function with parsed parameters
       greet(**config.to_dict())

.. include:: add_bottom.add