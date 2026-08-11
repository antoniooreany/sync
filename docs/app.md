# PR Sync and Release Automation Module

## Overview

The `pr_sync` module is designed to automate the process of synchronizing pull requests (PRs) from a remote repository to a local workspace, handling the synchronization with specified branches and models. The module also includes a feature to compress the SboxGame Windows build using PowerShell.

## Classes and Functions Reference

### `PrSync`
**Purpose**: Manages the main functionality of the PR sync process.

#### Methods:
- **`__init__(self)`**: Initializes the `PrSync` class.
  - Parameters: N/A
  - Return Type: None

- **`execute_sync(self, base, model=None)`**: Executes the PR sync process.
  - Parameters:
    - `base` (str): The base branch to synchronize with. Defaults to "develop".
    - `model` (str, optional): The model to use for synchronization. Defaults to `None`.
  - Return Type: A dictionary containing the return code and standard output/error of the sync process.

### `CompressBuild`
**Purpose**: Manages the creation of a compressed zip file for the SboxGame Windows build.

#### Methods:
- **`__init__(self)`**: Initializes the `CompressBuild` class.
  - Parameters: N/A
  - Return Type: None

- **`compress_zip(self)`**: Compresses the SboxGame Windows build using PowerShell and returns the path to the compressed zip file.
  - Parameters: N/A
  - Return Type: A string representing the path to the compressed zip file.

## Practical Usage Examples

#### Example of Using the `PrSync` Class

To use the `PrSync` class, you need to first initialize it with the base branch and model. Then, you can call the `execute_sync` method to execute the sync process.

```python
from pr_sync import PrSync

# Initialize the PrSync class
pr_sync = PrSync()

# Define the base branch and optional model
base_branch = "feature-branch"
model_name = "latest-release"

try:
    # Execute the PR sync process
    response = pr_sync.execute_sync(base_branch, model_name)
    print("Sync Process Response:", response)
except Exception as e:
    print(f"An error occurred: {e}")
```

#### Example of Using the `CompressBuild` Class

To use the `CompressBuild` class, you need to first initialize it. Then, you can call the `compress_zip` method to compress the SboxGame Windows build.

```python
from pr_sync import CompressBuild

# Initialize the CompressBuild class
compress_build = CompressBuild()

try:
    # Create a compressed zip file for the SboxGame Windows build
    zip_path = compress_build.compress_zip()
    print("Compressed Zip File Path:", zip_path)
except Exception as e:
    print(f"An error occurred: {e}")
```

This markdown documentation provides a clear and concise overview of the `pr_sync` module, its classes, methods, and usage examples.
