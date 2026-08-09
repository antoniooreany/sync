# Code-to-Docs Contract

## Overview

The `code-to-docs` module automatically generates structured PR metadata
(title, body, labels) from repository diff and commit data.

## Input

| Field           | Type         | Source                          |
|-----------------|--------------|---------------------------------|
| `diff`          | `str`        | `git diff {base}...{head}`      |
| `commits`       | `list[str]`  | `git log --oneline {base}..{head}` |
| `changed_files` | `list[str]`  | `git diff --name-only {base}...{head}` |
| `branch_name`   | `str`        | `git rev-parse --abbrev-ref HEAD` |
| `base_branch`   | `str`        | CLI argument `--base` (default: `develop`) |

## Output

### Title
```
Auto PR: {branch_name}
```

### Body (Smart Mode — LLM available)
```markdown
## Smart Summary
<LLM-generated logical grouping of changes>

## Risk Analysis
<LLM-generated assessment of risks>

## Raw Changes
- file1.py
- file2.py

## Inferred Labels
- type:feat, area:core, area:tests

## Notes
_Last updated by pr-sync (Smart Mode) at {timestamp}._
```

### Body (Fallback Mode — no LLM)
```markdown
## Summary
Introduce changes from branch {head} into {base}.

## Changes
- file1.py
- file2.py

## Commits
- abc1234 feat: add feature X
- def5678 fix: resolve bug Y

## Inferred Labels
- type:feat, area:core

## Risks
- Low: see commit history for scope of change.

## Config
- No new required environment variables beyond existing ones.

## Testing
- ruff check, pytest, manual smoke test.

## Notes
-
_Last updated by pr-sync at {timestamp}._
```

### Labels
Applied as GitHub PR labels via `gh pr edit --add-label`:

| Label        | Condition                                      |
|--------------|-------------------------------------------------|
| `type:ci`    | Changed files in `.github/workflows/`           |
| `type:docs`  | Changed files in `docs/` or `*.md`              |
| `type:test`  | Changed files in `tests/`                       |
| `type:feat`  | Changed files in `src/`                         |
| `type:chore` | Default fallback                                |
| `area:ci`    | Changed files in `.github/workflows/`           |
| `area:docs`  | Changed files in `docs/` or `*.md`              |
| `area:tests` | Changed files in `tests/`                       |
| `area:core`  | Changed files in `src/`                         |
| `area:misc`  | Default fallback                                |

## LLM Provider Priority

| Priority | Provider  | Env Variable       | Model                      |
|----------|-----------|--------------------|-----------------------------|
| 1        | Ollama    | `OLLAMA_MODEL`     | User-specified (local)      |
| 2        | Anthropic | `ANTHROPIC_API_KEY` | `claude-3-haiku-20240307`   |
| 3        | Google    | `GEMINI_API_KEY`   | Auto-detected (prefers lite)|

If no provider is available, the system falls back to the static template.

## Trigger Mechanisms

1. **Local CLI**: Run `pr.exe` or `pr-sync.exe` from any git repository
2. **GitHub Actions**: Comment `[review-pr]` on any open PR (requires `docs-assistant.yml` workflow)
