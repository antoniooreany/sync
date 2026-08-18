# Python Script: Git Root Finder

## File/Module Description

This Python script provides functions to find and change the working directory to the root of a Git repository. The script is designed to be used in environments where Git repositories are present, allowing for streamlined operations like running Git commands.

## Class and Function Reference

### `find_git_root(path=None)`

**Parameters:**
- `path` (str, optional): The path to start the search from. Defaults to the current working directory (`os.getcwd()`).

**Returns:**
- `Path` or `None`: The root directory of the Git repository if found, otherwise `None`.

**Description:**
- This function recursively searches for the `.git` directory in the specified path and its ancestors to determine the root of the Git repository.
- It returns the `Path` object representing the root directory, or `None` if no Git repository is found.

**Example Usage:**
```python
from git_root_finder import find_git_root

# Example usage: find the root directory of the current working directory
root_path = find_git_root()
if root_path:
    print(f"Git repository root: {root_path}")
else:
    print("No Git repository found.")
```

### `chdir_to_git_root()`

**Parameters:**
- None

**Returns:**
- `bool`: `True` if the working directory was successfully changed to the Git repository root, `False` otherwise.

**Description:**
- This function uses the `find_git_root` function to locate the root directory of the Git repository.
- It then changes the current working directory to the root directory using `os.chdir()`.
- It returns `True` if the change was successful, otherwise `False`.

**Example Usage:**
```python
from git_root_finder import chdir_to_git_root

# Example usage: change the working directory to the Git repository root
if chdir_to_git_root():
    print("Working directory changed to the Git repository root.")
else:
    print("Failed to change the working directory.")
```

## Practical Usage Examples

1. **Finding the Git Root:**
   ```python
   from git_root_finder import find_git_root

   root_path = find_git_root()
   if root_path:
       print(f"Git repository root: {root_path}")
   else:
       print("No Git repository found.")
   ```

2. **Changing the Working Directory to the Git Root:**
   ```python
   from git_root_finder import chdir_to_git_root

   if chdir_to_git_root():
       print("Working directory changed to the Git repository root.")
   else:
       print("Failed to change the working directory.")
   ```

This Python script provides a simple yet effective way to locate and change the working directory to the root of a Git repository, making it easier to perform Git operations from any directory.
