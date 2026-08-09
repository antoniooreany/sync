# Code-to-Docs Constraints

## What the agent MUST NOT do

1. **MUST NOT auto-merge PRs.** The agent only updates metadata (title, body, labels). Merging is always a human decision.

2. **MUST NOT modify source code.** The agent reads diffs but never writes to source files.

3. **MUST NOT create new branches.** The agent operates on the current branch only.

4. **MUST NOT delete branches.** Branch lifecycle is managed by humans or other automation.

5. **MUST NOT push commits.** The agent does not alter git history in any way.

6. **MUST NOT leak API keys.** Environment variables (`OLLAMA_MODEL`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`) must never appear in logs, PR body, or error messages beyond generic provider names.

7. **MUST NOT override manually edited PR descriptions** without explicit `--force` flag. If a PR body was manually edited by a human, the agent should warn and skip unless forced.

## What the agent MUST do

1. **MUST gracefully degrade** if no LLM provider is available. Fall back to the static template — never crash or leave the PR without a body.

2. **MUST retry on transient errors.** Use exponential backoff (10s → 20s → 40s) for HTTP 429 (rate limit) responses, up to 3 attempts.

3. **MUST sanitize diff content.** Truncate diffs to 4000 characters before sending to LLM to avoid token limit errors.

4. **MUST apply labels idempotently.** Running the agent multiple times on the same PR should not create duplicate labels.

5. **MUST use deterministic label inference.** Label inference from file paths (`docs_generator.py`) is rule-based, not LLM-based, ensuring consistent results.

## Scope boundaries

- The agent operates on **one PR at a time**.
- The agent requires `gh` CLI to be installed and authenticated.
- The agent assumes the repository follows **GitFlow** (base branch defaults to `develop`).
- The agent does not interact with CI/CD pipelines, deployment, or release processes.
