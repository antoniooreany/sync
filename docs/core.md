# Core Module Documentation

## Purpose and Design

The `core.py` module is designed to automate the setup of Gitlint-related configurations within a git repository. It provides functions to check if the current directory is a git root, generate standard Gitlint configuration files, create a cross-platform Python-based commit-msg hook script, and set up a GitHub Actions workflow for linting commits.

The design ensures that each function performs a specific task while maintaining a clean separation of concerns and error handling. The module uses subprocesses to interact with Git commands and pathlib for file path manipulation, ensuring compatibility across different platforms.

## Class and Function Reference

### is_git_root()

**Purpose:**
Check if the current working directory is a git repository root.

**Parameters:** None

**Return Type:** bool

**Exceptions Raised:**
- `subprocess.CalledProcessError`: If any Git command fails.
- `FileNotFoundError`: If the `.git` directory does not exist in the current directory.

### generate_gitlint_config()

**Purpose:**
Generate the standard .gitlint configuration string.

**Parameters:** None

**Return Type:** str

**Exceptions Raised:** None

### generate_commit_msg_hook()

**Purpose:**
Generate a cross-platform Python-based commit-msg hook script.

**Parameters:** None

**Return Type:** str

**Exceptions Raised:** None

### generate_workflow_config()

**Purpose:**
Generate the GitHub Actions commit-lint.yml workflow string.

**Parameters:** None

**Return Type:** str

**Exceptions Raised:** None

### write_configs(target_dir: Path, force: bool = False) -> list[Path]

**Purpose:**
Write all gitlint-related configuration files with safety checks.

**Parameters:**
- `target_dir` (Path): The target directory where the configuration files should be written.
- `force` (bool, optional): If True, overwrite existing configuration files without asking. Default is False.

**Return Type:** list[Path]

**Exceptions Raised:**
- `FileNotFoundError`: If the `.git` directory does not exist in the target directory.
- `FileExistsError`: If any of the configuration files already exist and `force` is False.

## Practical Usage Examples

### Example 1: Check if Current Directory is a Git Root

```python
from core import is_git_root

if is_git_root():
    print("This is a git repository root.")
else:
    print("This is not a git repository root.")
```

### Example 2: Generate and Write Configuration Files

```python
from pathlib import Path
from core import write_configs

target_directory = Path("/path/to/your/git/repo")
config_files_written = write_configs(target_directory)

print(f"Configuration files written to: {', '.join(str(file) for file in config_files_written)}")
```

### Example 3: Overwrite Existing Configuration Files

```python
from pathlib import Path
from core import write_configs

target_directory = Path("/path/to/your/git/repo")
config_files_written = write_configs(target_directory, force=True)

print(f"Configuration files overwritten and written to: {', '.join(str(file) for file in config_files_written)}")
```

These examples demonstrate how to use the functions provided by `core.py` to check if a directory is a git root, generate configuration files, and handle existing configurations with or without force mode.
