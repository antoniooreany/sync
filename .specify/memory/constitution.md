<!-- Sync Impact Report:
- Version change: 1.0.0 -> 2.0.0
- Added sections: Purpose, Automation Toolkit Principles, Core Invariants, Current and Planned Tools
- Modified principles: Replaced initial generic principles with specific Automation Toolkit principles, moved global user rules into Global Engineering Standards.
- Follow-up TODOs: None
-->

# Automation Toolkit Constitution

## Purpose
This constitution defines the core principles, invariants, and governance rules for the Automation Toolkit.
The toolkit is a family of small, focused automation tools that standardize and automate repetitive development workflows (PRs, releases, docs, CI, hygiene) across repositories, using Spec-Driven Development.

## Principles

### I. Spec-first
Behavior changes start from updating specifications and this constitution, not from direct code edits.

### II. No duplication
New tools MUST NOT reimplement functionality that already exists in other tools or engines (e.g. the docs-assistant / `code_to_docs.py`). They should orchestrate or extend existing capabilities, or cover new workflows.

### III. Single responsibility
Each tool focuses on one domain (PRs, releases, labels, CI, docs, repo hygiene) and has a clear scope document.

### IV. GitHub-first
v1 targets GitHub only, via the `gh` CLI. Multi-provider support (GitLab, Bitbucket, etc.) is explicitly out of scope for v1.

### V. Docs-as-code
All specs, this constitution, and related design docs live in the repository and are versioned with Git.

## Core Invariants (For all tools)
These apply across the toolkit; individual tools may add their own invariants.

1. **Written specification per tool**
   Every tool has a written specification document (e.g. `docs/pr-sync-specification.md`) that describes inputs, outputs, and behavior.

2. **Spec-backed tests**
   Tests MUST exist that directly enforce the specification: spec → tests → code, not the other way around.

3. **Semantic versioning**
   - The toolkit and each tool follow semantic versioning: MAJOR.MINOR.PATCH.
   - Breaking changes to any published specification or invariant require a MAJOR version bump.

4. **Spec-first changes**
   - Any behavioral change MUST start with a PR modifying the relevant spec and, if needed, this constitution.
   - Code changes that alter behavior MUST NOT be merged without corresponding spec and test updates.

5. **Safe-by-default behavior**
   - Tools MUST avoid destructive actions without explicit intent.
   - Examples: no force-push, no deleting branches by default, no creating duplicate PRs/releases when ambiguity exists.

6. **Reuse over reimplementation**
   - Existing engines (e.g. docs-assistant / `code_to_docs.py`) SHOULD be reused where applicable.
   - New tools SHOULD act as orchestrators, composers, or adapters around existing functionality.

## Global Engineering Standards
*(Enforced across all tools and AI interactions)*

1. **Language & Communication**: Codebase (code, comments, docs) MUST be in English. Chat interactions with the user MUST be in Russian.
2. **Git Workflow & Deployment**: Strictly use Gitflow (`main`, `develop`, `feature/*`, `fix/*`, `release/*`). Production deployments are permitted ONLY from release branches and require staging verification. Default deployments target staging.
3. **Clean Code & Testing**: Avoid 'magic numbers'. Refactor, commit/push, update docs, and write/run passing tests before completing any feature.
4. **Command Execution**: Execute shell commands separately (no `&&` in PowerShell). Do not ask permission to make changes; assume agreement. Do not run long-running commands like `npm start`.
5. **Logging & Telemetry**: Logs MUST be maximally detailed (environment metadata, versioning, `saltUsed`). Constants MUST auto-sync across layers. AI must log remaining credits and handle usage limit errors by logging details, retrying, and alerting the user.
6. **Reporting**: Reports MUST use SI units, HTML tables, and SVG graphs.

## Current and Planned Tools

- **Existing logic (origin)**:
  - Repo: oracle-capacity-hunter-claude (https://github.com/antoniooreany/oracle-capacity-hunter-claude)
  - Contains:
    - `scripts/pr.ps1` — script for creating/updating PRs via `gh`.
    - `src/capacity_hunter/code_to_docs.py` — docs-assistant engine for generating PR descriptions and docs from diffs.
- **Toolkit tools**:
  - `pr-sync` (first tool): PR body and metadata automation.
  - **Planned tools**:
    - `release-sync`: release notes, changelog, and GitHub Releases.
    - `version-sync`: semantic version bumping and tagging.
    - `label-sync`: automatic labeling and triage of PRs/issues.
    - `ci-sync`: CI summaries and flaky test handling.
    - `doc-sync`: orchestration of docs-assistant to update docs from code, specs, and PRs.
    - `repo-sync`: repository hygiene and cross-repo config consistency.

## Governance and Change Process

1. **Spec-first workflow**
   - Propose changes by editing:
     - `docs/specify-automation-toolkit.md` (if system-wide),
     - `docs/constitution.md` or `.specify/memory/constitution.md` (if principles/invariants/governance change),
     - the relevant tool specification (e.g. `docs/pr-sync-specification.md`).
   - Only then update tests and code.

2. **Mapping to tests**
   - Each invariant in this constitution and each requirement in a tool spec MUST have at least one test enforcing it.

3. **Breaking changes**
   - Removing or relaxing an invariant is considered a breaking change.
   - Such changes MUST: be explicitly flagged in the PR, bump MAJOR version, and include migration notes.

4. **Scope expansion**
   - Supporting new providers (GitLab, Bitbucket, etc.) or major new workflows MUST be described first in the specs and/or constitution, then be implemented with corresponding tests.

**Version**: 2.0.0 | **Ratified**: 2026-08-05 | **Last Amended**: 2026-08-05
