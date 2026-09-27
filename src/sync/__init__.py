import os
from pathlib import Path

def find_git_root(path=None):
    if path is None:
        path = Path.cwd()
    path = Path(path).resolve()
    for parent in [path] + list(path.parents):
        if (parent / ".git").is_dir():
            return parent
    return None

def chdir_to_git_root():
    root = find_git_root()
    if root:
        os.chdir(root)
        return True
    return False
