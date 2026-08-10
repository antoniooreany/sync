# Configuration Utilities Module

## Purpose and Design

The `config.py` module provides utilities for loading and expanding configuration files, particularly JSON files that may contain environment variables. The primary goal is to make it easier to manage configuration settings that can vary across different environments (development, staging, production) without requiring manual changes in the code.

### Key Features:

1. **Environment Variable Expansion**: Automatically expands `${ENV_VAR}` strings within configuration values using environment variables.
2. **ConfigError Handling**: Raises a `ConfigError` if an required environment variable is not set or if there are missing fields in the configuration file.

## Class and Function Reference

### ConfigError Exception

**Purpose**: Raised when a configuration is missing required fields or environment variables.

**Inheritance**: Inherits from Python's built-in `Exception`.

### expand_env(value: Any) -> Any

**Purpose**: Recursively expands `${ENV_VAR}` strings in configuration data using environment variables.

**Parameters**:
- `value (Any)`: The configuration value to be expanded. This can be a string, dictionary, list, or any other type.

**Return Type**: 
- `Any`: The expanded configuration value.

**Exceptions Raised**:
- `ConfigError`: If an required environment variable is not set.

**Example Usage**:
```python
import config

config_data = {"database": "${DB_URL}"}
expanded_config = config.expand_env(config_data)
print(expanded_config)  # Output depends on the 'DB_URL' environment variable
```

### load_json_config(path: str | Path) -> dict[str, Any]

**Purpose**: Loads a JSON configuration file and expands any environment variables within it.

**Parameters**:
- `path (str | Path)`: The path to the JSON configuration file.

**Return Type**: 
- `dict[str, Any]`: A dictionary containing the expanded configuration data.

**Exceptions Raised**:
- `ConfigError`: If a required environment variable is not set or if there are missing fields in the configuration file.
- `FileNotFoundError`: If the specified configuration file does not exist.
- `json.JSONDecodeError`: If the JSON file is malformed.

**Example Usage**:
```python
import config

config_path = "path/to/config.json"
config_data = config.load_json_config(config_path)
print(config_data)  # Output depends on the contents of 'config.json' and environment variables
```

## Practical Usage Examples

### Example Configuration File (`config.json`)

```json
{
    "database": {
        "url": "${DB_URL}",
        "username": "${DB_USERNAME}",
        "password": "${DB_PASSWORD}"
    },
    "server": {
        "host": "localhost",
        "port": 8080
    }
}
```

### Usage in Code

```python
import config

# Load and expand configuration
config_path = "path/to/config.json"
expanded_config = config.load_json_config(config_path)

# Accessing the database URL from the expanded configuration
db_url = expanded_config["database"]["url"]
print(f"Database URL: {db_url}")
```

### Setting Environment Variables

Before running the above code, ensure that the following environment variables are set:

```bash
export DB_URL="postgresql://user:password@localhost:5432/mydb"
export DB_USERNAME="myuser"
export DB_PASSWORD="mypassword"
```

This will allow the configuration loader to successfully expand the environment variable strings and provide a complete, functional configuration for the automation toolkit.
