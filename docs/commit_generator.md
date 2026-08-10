# commit_generator.py

commit_generator.py is a Python script designed to help generate and format Conventional Commit messages for Git commits. It provides both manual message formatting and automatic suggestion generation based on staged changes, optionally using an LLM (Large Language Model) for enhanced suggestions.

## Module Description

The module consists of several functions and a main execution flow:

1. **run_git(args: list[str]) -> str**: Executes a git command with the provided arguments and returns its output.
2. **get_staged_diff() -> str**: Retrieves the diff of currently staged changes.
3. **has_staged_changes() -> bool**: Checks if there are any staged changes.
4. **generate_suggestion(msg: str) -> str**: Generates a Conventional Commit suggestion based on a given raw commit message.
5. **main()**: The main function that parses command-line arguments, verifies the git repository context, formats or suggests a commit message, and commits if confirmed.

## Class and Function Reference

### Functions

#### run_git(args: list[str]) -> str
- **Parameters**:
  - `args` (list[str]): A list of string arguments for the git command.
- **Return Type**: str
- **Exception**: subprocess.CalledProcessError if the git command fails.

#### get_staged_diff() -> str
- **Return Type**: str
- **Description**: Retrieves the diff of currently staged changes using `run_git`.

#### has_staged_changes() -> bool
- **Return Type**: bool
- **Description**: Checks if there are any staged changes by running a git command. Returns True if changes exist, False otherwise.

#### generate_suggestion(msg: str) -> str
- **Parameters**:
  - `msg` (str): The raw commit message to format.
- **Return Type**: str
- **Description**: Formats the provided message into a Conventional Commit suggestion based on predefined rules. If the message already follows the pattern, it returns as is.

### Main Execution Flow

The `main()` function orchestrates the following steps:
1. Sets up command-line argument parsing using `argparse`.
2. Verifies if the script is running inside a valid Git repository.
3. Depending on whether a commit message is provided as an argument or not, it either formats the provided message or generates one using LLM based on staged changes.
4. Prompts the user for confirmation before committing.
5. If confirmed, executes the git commit command.

## Practical Usage Examples

### Example 1: Manual Message Formatting
```sh
python commit_generator.py "added new feature to improve performance"
```
Output:
```
✨ Formatted commit message: "feat: added new feature to improve performance"
❓ Confirm and commit? [Y/n]:
```

### Example 2: Automatic Message Generation from Staged Changes
1. Stage some changes in your Git repository.
2. Run the script without providing a message:
```sh
python commit_generator.py
```
Output:
```
🤖 Analyzing staged changes with AI...
🤖 AI Suggested Message: "refactor: updated documentation"
❓ Confirm and commit? [Y/n]:
```

### Example 3: Committing the Suggested Message
1. After generating a suggested message, respond with 'Y' to commit:
```sh
python commit_generator.py
🤖 Analyzing staged changes with AI...
🤖 AI Suggested Message: "fix: resolved critical bug"
❓ Confirm and commit? [Y/n]: Y
🎉 Successfully committed!
```

### Example 4: Aborting the Commit
1. Respond with 'n' or any other non-confirmation input:
```sh
python commit_generator.py
🤖 Analyzing staged changes with AI...
🤖 AI Suggested Message: "chore: updated dependencies"
❓ Confirm and commit? [Y/n]: n
Aborted.
```

### Example 5: Error Handling
1. If no staged changes are detected:
```sh
git add .
python commit_generator.py
❌ Error: No staged changes. Use 'git add' to stage files first.
```
2. If an error occurs during AI message generation:
```sh
git add .
python commit_generator.py
🤖 Analyzing staged changes with AI...
💥 Failed to generate message using AI: ...
```
