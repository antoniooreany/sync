# Constants Module

## Module Description

This module defines constants used throughout the Gitflow Sync application. These constants help in managing exit codes and branch naming conventions, ensuring consistency and clarity across the codebase.

## Class and Function Reference

### EXIT_CODE_SUCCESS

- **Description**: Indicates that the application has executed successfully without any errors.
- **Return Type**: `int`
- **Value**: 0
- **Exception Raised**: None

Example Usage:
```python
if process_gitflow_sync():
    sys.exit(EXIT_CODE_SUCCESS)
```

### EXIT_CODE_EXPECTED_ERROR

- **Description**: Indicates that the application encountered an error that was expected and handled gracefully.
- **Return Type**: `int`
- **Value**: 1
- **Exception Raised**: None

Example Usage:
```python
try:
    if not check_branches():
        raise ValueError("Invalid branch detected")
except ValueError as e:
    print(e)
    sys.exit(EXIT_CODE_EXPECTED_ERROR)
```

### EXIT_CODE_ENV_ERROR

- **Description**: Indicates that the application encountered an error related to its environment, such as missing dependencies or misconfiguration.
- **Return Type**: `int`
- **Value**: 2
- **Exception Raised**: None

Example Usage:
```python
if not check_environment():
    sys.exit(EXIT_CODE_ENV_ERROR)
```

### EXIT_CODE_OTHER_ERROR

- **Description**: Indicates that the application encountered an unexpected error during execution.
- **Return Type**: `int`
- **Value**: 3
- **Exception Raised**: None

Example Usage:
```python
try:
    perform_git_operations()
except Exception as e:
    print(f"An unexpected error occurred: {e}")
    sys.exit(EXIT_CODE_OTHER_ERROR)
```

### VALID_PREFIXES

- **Description**: A list of valid branch prefix patterns that should be used when creating new branches.
- **Return Type**: `list`
- **Value**: ["feature/", "fix/", "bugfix/", "release/", "hotfix/", "support/"]
- **Exception Raised**: None

Example Usage:
```python
branch_name = "fix/update-login"
if any(branch_name.startswith(prefix) for prefix in VALID_PREFIXES):
    print("Valid branch name")
else:
    print("Invalid branch name")
```

### REQUIRED_BASE_BRANCHES

- **Description**: A list of required base branches that must be present in the repository.
- **Return Type**: `list`
- **Value**: ["main", "master", "develop"]
- **Exception Raised**: None

Example Usage:
```python
base_branch = "feature/new-feature"
if base_branch not in REQUIRED_BASE_BRANCHES:
    print("Base branch is required")
else:
    print("Valid base branch")
```

## Practical Usage Examples

### Example 1: Handling Different Exit Codes

```python
import sys
from constants import EXIT_CODE_SUCCESS, EXIT_CODE_EXPECTED_ERROR

def process_gitflow_sync():
    # Simulate the process of synchronizing Gitflow branches
    if not check_branches():
        return False
    # Additional processing logic here
    return True

if __name__ == "__main__":
    try:
        if process_gitflow_sync():
            sys.exit(EXIT_CODE_SUCCESS)
        else:
            raise ValueError("Branch validation failed")
    except ValueError as e:
        print(e)
        sys.exit(EXIT_CODE_EXPECTED_ERROR)
```

### Example 2: Checking Branch Names

```python
from constants import VALID_PREFIXES

def check_branch_name(branch_name):
    return any(branch_name.startswith(prefix) for prefix in VALID_PREFIXES)

branch_name = "feature/new-feature"
if check_branch_name(branch_name):
    print("Valid branch name")
else:
    print("Invalid branch name")
```

### Example 3: Verifying Base Branches

```python
from constants import REQUIRED_BASE_BRANCHES

def check_base_branches(base_branch):
    return base_branch in REQUIRED_BASE_BRANCHES

base_branch = "feature/new-feature"
if check_base_branches(base_branch):
    print("Valid base branch")
else:
    print("Base branch is required")
```

These examples demonstrate how to use the constants and functions defined in the `constants.py` module to manage exit codes, validate branch names, and ensure compliance with Gitflow best practices.
