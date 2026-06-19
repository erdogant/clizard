"""Example: how another script/project reuses clizard for its own tool."""
from clizard import GenericCLI, parse_args

EXTRA_ARGS = [
    {"flags": ["--temperature"], "kwargs": {"type": float, "default": None, "help": "Sampling temperature"}},
]


def my_handler(prompt, cli):
    # plug in real LLM call here
    model = cli.config.get("model")
    return f"[{model}] you said: **{prompt}**"


def main():
    args = parse_args(app_name="LLMlight", extra_args=EXTRA_ARGS)

    cli = GenericCLI(
        app_name=args.name or "LLMlight",
        ascii_art=r"""
   /\_/\
  ( o.o )
   > ^ <
""",
        settings={"model": "google/gemma-26B-a4B", "path": "C:/LLMlight", "temperature": 0.7},
        config_path=args.config,
        handler=my_handler,
        tips=["/init", "/help", "generate documentation"],
        updates=["Agent system improvements", "Documentation generation", "Local model support"],
    )
    cli.config.update_from_args({"model": args.model, "path": args.path, "temperature": args.temperature})

    # custom command specific to this project
    @cli.command("/init", "Initialize a new project")
    def cmd_init(prompt):
        cli.assistant_message(f"Initialized project at `{cli.config.get('path')}`")

    cli.run()


if __name__ == "__main__":
    main()
