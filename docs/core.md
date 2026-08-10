## Module Description

The `gitflow_sync` module provides a set of functions to interact with Git repositories following the Gitflow branching model. It includes functionalities to check repository compliance, start new branches, and finish branches according to Gitflow rules.

### Purpose
To automate and ensure adherence to Gitflow practices within a Python project, making it easier for developers to manage feature branches, bug fixes, hotfixes, releases, and more following the well-established Gitflow workflow.

### Design
The module is designed as a collection of utility functions that interact with Git using subprocess calls. It checks repository state, validates branch names, and performs operations like creating, merging, and tagging branches to ensure compliance with Gitflow standards.

## Class and Function Reference

### `run_git(args: list[str]) -> str`
**Purpose:** Execute a git command and return its standard output.
**Parameters:**
- `args`: List of string arguments representing the git command to execute.
**Return Type:** String containing the standard output of the executed git command.
**Exceptions Raised:** Raises `subprocess.CalledProcessError` if the git command fails, or `FileNotFoundError` if 'git' is not found.

### `is_git_repo() -> bool`
**Purpose:** Check if the current directory is inside a valid Git repository.
**Return Type:** Boolean indicating whether the current directory is a Git repository.
**Exceptions Raised:** No exceptions raised.

### `get_current_branch() -> str`
**Purpose:** Retrieve the name of the currently active branch in the repository.
**Return Type:** String containing the name of the current branch.
**Exceptions Raised:** Raises `subprocess.CalledProcessError` if the git command fails, or `FileNotFoundError` if 'git' is not found.

### `list_local_branches() -> list[str]`
**Purpose:** Get a list of all local branches in the repository.
**Return Type:** List of strings containing names of all local branches.
**Exceptions Raised:** Raises `subprocess.CalledProcessError` if the git command fails, or `FileNotFoundError` if 'git' is not found.

### `get_base_branches(branches: list[str]) -> dict[str, str]`
**Purpose:** Identify and return a dictionary mapping of standard base branches (main/master, develop).
**Parameters:**
- `branches`: List of strings representing all branch names in the repository.
**Return Type:** Dictionary with keys "production" and/or "development", corresponding to the identified base branches.

### `validate_branch_name(name: str) -> bool`
**Purpose:** Check if a branch name adheres to Gitflow standards.
**Parameters:**
- `name`: String representing the branch name to validate.
**Return Type:** Boolean indicating whether the branch name is compliant with Gitflow standards.

### `check_gitflow_compliance() -> dict`
**Purpose:** Assess current repository compliance with Gitflow and return a detailed report.
**Return Type:** Dictionary containing details about the current branch, base branches, warnings, non-compliant branches, and overall compliance status.
**Exceptions Raised:** Raises `FileNotFoundError` if the directory is not a git repository.

### `start_branch(branch_type: str, name: str) -> str`
**Purpose:** Start a new branch of a given type from the correct base branch following Gitflow rules.
**Parameters:**
- `branch_type`: String representing the type of branch to create (e.g., "feature", "hotfix").
- `name`: String representing the desired name for the new branch.
**Return Type:** String containing the full name of the newly created branch.
**Exceptions Raised:** Raises `FileNotFoundError` if not in a git repository, `ValueError` if the branch type is invalid.

### `finish_current_branch(dry_run: bool = False, force: bool = False) -> None`
**Purpose:** Finish the current Gitflow branch with version and release synchronization following Gitflow rules.
**Parameters:**
- `dry_run`: Optional boolean indicating whether to perform a dry run (default is `False`).
- `force`: Optional boolean indicating whether to force version sync even if there are uncommitted changes (default is `False`).
**Return Type:** None
**Exceptions Raised:** Raises `FileNotFoundError` if not in a git repository, `ValueError` if the current branch is a base branch.

## Practical Usage Examples

### Checking Repository Compliance
```python
from gitflow_sync import check_gitflow_compliance

compliance_report = check_gitflow_compliance()
print(compliance_report)
```

### Starting a Feature Branch
```python
from gitflow_sync import start_branch

new_feature_branch = start_branch("feature", "new-feature-branch")
print(f"New feature branch created: {new_feature_branch}")
```

### Finishing a Release Branch
```python
from gitflow_sync import finish_current_branch

finish_current_branch(force=True)
print("Release branch finished successfully.")
```

These examples demonstrate how to use the functions provided by the `gitflow_sync` module to ensure Gitflow compliance and manage branches in your project effectively.
