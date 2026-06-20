"""Default console-script entry point: `clizard`."""
from .cli_args import parse_args
from .core import GenericCLI


def main():
    args = parse_args(app_name="GenericCLI")
    overrides = {"model": args.model, "path": args.path}
    cli = GenericCLI(
        app_name=args.name or "GenericCLI",
        config_path=args.config,
    )
    cli.config.update_from_args(overrides)
    cli.run()


if __name__ == "__main__":
    main()
