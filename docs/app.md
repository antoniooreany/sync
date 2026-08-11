# PR Sync Python Module Documentation

## 1. Module Description and Design

The `pr_sync` module is designed to automate the process of syncing pull requests (PRs) in a software development project. The primary purpose of this module is to ensure that changes from one branch are seamlessly integrated into another, which helps maintain code quality and consistency across different development teams.

### Key Features:
- **Synchronous Execution**: All sync processes run synchronously within the current Python environment, providing immediate feedback.
- **CLI Integration**: The module integrates with a custom CLI (`pr_sync.cli`) for advanced configuration and customization.
- **Error Handling**: The module includes robust error handling to manage failures gracefully.
- **Documentation**: Comprehensive documentation is available in Markdown format, making it easy for users to understand how to use the module.

### Design Goals:
1. **Scalability**: The module should be able to handle a large number of PRs concurrently without performance degradation.
2. **Flexibility**: Users should have the ability to customize various aspects of the sync process through the CLI.
3. **Ease of Use**: The module should provide clear, step-by-step instructions for users to set up and use the sync functionality.

## 2. Class and Function Reference

### Classes
- **PrSyncApp**:
  - Methods:
    - `__init__`: Initializes the Flask application instance.
    - `index()`: Renders the main UI page.
    - `sync()`: Executes the PR sync process with parameters from the UI.

### Functions
- **main()**: Entry point of the Flask application.
- **compress():** Runs PowerShell to compress a build directory into a zip file suitable for release.

#### Parameters and Return Types:
- **PrSyncApp.sync():**
  - Parameters:
    - `base`: String, the base branch for the sync process (default: "develop").
    - `model`: Optional string, optional model name for customizing the sync process.
  - Returns:
    - Dictionary with keys `"returncode"`, `"stdout"`, and `"stderr"` representing the execution result.

- **PrSyncApp.index():**
  - Parameters:
    - None
  - Returns:
    - Rendered HTML template containing the main UI page.

#### Exceptions Raised:
- The module does not raise any specific exceptions to the user. Instead, it uses Flask's error handling mechanisms to provide clear feedback in the UI.

### Practical Usage Examples

1. **Setting Up the Sync Application:**
   ```bash
   python app.py
   ```
   This command will start the Flask application on `http://127.0.0.1:5000`.

2. **Executing a PR Sync:**
   Access `http://127.0.0.1:5000/sync` in your web browser or using Postman.
   Send a POST request to `/sync` with the following JSON payload:
   ```json
   {
       "base": "feature-branch",
       "model": "CustomModel"
   }
   ```
   This will trigger the sync process for the `feature-branch` branch, using the `CustomModel` model if provided.

3. **Compressing a Build Directory:**
   Access `http://127.0.0.1:5000/compress` in your web browser or using Postman.
   This will run PowerShell to compress the contents of the `Builds/Windows` directory into `Release/SboxGame_v1.1.1.zip`.

4. **Error Handling in the UI:**
   If a file is not found in the build directory, the UI will display an error message indicating no files are present.

## Conclusion

The `pr_sync` module provides a robust and user-friendly tool for automating PR sync processes in software development projects. With its synchronous execution, CLI integration, and comprehensive documentation, it ensures efficient and reliable code management across teams.
