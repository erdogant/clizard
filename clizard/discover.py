"""Find a repo's entry-point main() function and turn its signature into
editable CLI settings, without needing argparse to be structured any
particular way.
"""
import importlib.util
import inspect
import sys
import re
from pathlib import Path
from .git_info import get_git_info


"""Locate the most likely entry-point .py file in a repo."""
def _find_entry_file(repo_path="."):
    repo_path = Path(repo_path)
    repo_name = repo_path.name

    CANDIDATE_FILENAMES = [
        "__main__.py",
        "main.py",
        f"{repo_name}.py",
    ]

    # Add GitHub repo name if available
    gitinfo = get_git_info()
    if gitinfo.get("github_repo"):
        CANDIDATE_FILENAMES.append(f"{gitinfo['github_repo']}.py")

    CANDIDATE_FILENAMES = list(dict.fromkeys(CANDIDATE_FILENAMES))

    # --- 1. Direct top-level candidates ---
    for name in CANDIDATE_FILENAMES:
        # subfolder match
        for candidate in repo_path.glob(f"*/{name}"):
            return candidate

        # direct match
        direct = repo_path / name
        if direct.exists():
            return direct

    # --- 2. Find file that actually handles arguments ---
    ARG_PATTERNS = [
        r"sys\.argv",
        r"argparse",
        r"ArgumentParser",
        r"click\.command",
        r"typer\.run",
    ]

    MAIN_PATTERN = r"def\s+main\s*\("

    for py_file in repo_path.rglob("*.py"):
        if ".git" in py_file.parts or "site-packages" in py_file.parts:
            continue

        try:
            text = py_file.read_text(errors="ignore")
        except OSError:
            continue

        # must define main()
        if not re.search(MAIN_PATTERN, text):
            continue

        # must reference arguments
        if any(re.search(p, text) for p in ARG_PATTERNS):
            return py_file

    # --- 3. Fallback: any file with main() and __name__ check ---
    for py_file in repo_path.rglob("*.py"):
        if ".git" in py_file.parts or "site-packages" in py_file.parts:
            continue

        try:
            text = py_file.read_text(errors="ignore")
        except OSError:
            continue

        if "__name__" in text and "def main(" in text:
            return py_file

    return None

def _load_module(py_file: Path):
    """Load py_file as a module, preserving package context so that any
    relative imports (`from . import foo`, `from .bar import baz`) inside
    it actually resolve, instead of raising ImportError.

    If py_file lives inside a package (its directory has an __init__.py),
    we import it as a real submodule of that package via importlib, with
    the package's *parent* directory on sys.path. Otherwise we fall back
    to loading it as a standalone module.
    """
    parent = py_file.parent

    if (parent / "__init__.py").exists():
        package_name = parent.name
        package_parent_dir = str(parent.parent)
        sys.path.insert(0, package_parent_dir)
        try:
            module_name = f"{package_name}.{py_file.stem}"
            # Drop any stale cached import from a previous discovery run.
            sys.modules.pop(module_name, None)
            sys.modules.pop(package_name, None)
            module = importlib.import_module(module_name)
        finally:
            sys.path.remove(package_parent_dir)
        return module

    module_name = f"_clizard_discovered_{py_file.stem}"
    spec = importlib.util.spec_from_file_location(module_name, py_file)
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(py_file.parent))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
    return module


def find_main(repo_path="."):
    """Return (module, main_func, file_path) or (None, None, None)."""
    py_file = _find_entry_file(repo_path)
    if py_file is None:
        return None, None, None

    try:
        module = _load_module(py_file)
    except Exception as e:
        print(f"clizard: failed to import {py_file} to discover main(): {e!r}", file=sys.stderr)
        return None, None, py_file

    main_func = getattr(module, "main", None)
    if main_func is None or not callable(main_func):
        return module, None, py_file

    return module, main_func, py_file


