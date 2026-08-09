# Automation Toolkit - Constitution & Overview

## 1. Specify Overview
**Who am I?**
Solo developer building a long-term toolkit of small automation tools for my own repositories (and later small teams).
Comfortable with Python, GitHub, CI, and Spec-Driven Development (SDD).
Already maintain automation logic inside another repository:
oracle-capacity-hunter-claude: https://github.com/antoniooreany/oracle-capacity-hunter-claude

**What problem am I solving?**
Today, key development workflows (PR metadata, release notes, labels, CI triage, documentation) are handled by:
- ad-hoc scripts embedded in a single repo (e.g. scripts/pr.ps1, code_to_docs.py),
- manual, repetitive steps in GitHub UI and CI,
- logic that grew organically and accumulated subtle bugs.
As I add more repositories, I either need to copy these scripts everywhere or risk each repo diverging in quality and behavior.

**What is my proposed solution?**
Build a small family of CLI tools that:
- share one SDD-based process (constitution + specs + tests + governance),
- reuse existing engines where possible (e.g. docs-assistant / code_to_docs.py),
- each focus on a single workflow (PRs, releases, docs, CI, repo hygiene),
- are reusable across repositories without copy-pasting scripts.
The first tool in this family is `pr-sync`, which standardizes how PRs are created and updated.

**Constraints and preferences**
- Platform: GitHub only for v1, via the `gh` CLI (no GitLab/Bitbucket yet).
- Language: Python for implementation, to reuse existing code_to_docs.py logic and fit into current tooling (pytest, ruff, etc.).
- Methodology: Spec-Driven Development (SDD):
  - behavior changes start from updating specs, not from "vibe coding" directly in the implementation;
  - every tool has a written contract (specification) and tests enforcing it;
  - tools must be safe-by-default and predictable.

## 2. Constitution
**Purpose**
This constitution defines the core principles, invariants, and governance rules for the Automation Toolkit.
The toolkit is a family of small, focused automation tools that standardize and automate repetitive development workflows (PRs, releases, docs, CI, hygiene) across repositories, using Spec-Driven Development.

**Principles**
- **Spec-first**: Behavior changes start from updating specifications and this constitution, not from direct code edits.
- **No duplication**: New tools MUST NOT reimplement functionality that already exists in other tools or engines (e.g. the docs-assistant / code_to_docs.py). They should orchestrate or extend existing capabilities, or cover new workflows.
- **Single responsibility**: Each tool focuses on one domain (PRs, releases, labels, CI, docs, repo hygiene) and has a clear scope document.
- **GitHub-first**: v1 targets GitHub only, via the gh CLI. Multi-provider support (GitLab, Bitbucket, etc.) is explicitly out of scope for v1.
- **Docs-as-code**: All specs, this constitution, and related design docs live in the repository and are versioned with Git.

**Core invariants (for all tools)**
These apply across the toolkit; individual tools may add their own invariants.
- **Written specification per tool**: Every tool has a written specification document (e.g. docs/pr-sync-specification.md) that describes inputs, outputs, and behavior.
- **Spec-backed tests**: Tests MUST exist that directly enforce the specification: spec → tests → code, not the other way around.
- **Semantic versioning**: The toolkit and each tool follow semantic versioning: MAJOR.MINOR.PATCH. Breaking changes to any published specification or invariant require a MAJOR version bump.
- **Spec-first changes**: Any behavioral change MUST start with a PR modifying the relevant spec and, if needed, this constitution. Code changes that alter behavior MUST NOT be merged without corresponding spec and test updates.
- **Safe-by-default behavior**: Tools MUST avoid destructive actions without explicit intent. Examples: no force-push, no deleting branches by default, no creating duplicate PRs/releases when ambiguity exists.
- **Reuse over reimplementation**: Existing engines (e.g. docs-assistant / code_to_docs.py) SHOULD be reused where applicable. New tools SHOULD act as orchestrators, composers, or adapters around existing functionality.

**Governance and change process**
- **Spec-first workflow**: Propose changes by editing:
  - `docs/specify-automation-toolkit.md` (if system-wide),
  - `.specify/constitution.md` (if principles/invariants/governance change),
  - the relevant tool specification.
  Only then update tests and code.
- **Mapping to tests**: Each invariant in this constitution and each requirement in a tool spec MUST have at least one test enforcing it.
- **Breaking changes**: Removing or relaxing an invariant is considered a breaking change. Such changes MUST: be explicitly flagged in the PR, bump MAJOR version, include migration notes.
- **Scope expansion**: Supporting new providers or major new workflows MUST be described first in the specs and/or constitution, then implemented with corresponding tests.

## 3. Tool Catalog and Scope
- **pr-sync**
  - **Status**: designing / implementing (v1 focus).
  - **Purpose**: Create or update a single GitHub PR for the current branch against a base branch, with a standardized PR body and integration with docs-assistant.
  - **Scope**: One open PR per (base, head) pair. PR body contains standardized sections. Uses git and gh. Delegates richer documentation to docs-assistant.
  - **Out of scope (v1)**: Release notes (handled by release-sync). Automatic semver decision. Direct generation of standalone documentation.
- **release-sync**: (planned) Aggregate merged PRs and commits into release notes and changelog sections, create GitHub Releases and git tags.
- **doc-sync**: (planned) Orchestrate the existing docs-assistant to update documentation from code, specs, PRs, and releases.
- **version-sync**: (future) Decide semantic version bump based on changes and labels, and update versions in code and tags.
- **label-sync**: (future) Automatically apply labels and help triage PRs/issues.
- **ci-sync**: (future) Provide CI health summaries, highlight flaky tests.
- **repo-sync**: (future) Maintain repository hygiene across multiple repos.
