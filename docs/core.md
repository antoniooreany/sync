# Release Sync Module Documentation

## Introduction
The `release_sync` module provides a set of functions to automate the process of creating and managing releases in a Git repository. It utilizes Python's `subprocess` module to interact with git commands and GitHub CLI for handling PRs, tags, and release management.

## Overview
- **`run_git_command`**: Executes git commands and returns their output.
- **`run_gh_command`**: Executes GitHub CLI commands and handles exceptions.
- **`get_latest_tag`**: Retrieves the latest git tag in the repository.
- **`verify_tag_does_not_exist`**: Checks if a version tag already exists locally.
- **`get_commits_between`**: Fetches commits between two specified refs.
- **`fetch_merged_prs`**: Fetches merged Pull Requests using GitHub CLI.
- **`resolve_author`**: Extracts author login name from PR structure.
- **`compile_release_notes`**: Compiles structured, alphabetical release notes from grouped PRs.
- **`prepend_to_changelog`**: Prepend the release notes block into CHANGELOG.md.
- **`get_current_branch`**: Gets the name of the current git branch.
- **`commit_and_push_release`**: Stages modified files, commits the release, and pushes to origin if configured.
- **`create_git_tag`**: Creates a local git tag for the release at HEAD.
- **`push_git_tag`**: Pushes the tag to the remote origin if configured.
- **`create_github_release`**: Create a GitHub release using gh CLI if remote is configured.

## Usage Examples
1. **Running Git Commands**:
   ```python
   latest_tag = run_git_command(["describe", "--tags", "--abbrev=0"])
   ```

2. **Fetching Merged PRs**:
   ```python
   merged_prs = fetch_merged_prs()
   for pr in merged_prs:
       print(pr)
   ```

3. **Prepending Release Notes to CHANGELOG.md**:
   ```python
   prepend_to_changelog(Path("CHANGELOG.md"), "1.0.0", "This is the release notes for version 1.0.0.")
   ```

4. **Syncing Version Across Repo**:
   ```python
   updated_files = sync_version_across_repo(Path(".git"), "2.0.0")
   print("Updated files:", updated_files)
   ```

## Notes
- The module is designed to be used in a Git repository with GitHub CLI installed and configured.
- Ensure that the GitHub CLI is authenticated properly before using `create_github_release`.
- For production environments, consider adding error handling and logging for more robustness.
