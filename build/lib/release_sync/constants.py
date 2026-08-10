# Constants to avoid magic numbers
EXIT_CODE_SUCCESS = 0
EXIT_CODE_EXPECTED_ERROR = 1
EXIT_CODE_ENV_ERROR = 2
EXIT_CODE_OTHER_ERROR = 3

DEFAULT_PR_LIMIT = 100
DEFAULT_TO_REF = "HEAD"
DEFAULT_CHANGELOG_FILENAME = "CHANGELOG.md"

# Categorization labels mapping
LABELS_BREAKING = {"breaking-change", "breaking"}
LABELS_FEATURES = {"type:feat", "feature", "enhancement"}
LABELS_BUGFIXES = {"type:fix", "bug", "fix"}
LABELS_DOCS = {"type:docs", "docs"}