def _extract_argparse_settings(main_func):
    """Many main()s take *no* parameters and instead build their own
    argparse.ArgumentParser() internally, reading from sys.argv. In that
    case there's nothing in the signature to inspect, but the settings
    are sitting right there in the source as `parser.add_argument(...)`
    calls. Parse the function's source with `ast` and recover them.

    Returns (settings, arg_meta). arg_meta entries carry a "flag" (e.g.
    "--username") and "is_flag" (True for store_true/store_false), which
    the generated /run command uses to rebuild sys.argv before calling
    main() with no arguments, since main() will parse it itself.
    """
    import ast

    settings = {}
    arg_meta = {}
    try:
        source = inspect.getsource(main_func)
    except (OSError, TypeError):
        return settings, arg_meta

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return settings, arg_meta

    parser_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            func = node.value.func
            func_name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", None)
            if func_name == "ArgumentParser":
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        parser_names.add(target.id)

    if not parser_names:
        return settings, arg_meta

    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument"):
            continue
        obj = node.func.value
        if not (isinstance(obj, ast.Name) and obj.id in parser_names):
            continue

        flags = [a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str)]
        if not flags:
            continue
        long_flags = [f for f in flags if f.startswith("--")]
        flag = long_flags[0] if long_flags else flags[-1]
        dest_name = flag.lstrip("-").replace("-", "_")

        kw = {}
        type_name = None
        for keyword in node.keywords:
            if keyword.arg is None:
                continue
            if keyword.arg == "type" and isinstance(keyword.value, ast.Name):
                type_name = keyword.value.id  # e.g. "int", "str", "float"
                continue
            try:
                kw[keyword.arg] = ast.literal_eval(keyword.value)
            except (ValueError, SyntaxError):
                kw[keyword.arg] = None

        dest_name = kw.get("dest", dest_name)
        action = kw.get("action")
        is_flag = action in ("store_true", "store_false")
        default = kw.get("default")
        if is_flag and default is None:
            default = (action == "store_false")

        settings[dest_name] = default
        arg_meta[dest_name] = {
            "choices": kw.get("choices"),
            "type": type_name,
            "help": kw.get("help"),
            "flag": flag,
            "is_flag": is_flag,
        }

    return settings, arg_meta


def settings_from_main(main_func):
    """Inspect main()'s signature -> (settings dict, arg_meta dict, call_style).

    call_style is "kwargs" when main() takes plain keyword parameters
    (settings become those params, and /run calls main(**settings)), or
    "argv" when main() takes no usable parameters but builds its own
    argparse.ArgumentParser() internally (settings are recovered from its
    add_argument() calls via AST, and /run rebuilds sys.argv before
    calling main() with no arguments).
    """
    settings = {}
    arg_meta = {}
    try:
        sig = inspect.signature(main_func)
    except (TypeError, ValueError):
        sig = None

    if sig is not None:
        for name, param in sig.parameters.items():
            if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
                continue
            default = None if param.default is inspect.Parameter.empty else param.default
            annotation = None if param.annotation is inspect.Parameter.empty else param.annotation
            settings[name] = default
            arg_meta[name] = {
                "choices": None,
                "type": annotation if callable(annotation) else None,
                "help": None,
                "flag": None,
                "is_flag": False,
            }

    if settings:
        return settings, arg_meta, "kwargs"

    # main() took no usable params -- see if it builds an argparse parser
    # internally instead, and recover settings from that.
    argv_settings, argv_meta = _extract_argparse_settings(main_func)
    if argv_settings:
        return argv_settings, argv_meta, "argv"

    return settings, arg_meta, "kwargs"


SNAKEMAKE_CONFIG_CANDIDATES = [
    "config.yaml", "config.yml",
    "config/config.yaml", "config/config.yml",
    "workflow/config.yaml", "workflow/config.yml",
]


def find_snakefile(repo_path="."):
    repo_path = Path(repo_path)
    for name in ("Snakefile", "workflow/Snakefile"):
        candidate = repo_path / name
        if candidate.exists():
            return candidate
    matches = list(repo_path.rglob("Snakefile"))
    return matches[0] if matches else None


def find_snakemake_config(repo_path="."):
    """Locate a Snakemake config YAML: explicit `configfile:` in the
    Snakefile takes priority, else common default paths are tried.
    """
    repo_path = Path(repo_path)
    snakefile = find_snakefile(repo_path)

    if snakefile and snakefile.exists():
        try:
            text = snakefile.read_text(errors="ignore")
        except OSError:
            text = ""
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("configfile:"):
                rel = line.split(":", 1)[1].strip().strip("'\"")
                candidate = (snakefile.parent / rel).resolve()
                if candidate.exists():
                    return candidate

    for rel in SNAKEMAKE_CONFIG_CANDIDATES:
        candidate = repo_path / rel
        if candidate.exists():
            return candidate

    return None


def settings_from_snakemake_config(config_path):
    """Load a Snakemake config YAML -> flat settings dict (keys prefixed
    'sm_' to avoid clashing with main()'s own argument names).
    """
    settings = {}
    if config_path is None:
        return settings
    try:
        import yaml
    except ImportError:
        return settings

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f) or {}
    except (OSError, yaml.YAMLError):
        return settings

    if not isinstance(data, dict):
        return settings

    for key, value in data.items():
        settings[f"sm_{key}"] = value

    return settings


def write_snakemake_config(config_path, settings: dict):
    """Write back sm_-prefixed settings into the Snakemake config YAML."""
    import yaml

    data = {k[3:]: v for k, v in settings.items() if k.startswith("sm_")}
    with open(config_path, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False)
