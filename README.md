# Repository Automation Toolkit: Usage Guide

This guide describes how to use the automation tools (`dp`, `gl`, `pr`, and `rl`) together to manage repository health, enforce commit formatting, generate pull requests, and automate version releases.

---

## 1. Initial Repository Setup (One-time)
To configure Dependabot, Commitlint, local commit hooks, and CI workflows in a single step, run this in the root of the Git repository:

* **Configure Dependabot**:
  ```bash
  dp init
  ```
  * *What it does*: Generates a low-noise `.github/dependabot.yml` (weekly checks, max 3 PRs).

* **Configure Commit Linting**:
  ```bash
  gl init
  ```
  * *What it does*: Generates `.gitlint` rules, sets up the local `.git/hooks/commit-msg` python validator, and adds the `.github/workflows/commit-lint.yml` GitHub Actions pipeline.

---

## 2. Daily Development Flow
With the tools initialized, follow this loop:

### Step A: Code & Commit
Make changes and commit them. The commit-msg hook runs automatically:
```bash
git add .
git commit -m "feat(ui): add new interactive dashboard"
```
* If the commit message is invalid (e.g. `fixed bug`), the commit is rejected with a clear explanation of Conventional Commits requirements.

### Step B: Create / Sync Pull Request
Once you push your branch and open a PR, run:
```bash
pr
```
* **With custom model**: `pr -m 1.5b`
* **What it does**: Analyzes diffs/commits, generates PR Title, detailed Markdown Body (with LLM Summary & Risk Analysis), and applies tags (`type:*`, `area:*`).

---

## 3. Releasing a New Version
When features in `develop` are ready, orchestrate the entire release (version bumping + changelog compilation + tagging + GitHub release) in a single atomic action:

```bash
rl 0.3.0
```
* **Dry-run first**: `rl 0.3.0 --dry-run` (prints what files would change and prints compiled release notes without committing or tagging).
* **What it does**:
  1. Bumps/sets version to `0.3.0` across all repository configs (`pyproject.toml`, etc.) and code source files.
  2. Compiles release notes from merged PRs since the last release.
  3. Updates `CHANGELOG.md`.
  4. Commits `CHANGELOG.md` and version changes with `chore(release): release v0.3.0`.
  5. Pushes the release commit to GitHub.
  6. Tags the release `v0.3.0` and pushes the tag.
  7. Creates the official GitHub Release.
