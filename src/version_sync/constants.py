# Constants to avoid magic numbers
EXIT_CODE_SUCCESS = 0
EXIT_CODE_EXPECTED_ERROR = 1
EXIT_CODE_ENV_ERROR = 2

# Version identification regexes
VERSION_TOML_PATTERN = r'^version\s*=\s*["\']([^"\']+)["\']'
VERSION_CODE_PATTERN = r'^(__version__|VERSION|version)\s*=\s*["\']([^"\']+)["\']'
