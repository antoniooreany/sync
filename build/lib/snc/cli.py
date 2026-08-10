"""snc – Shell command runner utility."""


def run_cmd(args: list) -> int:
    """Run a shell command and return its exit code.

    Returns 127 if the command is not found (POSIX convention).
    """
    import subprocess

    try:
        result = subprocess.run(args, check=False)
        return result.returncode
    except FileNotFoundError:
        return 127
