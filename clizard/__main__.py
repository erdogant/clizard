"""Default console-script entry point: `clizard`.

Run with no args inside a repo to auto-discover everything:
  - the repo's main() (via __main__.py / main.py signature)
  - a Snakemake workflow (Snakefile + config.yaml), if present
  - git remote info (.git/config)
  - pyproject.toml metadata (name, docs url, requirements)
  - .clizard overrides (ascii art, accent color, tips, app name, docs url)

Falls back to a bare GenericCLI if nothing is discoverable.
"""
import subprocess
import sys
from pathlib import Path

from .cli_args import parse_args
from .core import GenericCLI
from .git_info import get_git_info
from .project_info import get_project_info
from .clizard_file import ensure_clizard_file
from .discover import (
    find_main, settings_from_main,
    find_snakemake_config, settings_from_snakemake_config, write_snakemake_config,
)
from .scaffold import generate_clizard_main


def build_cli(repo_path="."):
    repo_path = str(Path(repo_path).resolve())

    git_info = get_git_info(repo_path)
    proj_info = get_project_info(repo_path)
    clz = ensure_clizard_file(repo_path, create=False)

    app_name = clz.get("app_name") or proj_info.get("name") or git_info.get("github_repo") or "clizard"
    docs_url = clz.get("docs_url") or proj_info.get("docs_url")

    discovery_errors = []
    module, main_func, entry_file = find_main(repo_path, errors=discovery_errors)
    main_settings, arg_meta, call_style = settings_from_main(main_func) if main_func else ({}, {}, "kwargs")

    sm_config_path = find_snakemake_config(repo_path)
    sm_settings = settings_from_snakemake_config(sm_config_path) if sm_config_path else {}

    # Short, friendly summary of what discovery found, so a bare/limited
    # CLI (no /run, few settings) is explained instead of just showing up
    # empty. Kept plain (no paths/backticks) to read as a status note, not
    # a technical/error log line.
    if main_func is not None:
        n = len(main_settings)
        main_bit = f"Connected {n} argument{'s' if n != 1 else ''} from the main file."
    elif discovery_errors:
        main_bit = "Couldn't load the main file automatically."
    else:
        main_bit = "No runnable entry point found yet."
    sm_bit = "Snakemake workflow connected." if sm_config_path else None
    discovery_summary = f"{main_bit} {sm_bit}" if sm_bit else main_bit

    settings = {
        "path": repo_path,
        "docs_url": docs_url or "",
        **main_settings,
        **sm_settings,
    }

    has_run_target = main_func is not None or sm_config_path is not None
    default_tips = (
        ["/wizard", "/run", "/settings", "/reset", "/home", "/help"]
        if has_run_target
        else ["/settings", "/reset", "/home", "/help"]
    )
    default_tips.extend(["/install", "/docs"])
    if main_func is not None:
        default_tips.append("/scaffold")

    from .config import local_settings_path

    cli = GenericCLI(
        app_name=app_name,
        ascii_art=clz.get("ascii_art"),
        accent_color=clz.get("accent_color", "#d97757"),
        settings=settings,
        config_path=str(local_settings_path(repo_path)),
        tips=clz.get("tips") if clz.get("tips") else default_tips,
        updates=clz.get("updates"),
        discovery_summary=discovery_summary,
    )
    cli.arg_meta = arg_meta

    # Config persists settings across runs (so a value the user explicitly
    # set via /settings, e.g. username="test", survives between sessions).
    # But that means a key first discovered with no default (None) stays
    # None forever in the persisted store, even after main()'s source gains
    # an explicit default later (e.g. clean=True, verbosity=3). Backfill: if
    # the persisted value is still None, adopt the freshly discovered
    # default instead of leaving it stuck.
    for key, val in {**main_settings, **sm_settings}.items():
        if cli.config.get(key) is None and val is not None:
            cli.config.set(key, val)

    # Only show /run if there's actually something to run.
    if not has_run_target:
        cli._commands.pop("/run", None)
        if "/run" in cli.tips:
            cli.tips = [t for t in cli.tips if t != "/run"]

    if has_run_target:
        @cli.command("/run", "Run the project's main with current arguments")
        def _cmd_run(prompt):
            if main_func is not None:
                with cli.status("Running main()..."):
                    if call_style == "argv":
                        argv = ["clizard"]
                        for name, meta in arg_meta.items():
                            flag = meta.get("flag")
                            if not flag:
                                continue
                            val = cli.config.get(name)
                            if val is None:
                                continue
                            if meta.get("is_flag"):
                                if val:
                                    argv.append(flag)
                            else:
                                argv.extend([flag, str(val)])
                        old_argv = sys.argv
                        sys.argv = argv
                        try:
                            result = main_func()
                        finally:
                            sys.argv = old_argv
                    else:
                        call_kwargs = {k: cli.config.get(k) for k in main_settings}
                        result = main_func(**call_kwargs)
                if result is not None:
                    cli.assistant_message(str(result))

            if sm_config_path is not None:
                current_sm = {k: cli.config.get(k) for k in sm_settings}
                write_snakemake_config(sm_config_path, current_sm)
                cmd = ["snakemake", "--configfile", str(sm_config_path), "--cores", "all"]
                console_cmd = " ".join(cmd)
                try:
                    with cli.status(f"Running: {console_cmd}"):
                        result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
                    output = (result.stdout + result.stderr).strip()
                    shown = output[-2000:]
                    note = "\n[...output truncated...]" if len(output) > 2000 else ""
                    cli.assistant_message(f"```\n$ {console_cmd}\n{shown}\n```{note}")
                except FileNotFoundError:
                    cli.error("snakemake is not installed or not on PATH.")

    if main_func is not None:
        @cli.command("/scaffold", "Generate clizard_main.py wrapping this project's main()")
        def _cmd_scaffold(prompt):
            try:
                out_path = generate_clizard_main(repo_path)
                cli.assistant_message(f"Wrote `{out_path}`. Run it with:\n\n```\npython {out_path.name}\n```")
            except RuntimeError as e:
                cli.error(str(e))

    return cli


def main():
    args = parse_args(app_name="clizard")
    cli = build_cli(repo_path=args.path or ".")
    if args.model:
        cli.config.set("model", args.model)
    cli.run()


if __name__ == "__main__":
    main()
