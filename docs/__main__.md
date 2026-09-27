# PrSync: A Python Workspace Synchronization Tool

PrSync is a comprehensive Python tool designed to synchronize local git repositories and manage Python project dependencies. It includes a web UI for real-time updates and integrates with Dependabot and Gitlint for continuous integration and code quality management.

## File/Module Description

### `run_sync_workspace()`
- **Purpose**: Synchronizes the local git repository from origin and updates dependencies based on project type.
- **Parameters**: None.
- **Return Type**: `None`.
- **Exceptions Raised**: `subprocess.CalledProcessError`

### `run_ui()`
- **Purpose**: Starts the PrSync web UI on `http://127.0.0.1:5000`.
- **Parameters**: None.
- **Return Type**: `None`.
- **Exceptions Raised**: `subprocess.CalledProcessError`

### `run_init()`
- **Purpose**: Initializes the repository by running Dependabot and Gitlint for continuous integration and code quality management.
- **Parameters**: None.
- **Return Type**: `None`.
- **Exceptions Raised**: `subprocess.CalledProcessError`

### `main()`
- **Purpose**: The entry point for the workspace sync tool.
- **Parameters**: None.
- **Return Type**: `None`.
- **Exceptions Raised**: `subprocess.CalledProcessError`

## Practical Usage Examples

#### Synchronize the Local Git Repository
To synchronize the local git repository, run the following command:
```sh
python pr_sync/main.py
```

#### Start the PrSync Web UI
To start the web UI, run the following command:
```sh
python pr_sync/main.py ui
```

#### Initialize the Repository
To initialize the repository, run the following command:
```sh
python pr_sync/main.py init
```

### Additional Notes

- **Dependency Management**: PrSync supports Python projects using `package.json` for Node.js projects, `pyproject.toml` for Python projects, and `requirements.txt` for Python projects.
- **Continuous Integration**: The tool integrates with Dependabot and Gitlint to ensure that your project dependencies are up-to-date.
- **Real-Time Updates**: The web UI provides real-time updates on changes and dependency updates.

### Contributing

Contributions are welcome! Please open an issue or a pull request to contribute to the tool.
