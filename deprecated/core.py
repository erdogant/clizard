"""Generic Claude-style rich CLI, reusable across projects."""
import time
from rich import box
from rich.align import Align
from rich.console import Console, Group
from rich.live import Live
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.spinner import Spinner
from rich.table import Table
from rich.text import Text

from .config import Config

console = Console()

DEFAULT_ASCII = r"""
  .-.
 |o o|
 | = |
/|___|\
"""


class GenericCLI:
    """Reusable rich-based chat CLI.

    Pass `handler(prompt, cli) -> str` to process user input, or subclass
    and override `handle(prompt)`. Register extra slash-commands with
    `@cli.command("/foo")`.
    """

    def __init__(
        self,
        app_name="Generic CLI",
        ascii_art=None,
        accent_color="#d97757",
        dim_color="#9ca3af",
        user_color="#3b82f6",
        settings: dict = None,
        config_path: str = None,
        handler=None,
        tips: list = None,
        updates: list = None,
    ):
        self.app_name = app_name
        self.ascii_art = ascii_art or DEFAULT_ASCII
        self.ACCENT = accent_color
        self.DIM = dim_color
        self.USER = user_color
        self.handler = handler
        self.tips = tips or ["/help", "/settings"]
        self.updates = updates or ["Initial release"]

        defaults = {"model": "default-model", "path": "."}
        if settings:
            defaults.update(settings)
        self.config = Config(app_name, defaults=defaults, config_path=config_path)

        self._commands = {}
        self._register_builtins()

    # ---------- command registry ----------
    def command(self, name, help_text=""):
        """Decorator: register a slash-command. fn(self, prompt) -> None."""
        def deco(fn):
            self._commands[name] = (fn, help_text)
            return fn
        return deco

    def register_command(self, name, fn, help_text=""):
        self._commands[name] = (fn, help_text)

    def _register_builtins(self):
        self.register_command("/wizard", self._cmd_wizard, "Step through all settings, then optionally /run")
        self.register_command("/help", self._cmd_help, "Show available commands")
        self.register_command("/clear", self._cmd_clear, "Clear the terminal")
        self.register_command("/settings", self._cmd_settings, "View or edit settings")
        self.register_command("/exit", self._cmd_exit, "Exit the session")
        self.register_command("/quit", self._cmd_exit, "Exit the session")

    def _cmd_help(self, prompt):
        lines = "\n".join(f"* `{name}` - {desc}" for name, (_, desc) in sorted(self._commands.items()))
        self.assistant_message(f"### Available Commands\n{lines}")

    def _cmd_clear(self, prompt):
        console.clear()

    def _cmd_exit(self, prompt):
        console.print(f"[dim]Goodbye! Thanks for using {self.app_name}.[/dim]")
        raise SystemExit(0)

    @staticmethod
    def _cast_value(raw: str, current):
        """Cast a string CLI value to match the type of the existing setting."""
        if isinstance(current, bool):
            return raw.strip().lower() in {"1", "true", "yes", "on"}
        if isinstance(current, int) and not isinstance(current, bool):
            try:
                return int(raw)
            except ValueError:
                return raw
        if isinstance(current, float):
            try:
                return float(raw)
            except ValueError:
                return raw
        if raw.lower() == "none":
            return None
        return raw

    def _cmd_settings(self, prompt):
        # /settings              -> interactive view + optional edit
        # /settings set k v...   -> direct set (v can contain spaces)
        parts = prompt.split(maxsplit=3)
        if len(parts) >= 3 and parts[1] == "set":
            key = parts[2]
            raw_value = parts[3] if len(parts) > 3 else ""
            current = self.config.get(key)
            value = self._cast_value(raw_value, current)
            self.config.set(key, value)
            console.print(f"[dim]Set {key} = {value!r}[/dim]")
            return

        self._show_settings_table()
        try:
            answer = Prompt.ask("  ✏️  Edit a setting now?", choices=["y", "n"], default="n")
        except (KeyboardInterrupt, EOFError):
            return
        if answer != "y":
            return

        keys = list(self.config.settings.keys())
        key = Prompt.ask(f"  Which key? [{'/'.join(keys)}]")
        if key not in self.config.settings:
            self.error(f"Unknown key: {key}")
            return
        current = self.config.get(key)
        raw_value = Prompt.ask(f"  New value for [bold]{key}[/bold]", default=str(current))
        value = self._cast_value(raw_value, current)
        self.config.set(key, value)
        console.print(f"[dim]Set {key} = {value!r}[/dim]")
        self._show_settings_table()

    def _cmd_wizard(self, prompt):
        console.print(f"[bold {self.ACCENT}]Setup Wizard[/bold {self.ACCENT}] — press Enter to keep the current value.\n")
        meta = getattr(self, "arg_meta", {}) or {}

        for key in list(self.config.settings.keys()):
            current = self.config.get(key)
            info = meta.get(key, {})
            help_text = info.get("help")
            choices = info.get("choices")

            label = f"  [bold]{key}[/bold]"
            if help_text:
                label += f" [dim]({help_text})[/dim]"
            if choices:
                label += f" [dim]choices: {choices}[/dim]"

            while True:
                raw_value = Prompt.ask(label, default=str(current))
                caster = info.get("type")
                if caster and current is None:
                    try:
                        value = caster(raw_value)
                    except (ValueError, TypeError):
                        value = self._cast_value(raw_value, current)
                else:
                    value = self._cast_value(raw_value, current)
                if choices and value not in choices:
                    self.error(f"Invalid value {value!r}. Choose from {choices}.")
                    continue
                break

            self.config.set(key, value)

        console.print()
        self._show_settings_table()

        if "/run" in self._commands:
            try:
                answer = Prompt.ask("  ▶️  Start /run now?", choices=["y", "n"], default="y")
            except (KeyboardInterrupt, EOFError):
                return
            if answer == "y":
                self._commands["/run"][0]("/run")
        else:
            console.print("[dim]No /run command registered.[/dim]")

    def _show_settings_table(self):
        table = Table(
            title="Current Configuration Settings",
            box=box.ROUNDED,
            border_style=self.ACCENT,
            show_lines=False,
        )
        table.add_column("Parameter", style=self.ACCENT)
        table.add_column("Current Value")
        for k, v in self.config.settings.items():
            table.add_row(str(k), str(v))
        console.print(table)

    # ---------- rendering ----------
    def welcome(self):
        console.print()
        header_text = Text()
        header_text.append(f" {self.app_name} \n", style=f"bold {self.ACCENT} reverse")
        header_text.append(self.ascii_art, style=self.ACCENT)
        header_text.append(f"\nmodel: ", style=f"dim {self.DIM}")
        header_text.append(f"{self.config.get('model')}\n", style="italic")
        header_text.append(f"path:  ", style=f"dim {self.DIM}")
        header_text.append(f"{self.config.get('path')}\n", style="dim")

        centered_header = Align.center(header_text, vertical="middle")

        grid = Table.grid(expand=True, padding=(0, 4))
        grid.add_column(ratio=1)
        grid.add_column(ratio=1)

        tips_md = "\n".join(f"  • [cyan]{t}[/cyan]" for t in self.tips)
        updates_md = "\n".join(f"• {u}" for u in self.updates)

        tips_text = Text.from_markup(f"[bold {self.ACCENT}]Getting started[/bold {self.ACCENT}]\n\nType commands like:\n{tips_md}")
        updates_text = Text.from_markup(f"[bold {self.ACCENT}]What's new[/bold {self.ACCENT}]\n\n{updates_md}")

        grid.add_row(tips_text, updates_text)

        layout_group = Group(centered_header, "─" * 64, "", grid)

        console.print(
            Align.center(
                Panel(layout_group, box=box.ROUNDED, border_style=self.ACCENT, padding=(2, 4), width=76)
            )
        )
        console.print()

    def user_message(self, text):
        console.print(f"\n[bold {self.USER}]👤 You[/bold {self.USER}] › {text}\n")

    def assistant_message(self, text):
        console.print(f"[bold {self.ACCENT}]🤖 Assistant[/bold {self.ACCENT}]")
        console.print("═" * 40, style=self.ACCENT)
        console.print(Markdown(text))
        console.print("═" * 40, style="dim")
        console.print()

    def status(self, text, duration=1.2):
        with Live(Spinner("dots", text=f"[dim]{text}[/dim]", style=self.ACCENT), refresh_per_second=12, transient=True):
            time.sleep(duration)

    def tool_call(self, tool_name):
        console.print(f"  [dim]🛠️ Running tool:[/dim] [italic cyan]{tool_name}[/italic cyan]...")

    def error(self, text):
        console.print(f"[bold red]✕ Error:[/bold red] {text}")

    # ---------- main loop ----------
    def handle(self, prompt):
        """Default handler if none supplied; override or pass `handler=`."""
        if self.handler:
            return self.handler(prompt, self)
        return f"Successfully captured your request: **'{prompt}'**."

    def run(self):
        self.welcome()
        while True:
            try:
                prompt = Prompt.ask(f"[bold {self.ACCENT}]❯[/bold {self.ACCENT}]").strip()
                if not prompt:
                    continue

                cmd = prompt.split(maxsplit=1)[0]
                if cmd in self._commands:
                    fn, _ = self._commands[cmd]
                    fn(prompt)
                    continue
                if cmd.startswith("/"):
                    self.error(f"Unknown command: {cmd} (type /help for a list)")
                    continue

                self.user_message(prompt)
                self.status("Thinking...")
                reply = self.handle(prompt)
                self.assistant_message(reply)

            except SystemExit:
                break
            except (KeyboardInterrupt, EOFError):
                console.print("\n[dim]Session terminated gracefully.[/dim]")
                break
