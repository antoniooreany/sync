# GitHub API Interaction Layer Documentation

## Module Description

The `gh_api.py` module provides a layer of interaction with GitHub using the GitHub CLI (Command Line Interface). It includes functions to check authentication status, find open pull requests, create new pull requests, update existing pull requests, and add labels to pull requests.

### Design
- The module uses Python's `subprocess` module to run GitHub CLI commands.
- It captures the output of these commands and handles exceptions for common errors such as unauthenticated access or missing CLI tool.
- Functions are designed to return structured data (e.g., dictionaries) where applicable, and raise exceptions if operations fail.

## Class and Function Reference

### `check_auth() -> bool`

**Purpose:**  
Checks if the GitHub CLI is authenticated.

**Parameters:**  
None

**Return Type:**  
`bool`: True if authenticated, False otherwise.

**Exceptions Raised:**
- `FileNotFoundError`: If the GitHub CLI (`gh`) is not found on the system.

### `find_open_pr(base: str, head: str) -> dict`

**Purpose:**  
Finds an open pull request for the given base and head branches. Returns details of the PR if found.

**Parameters:**  
- `base` (str): The name of the base branch.
- `head` (str): The name of the head branch.

**Return Type:**  
`dict`: A dictionary containing details of the open PR, or `None` if no such PR is found.

**Exceptions Raised:**
- `RuntimeError`: If the GitHub CLI is not authenticated or not found.
- `ValueError`: If multiple open PRs are found for the given base and head branches.

### `create_pr(title: str, body: str, base: str, head: str) -> dict`

**Purpose:**  
Creates a new pull request with the specified title, body, base branch, and head branch.

**Parameters:**  
- `title` (str): The title of the new PR.
- `body` (str): The description or body text of the new PR.
- `base` (str): The name of the base branch.
- `head` (str): The name of the head branch.

**Return Type:**  
`dict`: A dictionary containing the URL of the newly created PR.

**Exceptions Raised:**
- `RuntimeError`: If the GitHub CLI is not authenticated or not found.

### `update_pr(pr_number: str, title: str, body: str) -> dict`

**Purpose:**  
Updates an existing pull request with the specified PR number, new title, and body text.

**Parameters:**  
- `pr_number` (str): The number of the PR to update.
- `title` (str): The new title for the PR.
- `body` (str): The new description or body text for the PR.

**Return Type:**  
`dict`: A dictionary containing the number of the updated PR.

**Exceptions Raised:**
- `RuntimeError`: If the GitHub CLI is not authenticated or not found.

### `add_labels(pr_number: str, labels: list[str]) -> None`

**Purpose:**  
Applies labels to an existing pull request. Creates labels if they do not already exist in the repository.

**Parameters:**  
- `pr_number` (str): The number of the PR to which labels will be applied.
- `labels` (list[str]): A list of label names to apply to the PR.

**Return Type:**  
None

**Exceptions Raised:**
- `RuntimeError`: If the GitHub CLI is not authenticated or not found.

## Practical Usage Examples

### Example 1: Checking Authentication Status
```python
if gh_api.check_auth():
    print("GitHub CLI is authenticated.")
else:
    print("GitHub CLI is not authenticated.")
```

### Example 2: Finding an Open PR
```python
base_branch = "main"
head_branch = "feature-branch"

pr_info = gh_api.find_open_pr(base_branch, head_branch)
if pr_info:
    print(f"Open PR found: {pr_info['url']}")
else:
    print("No open PR found.")
```

### Example 3: Creating a New PR
```python
title = "Add new feature"
body = "This is the description of the new feature."
base_branch = "main"
head_branch = "feature-branch"

new_pr_url = gh_api.create_pr(title, body, base_branch, head_branch)
print(f"New PR created: {new_pr_url['url']}")
```

### Example 4: Updating an Existing PR
```python
pr_number = "123"
new_title = "Updated feature"
new_body = "Updated description of the feature."

gh_api.update_pr(pr_number, new_title, new_body)
print(f"PR {pr_number} updated successfully.")
```

### Example 5: Adding Labels to a PR
```python
pr_number = "123"
labels = ["bug", "urgent"]

gh_api.add_labels(pr_number, labels)
print(f"Labels added to PR {pr_number}.")
```
