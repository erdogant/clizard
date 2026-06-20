"""Read project metadata out of pyproject.toml."""
from pathlib import Path

try:
    import tomllib  # py3.11+
except ImportError:
    import tomli as tomllib  # fallback


def get_project_info(repo_path="."):
    """Return dict with: name, version, docs_url, requirements (list)."""
    info = {"name": None, "version": None, "docs_url": None, "requirements": []}

    pyproject = Path(repo_path) / "pyproject.toml"
    if pyproject.exists():
        try:
            with open(pyproject, "rb") as f:
                data = tomllib.load(f)
        except Exception:
            data = {}

        project = data.get("project", {})
        info["name"] = project.get("name")
        info["version"] = project.get("version")
        info["requirements"] = project.get("dependencies", [])
        info["description"] = project.get("description", "")

        urls = project.get("urls", {})
        for key in ("Documentation", "documentation", "Docs", "docs"):
            if key in urls:
                info["docs_url"] = urls[key]
                break

    req_file = Path(repo_path) / "requirements.txt"
    if not info["requirements"] and req_file.exists():
        info["requirements"] = [
            line.strip() for line in req_file.read_text().splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]

    return info
