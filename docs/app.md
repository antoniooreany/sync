# Sync Module Documentation

The `sync` module is designed to manage various tasks related to syncing and maintaining monorepo projects. It provides two main routes: `/run` and `/compress`.

## Module Description

This module includes functions for executing specific target scripts with parameters, as well as a feature to compress SboxGame Windows builds using PowerShell.

### Class and Function Reference

#### `sync.run_command`

**Description:** Executes the specified script with given arguments in the local monorepo directory.

**Parameters:**
- **script (str):** The name of the target script. Supported scripts include:
  - `pr`: `pr_sync.cli`
  - `rl`: `release_sync.cli`
  - `dp`: `dependabot_sync.cli`
  - `glnt`: `gitlint_sync.cli`
  - `cm`: `gitlint_sync.commit_generator`
  - `gf`: `gitflow_sync.cli`
  - `fs`: `feature_sync.cli`
  - `vs`: `version_sync.cli`

- **args (list):** A list of arguments to pass to the target script. The order and number of arguments are not specified, but the provided parameters should be valid for the respective script.

**Return Type:**
- **dict:** A dictionary containing the return code (`returncode`), standard output (`stdout`), and standard error (`stderr`) from the executed script.

**Exceptions Raised:**
- **ValueError:** If an invalid script name is provided.
- **subprocess.CalledProcessError:** If the command execution fails with a non-zero exit status.

#### `sync.compress`

**Description:** Runs PowerShell to compress the contents of the specified SboxGame Windows build directory into a ZIP file.

**Parameters:**
- **None**

**Return Type:**
- **dict:** A dictionary containing the return code (`returncode`), standard output (`stdout`), and standard error (`stderr`) from the PowerShell command execution.

**Exceptions Raised:**
- **FileNotFoundError:** If the specified build directory does not exist.
- **subprocess.CalledProcessError:** If the PowerShell command execution fails with a non-zero exit status.

## Practical Usage Examples

#### Running a Target Script

To run a specific target script, send a POST request to `/run` with the appropriate JSON payload. For example:

```json
{
    "script": "pr",
    "args": ["list", "of", "arguments"]
}
```

This will execute the `pr_sync.cli` script with the provided arguments and return the output in JSON format.

#### Compressing a Build Directory

To compress the SboxGame Windows build directory, send a POST request to `/compress`. For example:

```json
{
    // No parameters needed for this endpoint
}
```

This will run the PowerShell command to zip up the contents of the `Builds/Windows` directory into `Release/SboxGame_v1.1.1.zip`.

These examples demonstrate how to interact with the `sync` module using Python, ensuring that tasks related to project synchronization and management are efficiently managed.
