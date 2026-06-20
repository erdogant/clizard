"""Read repo identity straight out of .git/config."""
import configparser
import re
from pathlib import Path


def _parse_remote_url(url: str):
    """Return (host, user, repo) from a git remote URL (ssh or https)."""
    url = url.strip().rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]

    m = re.match(r"git@([^:]+):([^/]+)/(.+)$", url)  # git@github.com:user/repo
    if not m:
        m = re.match(r"https?://([^/]+)/([^/]+)/(.+)$", url)  # https://github.com/user/repo
    if not m:
        return None, None, None

    host, user, repo = m.group(1), m.group(2), m.group(3)
    return host, user, repo


def get_git_info(repo_path="."):
    """Inspect <repo_path>/.git/config and return repo metadata.

    Returns dict with: host, github_user, github_repo, remote_url,
    default_branch. Any field defaults to None/"" if not found.
    """
    info = {
        "host": None,
        "github_user": None,
        "github_repo": None,
        "remote_url": None,
        "default_branch": "main",
    }

    git_config = Path(repo_path) / ".git" / "config"
    if not git_config.exists():
        return info

    parser = configparser.ConfigParser(strict=False)
    try:
        parser.read(git_config)
    except configparser.Error:
        return info

    for section in parser.sections():
        if section.startswith('remote "'):
            url = parser.get(section, "url", fallback=None)
            if url:
                info["remote_url"] = url
                host, user, repo = _parse_remote_url(url)
                info["host"] = host
                info["github_user"] = user
                info["github_repo"] = repo
                break  # first remote (usually 'origin') wins

    head_file = Path(repo_path) / ".git" / "HEAD"
    if head_file.exists():
        head = head_file.read_text().strip()
        if head.startswith("ref: refs/heads/"):
            info["default_branch"] = head.split("refs/heads/")[-1]

    return info
