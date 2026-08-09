import datetime
from pathlib import Path
from toolkit.docs_generator import infer_type_label, infer_area_labels
from toolkit.llm_engine import generate_smart_pr_summary

def render_pr_body(diff: str, commits: list, base: str = "develop", head: str = "HEAD", changed_files: list = None, custom_model: str = None) -> str:
    """Render the PR body using a local template or falling back to the default."""
    if changed_files is None:
        changed_files = []
        
    commits_str = "\n".join(f"{c}" for c in commits) if commits else "- None"
    changes_str = "\n".join(f"- {f}" for f in changed_files) if changed_files else "- None"
    timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")
    
    # Infer labels from the changed files
    type_label = infer_type_label(changed_files)
    area_labels = infer_area_labels(changed_files)
    inferred_labels = f"{type_label}, " + ", ".join(area_labels)

    # Try to generate smart summary via LLM
    smart_summary = generate_smart_pr_summary(diff, commits, custom_model=custom_model)

    
    if smart_summary:
        body_content = f"""{smart_summary}

## Raw Changes
{changes_str}

## Inferred Labels
- {inferred_labels}

## Notes
_Last updated by pr-sync (Smart Mode) at {timestamp}._"""
        return body_content
    
    # Context for rendering (fallback)
    context = {
        "{head}": head,
        "{base}": base,
        "{changes_str}": changes_str,
        "{commits_str}": commits_str,
        "{timestamp}": timestamp
    }
    
    local_template = Path(".specify/templates/pr-template.md")
    
    if local_template.exists():
        body = local_template.read_text(encoding="utf-8")
        for key, val in context.items():
            body = body.replace(key, val)
        return body
        
    # Default fallback template
    return f"""## Summary

Introduce changes from branch {head} into {base}.

## Changes

{changes_str}

## Commits

{commits_str}

## Inferred Labels

- {inferred_labels}

## Risks

- Low: see commit history for scope of change.

## Config

- No new required environment variables beyond existing ones.

## Testing

- ruff check, pytest, manual smoke test.

## Notes

-

_Last updated by pr-sync at {timestamp}._"""


