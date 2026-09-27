# Maturity & Hygiene Specification

**Status:** Implemented (retroactive SDD formalization)  
**Version:** 0.4.2  
**Branch:** `feature/maturity-hygiene`  
**Related:** `.specify/memory/constitution.md` (spec-first, Gitflow, spec-backed tests)

## Purpose

Raise repository maturity without new product features: make the toolkit installable, CI-gated, honest about shipped capabilities, and free of author-specific hardcoding.

## Scope

| In scope | Out of scope |
|----------|--------------|
| Dependency hygiene | PyPI publish |
| CI (pytest + ruff) | Multi-provider LLM (Gemini) |
| UI allowlist / remove SboxGame hooks | New `docgen` / `testgen` packages |
| Dead-code removal; implement docs stub | Docker |
| README, architecture, LICENSE | Monorepo shared-lib refactor |

## Requirements

### R1 — Runtime dependencies match imports

- **Given** the package defined in `pyproject.toml`
- **Then** runtime `dependencies` MUST include only packages imported under `src/`
- **And** MUST NOT list unused `requests` or `google-genai`
- **And** MUST provide optional `dev` extras: `pytest`, `ruff`

**Tests:** `tests/test_maturity_hygiene.py::test_r1_runtime_deps_match_policy`

### R2 — CI quality gate

- **Given** a push or pull request
- **Then** GitHub Actions MUST run pytest on Python 3.9 and 3.12
- **And** MUST run `ruff check src tests`
- **And** workflow lives at `.github/workflows/ci.yml`

**Tests:** `tests/test_maturity_hygiene.py::test_r2_ci_workflow_exists`

### R3 — Duplicate release-notes tests removed

- **Given** release-notes unit tests
- **Then** exactly one canonical module MUST own them: `tests/test_release_sync.py`
- **And** `tests/test_core.py` MUST NOT exist

**Tests:** `tests/test_maturity_hygiene.py::test_r3_no_duplicate_core_tests`

### R4 — UI has no project-specific release zip hooks

- **Given** the Flask dashboard
- **Then** routes `/compress` and `/download` MUST NOT exist
- **And** UI templates MUST NOT reference SboxGame paths or Compress-Archive release zip UX

**Tests:** `tests/test_maturity_hygiene.py::test_r4_no_sbox_routes_or_template_hooks`

### R5 — `/run` allowlist only

- **Given** `POST /run` with a script name
- **When** the script is not in the explicit allowlist
- **Then** the API MUST respond HTTP 400
- **And** allowlist MUST be exactly: `pr`, `rl`, `dp`, `glnt`, `cm`, `gf`, `fs`, `vs`, `doc`, `sync`
- **And** `args` MUST be a list of strings or the API returns HTTP 400
- **And** Flask MUST run with `debug=False` by default (`sync ui` and `__main__`)

**Tests:** `tests/test_ui_allowlist.py`, `tests/test_maturity_hygiene.py::test_r5_debug_false`

### R6 — LLM engine is Ollama-only

- **Given** `pr_sync.llm_engine`
- **Then** there MUST be no Gemini model-discovery helper
- **And** generation MUST target local Ollama

**Tests:** `tests/test_maturity_hygiene.py::test_r6_no_gemini_helper`

### R7 — `generate_module_docs` is implemented

- **Given** an existing source file path
- **When** `generate_module_docs` is called
- **Then** it MUST call the LLM content API (not a no-op `pass`)
- **And** return stripped markdown or `""` on failure / missing file

**Tests:** `tests/test_maturity_hygiene.py::test_r7_generate_module_docs_uses_llm`

### R8 — Feature porter catalog is honest

- **Given** `feature_sync.constants.FEATURES`
- **Then** entries MUST map to existing CLIs only
- **And** MUST NOT advertise `docgen_sync` / `testgen_sync` (`dg` / `tg`)
- **And** MAY include `doc_sync` for the real `doc` command

**Tests:** `tests/test_feature_sync.py::test_get_porter_features`

### R9 — Documentation surface

- **Given** a new contributor
- **Then** root `README.md` MUST document install, prerequisites, and all console scripts including `gf`, `fs`, `vs`, `doc`, `sync`
- **And** `docs/architecture.md` MUST describe package/script map
- **And** `LICENSE` (MIT) MUST exist
- **And** auto-generated `docs/*` MUST be labeled as drafts in `docs/README.md`

**Tests:** `tests/test_maturity_hygiene.py::test_r9_docs_and_license`

### R10 — Smoke coverage for previously weak CLIs

- **Given** `doc` and `gf` CLIs
- **Then** smoke tests MUST cover exit codes for empty staged docs, missing git repo, and compliant/non-compliant `gf check`

**Tests:** `tests/test_doc_sync.py`, `tests/test_gitflow_cli.py`

## Non-functional

- Chat with humans: Russian; code/docs/commits: English (constitution).
- Changes land on `feature/*` under Gitflow; CI must be green before merge.

## Acceptance

All tests listed above pass locally and in CI. Spec and tests are merged with the implementation on `feature/maturity-hygiene`.
