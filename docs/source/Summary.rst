Summary
========

Background
**********

The *clizard* library is a lightweight toolkit designed to simplify the creation and management of command‑line interfaces (CLIs) in Python projects. Its core philosophy is that most CLI applications share a common set of options—such as verbosity, configuration file paths, and help flags—and that these can be generated automatically without repetitive boilerplate code. By providing a small API surface around `argparse`, *clizard* allows developers to focus on business logic while still delivering a polished user experience.

The library was conceived in response to the growing need for reproducible data‑science workflows. Researchers often prototype scripts that later become production tools, yet they repeatedly write similar CLI scaffolding. *clizard* eliminates this duplication by offering functions like `build_parser` and `auto_cli`, which introspect existing parsers or configuration files and generate fully functional command lines on the fly. This not only speeds up development but also enforces consistency across projects.

Another motivation behind *clizard* is to bridge the gap between code and documentation. The library can load a `.clizard.json` file that contains metadata about the CLI, such as default values and help messages. Functions like `load_clizard_file` and `ensure_clizard_file` provide robust handling of these files, ensuring that even if a user forgets to supply one, sensible defaults are applied automatically.

Output
******

When a developer integrates *clizard* into their project, the library produces two primary artifacts: an enriched command‑line parser and a JSON configuration file. The enriched parser automatically injects standard arguments (`--verbose`, `--config`, `--help`) while preserving any custom options defined by the user. This guarantees that every executable script in a codebase behaves consistently, making it easier for end users to discover available flags and understand their effects.

In addition to the parser, *clizard* writes a `.clizard.json` file that captures the current state of the CLI configuration. This file can be used by downstream tools—such as documentation generators or CI pipelines—to introspect the command‑line interface without executing the script. By keeping this metadata in sync with the code, developers avoid the pitfalls of stale help messages and mismatched defaults.

Finally, *clizard* offers a small set of helper functions that expose the parsed arguments as a dictionary. This makes it trivial to serialize runtime configuration for reproducibility or logging purposes, enabling researchers to capture exactly how a script was invoked in a single line of code.

Schematic Overview
******************

The high‑level workflow of *clizard* can be visualised with the following ASCII diagram:

.. code-block:: text

   ┌───────────────────────┐
   │  User defines parser  │
   │ (argparse.ArgumentParser)│
   └─────────────▲─────────┘
                 │
          enrich_parser()
                 │
   ┌─────────────▼─────────┐
   │  Parser with defaults │
   │  and standard flags   │
   └─────────────▲─────────┘
                 │
         parse_args() or auto_cli()
                 │
   ┌─────────────▼─────────┐
   │  Namespace object     │
   │  (user arguments)     │
   └─────────────▲─────────┘
                 │
          write_clizard_file()
                 │
   ┌─────────────▼─────────┐
   │  .clizard.json file   │
   │  (metadata snapshot)  │
   └───────────────────────┘

The diagram illustrates how *clizard* starts with a user‑supplied parser, enriches it with standard arguments and defaults, parses the command line, and finally persists the configuration to disk. Each step is intentionally lightweight so that developers can drop *clizard* into existing projects without altering their workflow.

.. include:: add_bottom.add