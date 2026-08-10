"""
GitHub interaction layer using gh CLI.
"""
import subprocess
import json

def check_auth() -> bool:
    """Check if gh CLI is authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True, text=True, encoding="utf-8"
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def find_open_pr(base: str, head: str) -> dict:
    """Find an open PR for the given base and head branches. Returns dict with PR info or None."""
    if not check_auth():
        raise RuntimeError("GitHub CLI is not authenticated or not found")
        
    result = subprocess.run(
        ["gh", "pr", "list", "--base", base, "--head", head, "--state", "open", "--json", "number,url,title,body"],
        capture_output=True, text=True, encoding="utf-8", check=True
    )
    prs = json.loads(result.stdout)
    if not prs:
        return None
    if len(prs) > 1:
        raise ValueError(f"Found multiple open PRs for base {base} and head {head}")
    return prs[0]

def create_pr(title: str, body: str, base: str, head: str) -> dict:
    """Create a new PR."""
    if not check_auth():
        raise RuntimeError("GitHub CLI is not authenticated or not found")
        
    result = subprocess.run(
        ["gh", "pr", "create", "--base", base, "--head", head, "--title", title, "--body", body],
        capture_output=True, text=True, encoding="utf-8", check=True
    )
    url = result.stdout.strip()
    return {"url": url}

def update_pr(pr_number: str, title: str, body: str) -> dict:
    """Update an existing PR."""
    if not check_auth():
        raise RuntimeError("GitHub CLI is not authenticated or not found")
        
    subprocess.run(
        ["gh", "pr", "edit", str(pr_number), "--title", title, "--body", body],
        capture_output=True, text=True, encoding="utf-8", check=True
    )
    return {"number": pr_number}

def add_labels(pr_number: str, labels: list[str]) -> None:
    """Apply GitHub labels to a PR. Creates labels if they don't exist."""
    if not check_auth():
        raise RuntimeError("GitHub CLI is not authenticated or not found")

    if not labels:
        return

    # Ensure labels exist in the repository
    for label in labels:
        subprocess.run(
            ["gh", "label", "create", label],
            capture_output=True, text=True, encoding="utf-8"
        )

    cmd = ["gh", "pr", "edit", str(pr_number)]
    for label in labels:
        cmd.extend(["--add-label", label])

    subprocess.run(
        cmd,
        capture_output=True, text=True, encoding="utf-8", check=True
    )


