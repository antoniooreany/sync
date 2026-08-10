# Release Sync CLI (rl)

## Purpose and Design

The `release_sync` command-line interface is designed to automate the process of releasing software projects by integrating GitHub and Git functionalities. This tool helps in automating versioning, tracking changes, and creating detailed release notes.

### Class and Function Reference

#### Main Script (`main.py`)
- **Description**: The main entry point for the `release_sync` CLI. It parses command-line arguments, validates environment conditions, and orchestrates the release process.
- **Parameters**:
  - `version`: Optional, the semantic version of the target release (e.g., `0.3.0`) or a bump level (`major`, `minor`, `patch`).
  - `from_ref`: Exclusive starting git reference for the range of commits to include in the release.
  - `to_ref`: Inclusive ending git reference for the range of commits to include in the release.
  - `dry-run`: Optional, whether to perform a dry run without writing files or creating GitHub releases.
  - `force`: Optional, whether to allow version downgrade.
  - `changelog`: Path to the CHANGELOG file. Default: `CHANGELOG.md`.
- **Return Type**: None
- **Exceptions Raised**:
  - `ValueError` if the version specified does not match a known semantic version or bump level.
  - `RuntimeError` for environmental issues (not inside a valid Git repository or GitHub CLI authentication).

#### Core Functions (`core.py`)
- **get_latest_tag()**: Retrieves the latest tag in the Git repository.
- **verify_tag_does_not_exist(target_version)**: Checks if a specified semantic version tag already exists in the Git repository.
- **get_commits_between(from_ref, to_ref)**: Fetches commits between two git references (exclusive starting and inclusive ending).
- **fetch_merged_prs()**: Retrieves all merged pull requests from GitHub within the specified commit range.
- **compile_release_notes(matched_prs)**: Compiles detailed release notes based on the matched PRs and their associated commits.
- **prepend_to_changelog(changelog_path, target_version, notes)**: Prepends the generated release notes to the CHANGELOG file.
- **create_git_tag(target_version)**: Creates a new git tag with the specified semantic version.
- **push_git_tag(target_version)**: Pushes the newly created git tag to the remote repository.
- **create_github_release(target_version, notes)**: Creates a GitHub release using the specified semantic version and release notes.
- **commit_and_push_release(target_version, changelog_path)**: Commits and pushes all changes related to the release (CHANGELOG and version configs).
- **sync_version_across_repo(project_root, target_version, force=args.force)**: Syncs the version across different project directories with the specified semantic version and optional force flag.

## Practical Usage Examples

1. **Automatic Version Bumping**:
   ```sh
   rl --version patch
   ```
   This command will check the current version, auto-detect a bump level (patch by default), and sync the version across all project directories if necessary.

2. **Custom Version Specification**:
   ```sh
   rl --version 0.3.5 --from v0.3.0 --to HEAD
   ```
   This command will use the specified semantic version (`0.3.5`) and a custom range of commits (`v0.3.0` to `HEAD`) to generate release notes, sync the version across all project directories, and create a GitHub release.

3. **Dry Run**:
   ```sh
   rl --version 1.2.3 --dry-run
   ```
   This command will simulate the entire release process without writing files or creating GitHub releases, allowing you to preview changes before they are applied.

4. **Force Version Downgrade**:
   ```sh
   rl --version 0.5.6 --force
   ```
   This command will allow version downgrade if specified, ensuring that `0.5.6` is used as the target release even if it does not match a known semantic version or bump level.

By following these steps and using the provided examples, you can automate the release process for your software projects with ease using the `release_sync` CLI.
