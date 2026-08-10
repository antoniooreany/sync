"""
Git access layer.
"""
import subprocess

def get_current_branch() -> str:
    """Return the current git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, encoding="utf-8", check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git error: {e.stderr.strip() if e.stderr else 'Unknown error'}") from e
    except FileNotFoundError:
        raise RuntimeError("Git executable not found in PATH")

def get_diff(base: str, head: str) -> str:
    """Return the diff between base and head branches."""
    try:
        result = subprocess.run(
            ["git", "diff", f"{base}..{head}"],
            capture_output=True, text=True, encoding="utf-8", check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git diff error: {e.stderr.strip() if e.stderr else 'Unknown error'}") from e
    except FileNotFoundError:
        raise RuntimeError("Git executable not found in PATH")
def get_commits(base: str, head: str) -> list[str]:
    """Return the list of commits (oneline) between base and head branches."""
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", f"{base}..{head}"],
            capture_output=True, text=True, encoding="utf-8", check=True
        )
        return [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git log error: {e.stderr.strip() if e.stderr else 'Unknown error'}") from e
    except FileNotFoundError:
        raise RuntimeError("Git executable not found in PATH")

def get_changed_files(base: str, head: str) -> list[str]:
    """Return the list of changed files between base and head branches."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base}...{head}"],
            capture_output=True, text=True, encoding="utf-8", check=True
        )
        return [line.strip() for line in result.stdout.strip().splitlines() if line.strip()]
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Git diff error: {e.stderr.strip() if e.stderr else 'Unknown error'}") from e
    except FileNotFoundError:
        raise RuntimeError("Git executable not found in PATH")
