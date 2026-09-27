# Documentation Generator (doc)

## Purpose and Design

The **Documentation Generator (doc)** is a Python script designed to automatically generate and stage documentation for source files within the `src/` directory of a project. This script utilizes the `pr_sync.code_to_docs_generator` module to achieve this task.

## Class and Function Reference

### `run_git(args: list[str]) -> str`
- **Parameters**: 
  - `args: list[str]` - A list of Git arguments to be executed.
- **Returns**: 
  - `str` - The standard output of the Git command.
- **Exceptions Raised**: 
  - `subprocess.CalledProcessError` - If the Git command fails.

### `get_staged_files() -> list[str]`
- **Returns**: 
  - `list[str]` - A list of file names in the staging area.
- **Exceptions Raised**: 
  - `None` - No exceptions are raised.

### `get_all_src_files() -> list[str]`
- **Returns**: 
  - `list[str]` - A list of all supported source files in the `src/` directory.
- **Exceptions Raised**: 
  - `None` - No exceptions are raised.

### `main()`
- **Purpose**: 
  - Main entry point of the script.
- **Parameters**: 
  - `sys.platform == "win32"`: Check if the platform is Windows.
  - `parser.add_argument()`: Adds command-line arguments for generating documentation.
  - `parser.parse_args()`: Parses the command-line arguments.
  - `files_to_process`: List of files to process based on the provided arguments.
  - `from pr_sync.code_to_docs_generator import run_code_to_docs`: Imports the `run_code_to_docs` function from the `pr_sync.code_to_docs_generator` module.
  - `print(f"📚 Generating documentation for {len(files_to_process)} file(s)...")`: Prints a message indicating the start of the documentation generation process.
  - `run_code_to_docs(files_to_process)`: Calls the `run_code_to_docs` function with the list of files to process.
  - `if generated`: Prints a success message if documentation was generated.
  - `except Exception as e`: Prints an error message if the documentation generation fails.

## Practical Usage Examples

1. **Generate all supported source files in the `src/` directory:**
   ```bash
   python doc.py
   ```

2. **Generate docs for specific files in the `src/` directory:**
   ```bash
   python doc.py my_file.py another_file.py
   ```

3. **Generate docs for staged files (default if no arguments are provided):**
   ```bash
   git add .
   python doc.py
   ```

4. **Generate docs for specific staged files:**
   ```bash
   git add .
   python doc.py specific_file1.py specific_file2.py
   ```

This script provides a streamlined way to manage and generate documentation for source files within a project, leveraging the power of Git for version control and the `pr_sync.code_to_docs_generator` module for the actual documentation generation process.
