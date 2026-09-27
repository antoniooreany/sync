# syNC — Repository Automation Toolkit

CLI tools for Dependabot/commitlint setup, Conventional Commits, AI-assisted PRs and docs (local Ollama), gitflow, version bumps, and GitHub releases. Optional local Flask dashboard via `sync ui`.

## Prerequisites

- Python ≥ 3.9
- [`git`](https://git-scm.com/)
- [`gh`](https://cli.github.com/) (GitHub CLI), authenticated (`gh auth login`)
- [Ollama](https://ollama.com/) for `pr` / `doc` / `cm` AI features (default model: `qwen2.5-coder:7b`)

## Install

```bash
pip install -e ".[dev]"   # package + pytest/ruff
# or runtime only:
pip install -e .
```

## Shortcuts

```bash
sync init   # Dependabot + Commitlint hooks/CI in one step
sync ui     # Local web dashboard (http://127.0.0.1:5000)
sync        # Fetch/pull + install project deps (npm/pip)
dp          # Dependabot config (dp init)
glnt        # Commit lint setup (glnt init)
cm          # Conventional Commit helper (LLM or manual)
doc         # AI Markdown docs (staged files; doc --all for src/)
pr          # Create/update PR title, body, labels from diffs
rl          # Version bump, CHANGELOG, tag, GitHub Release
gf          # Gitflow check / start / finish
fs          # Feature porter (copy toolkit configs into a repo)
vs          # Version detect / bump / set / sync
```

Architecture overview: [docs/architecture.md](docs/architecture.md). Auto-generated module pages under `docs/` are drafts — prefer this README and the architecture doc.

---

## 1. Initial setup (one-time)

In the target git repository:

```bash
sync init
# or separately:
dp init    # .github/dependabot.yml
glnt init  # .gitlint, commit-msg hook, commit-lint workflow
```

---

## 2. Daily development flow

### Commit

```bash
git add .
git commit -m "feat(ui): add new interactive dashboard"
# or: cm
```

Invalid messages (e.g. `fixed bug`) are rejected by the commit-msg hook with Conventional Commits guidance.

### Pull request

```bash
pr
pr -m 1.5b   # optional Ollama model override
```

Analyzes diffs/commits, generates title and Markdown body (summary + risks), applies labels (`type:*`, `area:*`).

---

## 3. Releasing

```bash
rl 0.3.0 --dry-run   # preview
rl 0.3.0             # bump, CHANGELOG, commit, tag, GitHub Release
# or: rl patch | rl minor | rl major
```

Steps: sync version across configs → notes from merged PRs → `CHANGELOG.md` → commit → push → tag → GitHub Release.

---

## 4. Other tools

| Command | Role |
|---------|------|
| `gf check` | Gitflow branch naming compliance |
| `gf start feature <name>` | Create and switch to a gitflow branch |
| `gf finish` | Merge/finish current gitflow branch |
| `vs detect` / `vs bump` / `vs set` | Version helpers |
| `doc` / `doc --all` | LLM docs for staged or all `src/` files |
| `fs` | Interactive porter for toolkit features into another repo |
| `sync ui` | Dashboard for the same CLIs (allowlisted modules only) |

## Development

```bash
pytest
ruff check src tests
```

CI runs pytest (Python 3.9 / 3.12) and ruff on push and pull requests.
