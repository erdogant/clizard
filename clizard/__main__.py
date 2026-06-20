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
    clz = ensure_clizard_file(repo_path)

    app_name = clz.get("app_name") or proj_info.get("name") or git_info.get("github_repo") or "clizard"
    docs_url = clz.get("docs_url") or proj_info.get("docs_url")

    module, main_func, entry_file = find_main(repo_path)
    main_settings, arg_meta, call_style = settings_from_main(main_func) if main_func else ({}, {}, "kwargs")

    sm_config_path = find_snakemake_config(repo_path)
    sm_settings = settings_from_snakemake_config(sm_config_path) if sm_config_path else {}

    settings = {
        # "path": repo_path,
        # "github_user": git_info.get("github_user") or "",
        # "github_repo": git_info.get("github_repo") or "",
        # "remote_url": git_info.get("remote_url") or "",
        # "default_branch": git_info.get("default_branch") or "main",
        "docs_url": docs_url or "",
        **main_settings,
        **sm_settings,
    }

    has_run_target = main_func is not None or sm_config_path is not None
    default_tips = ["/wizard", "/run", "/settings", "/docs", "/help"] if has_run_target else ["/settings", "/help"]

    cli = GenericCLI(
        app_name=app_name,
        ascii_art=clz.get("ascii_art"),
        accent_color=clz.get("accent_color", "#d97757"),
        settings=settings,
        tips=clz.get("tips") if clz.get("tips") else default_tips,
        updates=clz.get("updates"),
    )
    cli.arg_meta = arg_meta

    # Only show /run if there's actually something to run.
    if not has_run_target:
        cli._commands.pop("/run", None)
        if "/run" in cli.tips:
            cli.tips = [t for t in cli.tips if t != "/run"]

    if has_run_target:
        @cli.command("/run", "Run the project's main()/Snakemake workflow with current settings")
        def _cmd_run(prompt):
            if main_func is not None:
                cli.status("Running main()...")
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
                cli.status(f"Running: {console_cmd}")
                try:
                    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
                    output = (result.stdout + result.stderr).strip()
                    cli.assistant_message(f"```\n$ {console_cmd}\n{output[-2000:]}\n```")
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
    # if args.model:
    #     cli.config.set("model", args.model)
    cli.run()


if __name__ == "__main__":
    main()
