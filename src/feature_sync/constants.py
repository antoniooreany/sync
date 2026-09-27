EXIT_CODE_SUCCESS = 0
EXIT_CODE_EXPECTED_ERROR = 1
EXIT_CODE_ENV_ERROR = 2

FEATURES = {
    "gitflow_sync": {
        "name": "Gitflow Compliance (gf)",
        "desc": "Automates branch creation (start) and compliant merging with automatic version syncing (finish).",
        "next_steps": [
            "Run 'gf check' to check current compliance of the repository.",
            "Start a new feature with 'gf start feature <name>'."
        ]
    },
    "gitlint_sync": {
        "name": "Conventional Commit Linter (glnt/cm)",
        "desc": "Installs commit hooks and CI workflows to validate commit formats against Conventional Commits.",
        "next_steps": [
            "Run 'glnt init' to register commit-msg hook and local configs.",
            "Use 'cm' to auto-generate and commit compliant messages."
        ]
    },
    "release_sync": {
        "name": "Release Automator (rl)",
        "desc": "Automatically bumps version, updates CHANGELOG, creates git tag, and uploads a GitHub Release.",
        "next_steps": [
            "Run 'rl patch' (or minor/major) to release a new version."
        ]
    },
    "doc_sync": {
        "name": "Documentation Generator (doc)",
        "desc": "Generates Markdown documentation for source files via local Ollama (defaults to staged files).",
        "next_steps": [
            "Ensure Ollama is running locally with 'qwen2.5-coder:7b'.",
            "Run 'doc' for staged files, or 'doc --all' for everything under src/."
        ]
    },
}
