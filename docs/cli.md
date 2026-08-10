# PR Sync CLI Documentation

## Module Description

`cli.py` is a command-line interface (CLI) tool designed to automate the process of creating and updating pull requests (PRs) on GitHub based on changes in a Git repository. It integrates with both local Git operations and GitHub's REST API to fetch repository data, analyze changes, generate PR content, and apply appropriate labels.

## Class and Function Reference

### Main Function: `main()`

**Purpose:** The primary function that orchestrates the entire PR sync process.

**Parameters:**
- None

**Return Type:**
- Integer: Exit code (0 for success, non-zero for failure).

**Exceptions Raised:**
- Any exception encountered during execution will be caught and printed to `stderr`.

**Example Usage:**
```python
# Running the CLI script from the command line
python cli.py --base develop
```

### Helper Functions

#### `check_auth()`
- **Purpose:** Verifies if GitHub CLI is authenticated.
- **Parameters:** None
- **Return Type:** Boolean: True if authenticated, False otherwise.

#### `get_current_branch()`
- **Purpose:** Fetches the current Git branch.
- **Parameters:** None
- **Return Type:** String: Name of the current branch.

#### `get_diff(base, head)`
- **Purpose:** Retrieves the difference between two branches (base and head).
- **Parameters:**
  - `base` (String): Base branch name.
  - `head` (String): Head branch name.
- **Return Type:** String: The diff output.

#### `get_commits(base, head)`
- **Purpose:** Fetches the commits between two branches.
- **Parameters:**
  - `base` (String): Base branch name.
  - `head` (String): Head branch name.
- **Return Type:** List of dictionaries: Each dictionary represents a commit.

#### `get_changed_files(base, head)`
- **Purpose:** Lists files that have changed between two branches.
- **Parameters:**
  - `base` (String): Base branch name.
  - `head` (String): Head branch name.
- **Return Type:** List of strings: Each string is a file path.

#### `check_no_empty_diff_action(diff)`
- **Purpose:** Checks if there are any non-empty diff actions in the provided diff.
- **Parameters:**
  - `diff` (String): Diff output.
  - `skip_check` (Boolean, optional): If True, skips the check.
- **Return Type:** Boolean: True if no changes, False otherwise.

#### `render_pr_body(diff, commits, base, head, changed_files, custom_model)`
- **Purpose:** Generates the PR body content based on the provided diff and commit information.
- **Parameters:**
  - `diff` (String): Diff output.
  - `commits` (List of dictionaries): Commit data.
  - `base` (String): Base branch name.
  - `head` (String): Head branch name.
  - `changed_files` (List of strings): Changed file paths.
  - `custom_model` (String, optional): Custom model for PR body generation.
- **Return Type:** String: PR body content.

#### `infer_type_label(changed_files)`
- **Purpose:** Infers the type label based on changed files.
- **Parameters:**
  - `changed_files` (List of strings): Changed file paths.
- **Return Type:** String: Inferred type label.

#### `infer_area_labels(changed_files)`
- **Purpose:** Infers area labels based on changed files.
- **Parameters:**
  - `changed_files` (List of strings): Changed file paths.
- **Return Type:** List of strings: Inferred area labels.

## Practical Usage Examples

### Basic PR Sync
```bash
python cli.py --base develop
```
This command will synchronize a pull request from the current branch to the `develop` branch.

### Custom Model for PR Body
```bash
python cli.py --base develop --model custom-model-name
```
This command will use a custom model named "custom-model-name" for generating the PR body content.

### Example of Error Handling
If any step fails, an error message will be printed to `stderr` and the script will return a non-zero exit code.
