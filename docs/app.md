# SboxGame Release Automation Flask Application

## Introduction
This Flask application is designed to facilitate the release automation process for a SboxGame project. It provides a user-friendly interface to manage local Git branches and execute various scripts for releasing different types of builds. The application is designed to be easily integrated into a development workflow and can be run locally for testing and development purposes.

## File/Module Description

#### `app.py`
- **Purpose**: Main application entry point. It sets up the Flask web server and routes for different functionalities.
- **Design**:
  - **Flask**: The main web server to handle HTTP requests and responses.
  - **find_git_root**: A function to locate the root directory of the Git repository.
  - **index**: Handles the main dashboard page, displaying dynamic git branches list.
  - **run_command**: Executes the selected monorepo script with specified parameters.
  - **compress**: Compresses the build artifacts using PowerShell.
  - **download_release**: Downloads the generated release zip file.

#### `sync.py`
- **Purpose**: Contains utilities for syncing and deploying different types of builds.
- **Design**:
  - **find_git_root**: A function to locate the root directory of the Git repository.
  - **main**: The main function to execute the selected monorepo script.

## Class and Function Reference

#### `app.py`
- **`index()`**
  - **Purpose**: Renders the main dashboard page with dynamic git branches list.
  - **Parameters**:
    - `branches`: List of available branches.
    - `repo_name`: Name of the repository.
  - **Return Type**: HTML string.
  - **Raises**: `Exception` if an error occurs during the execution of `git branch`.

- **`run_command()`**
  - **Purpose**: Executes the selected monorepo script with specified parameters.
  - **Parameters**:
    - `data`: JSON payload containing the script and arguments.
  - **Return Type**: JSON response containing the return code, stdout, and stderr.
  - **Raises**: `Exception` if an error occurs during the execution of the script.

- **`compress()`**
  - **Purpose**: Compresses the build artifacts using PowerShell.
  - **Parameters**:
    - `None`
  - **Return Type**: JSON response containing the return code, stdout, and stderr.
  - **Raises**: `Exception` if an error occurs during the compression process.

- **`download_release()`**
  - **Purpose**: Downloads the generated release zip file.
  - **Parameters**: `None`
  - **Return Type**: Redirects to the release zip file for download.
  - **Raises**: `Exception` if the release zip file is not found.

#### `sync.py`
- **`main()`**
  - **Purpose**: Executes the selected monorepo script.
  - **Parameters**:
    - `script`: The name of the script to execute.
    - `args`: The arguments to pass to the script.
  - **Return Type**: None.
  - **Raises**: `Exception` if the script execution fails.

## Practical Usage Examples

### Running a Script

1. **Navigate to the Project Directory**:
   ```sh
   cd /path/to/your/project
   ```

2. **Run the Main Application**:
   ```sh
   python app.py
   ```

3. **Open the Web Browser**:
   Open a web browser and navigate to `http://127.0.0.1:5000/`.

4. **Select a Script and Arguments**:
   - Go to the "Run" route.
   - Select a script from the dropdown menu.
   - Enter any required arguments in the input fields.

5. **View the Output**:
   - The application will execute the selected script and return the output in JSON format.

### Compressing a Build

1. **Navigate to the Build Directory**:
   ```sh
   cd /path/to/your/project/Builds/Windows
   ```

2. **Run the Compress Route**:
   ```sh
   curl -X POST http://127.0.0.1:5000/compress
   ```

3. **Download the Result**:
   - The application will execute the compression process and return the zip file URL.
   - Click the link to download the generated release zip file.

### Downloading a Release

1. **Navigate to the Release Directory**:
   ```sh
   cd /path/to/your/project/Release
   ```

2. **Run the Download Route**:
   ```sh
   curl -X GET http://127.0.0.1:5000/download
   ```

3. **Download the Result**:
   - The application will return the zip file URL.
   - Click the link to download the generated release zip file.

By following these usage examples, you can easily manage the release automation process for your SboxGame project using this Flask application.
