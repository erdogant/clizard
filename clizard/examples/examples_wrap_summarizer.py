"""Example: expose summarizer.main(...) through a clizard interface.

Run:
    python wrap_summarizer.py --input-path notes.txt --max-words 20
"""
from clizard import GenericCLI, parse_args
from summarizer import main as summarize

# 1. Declare the script's own arguments as extra CLI flags.
EXTRA_ARGS = [
    {"flags": ["--input-path"], "kwargs": {"default": None, "help": "Path to input text file"}},
    {"flags": ["--max-words"], "kwargs": {"type": int, "default": 50, "help": "Max words to keep"}},
    {"flags": ["--uppercase"], "kwargs": {"action": "store_true", "help": "Uppercase the output"}},
]


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

    # 2. A command that calls main() using whatever is currently in settings.
    @cli.command("/run", "Run the summarizer with current settings")
    def cmd_run(prompt):
        path = cli.config.get("input_path")
        if not path:
            cli.error("No input_path set. Use: /settings set input_path <file>")
            return
        cli.status(f"Summarizing {path}...")
        result = summarize(
            input_path=path,
            max_words=cli.config.get("max_words"),
            uppercase=cli.config.get("uppercase"),
        )
        cli.assistant_message(result)

    # 3. Optional: also let free-text input trigger main() directly,
    #    treating the typed text as the input_path.
    def handler(prompt, cli):
        return summarize(
            input_path=prompt,
            max_words=cli.config.get("max_words"),
            uppercase=cli.config.get("uppercase"),
        )

    cli.handler = handler
    return cli


def main():
    args = parse_args(app_name="Summarizer CLI", extra_args=EXTRA_ARGS)
    cli = build_cli(args)
    cli.run()


if __name__ == "__main__":
    main()
