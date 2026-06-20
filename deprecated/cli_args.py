"""Argument parsing for GenericCLI-based tools."""
import argparse


def build_parser(app_name="Generic CLI", extra_args=None):
    """Create an argparse.ArgumentParser with common options.

    extra_args: list of dicts like {"flags": ["--foo"], "kwargs": {...}}
    to let downstream scripts add their own arguments.
    """
    parser = argparse.ArgumentParser(prog=app_name, description=f"{app_name} - interactive CLI")
    parser.add_argument("--model", default=None, help="Model name/identifier to use")
    parser.add_argument("--path", default=None, help="Working/project path")
    parser.add_argument("--config", default=None, help="Path to a JSON config file")
    parser.add_argument("--name", default=None, help="Override the displayed app name")

    if extra_args:
        for arg in extra_args:
            parser.add_argument(*arg["flags"], **arg.get("kwargs", {}))

    return parser


def parse_args(app_name="Generic CLI", extra_args=None, argv=None):
    parser = build_parser(app_name, extra_args)
    return parser.parse_args(argv)


def auto_cli(parser, args=None, app_name=None, handler=None, run_callback=None, config_path=None):
    """Build a GenericCLI automatically from an existing argparse.ArgumentParser.

    Every `--flag` already defined on `parser` becomes an editable setting:
    its current value (parsed from argv, or its default) seeds the CLI's
    `/settings` table, and its `choices`/`type`/`help` are kept so `/settings`
    can validate and cast edits correctly.

    Parameters
    ----------
    parser : argparse.ArgumentParser
        An already-configured parser (e.g. the one built in your existing
        `main()`), or just `parser` before calling `parse_args()` on it.
    args : argparse.Namespace, optional
        Pre-parsed args. If omitted, `parser.parse_args()` is called.
    app_name : str, optional
        Defaults to `parser.prog`.
    handler : callable(prompt, cli) -> str, optional
        Called for free-text input. If omitted, free-text input does nothing
        special; use `run_callback` + a `/run` command instead (see below).
    run_callback : callable(cli) -> str, optional
        If given, a `/run` command is registered that calls
        `run_callback(cli)` using the current settings, mirroring how you'd
        call your script's `run(...)` function with `args.*`.
    config_path : str, optional
        Where to persist settings between sessions.

    Returns
    -------
    GenericCLI
    """
    from .core import GenericCLI  # local import avoids a circular import

    if args is None:
        args = parser.parse_args()

    settings = {}
    arg_meta = {}
    for action in parser._actions:
        dest = action.dest
        if dest in ("help",) or isinstance(action, argparse._HelpAction):
            continue
        settings[dest] = getattr(args, dest, action.default)
        arg_meta[dest] = {
            "choices": list(action.choices) if action.choices else None,
            "type": action.type,
            "help": action.help,
        }

    cli = GenericCLI(
        app_name=app_name or parser.prog or "CLI",
        settings=settings,
        config_path=config_path,
        handler=handler,
        tips=["/run", "/settings", "/help"] if run_callback else ["/settings", "/help"],
    )
    cli.arg_meta = arg_meta  # exposed for validation / display in /settings

    if run_callback is not None:
        @cli.command("/run", "Run the script with current settings")
        def _cmd_run(prompt):
            cli.status("Running...")
            result = run_callback(cli)
            if result is not None:
                cli.assistant_message(str(result))

    return cli

