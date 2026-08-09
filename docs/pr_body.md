# `pr_sync.render_pr_body` Module Documentation

The `render_pr_body` function is designed to generate a PR body in Markdown format based on a given set of inputs, such as diffs, commits, and base/head branch information. This function leverages templates for customization and uses LLMs (Language Model Applications) to create a more detailed summary of the changes.

## Purpose and Design

- **Local Template Customization**: The function allows users to specify their own Markdown template for the PR body.
- **LLM Integration**: It uses a default LLM (`generate_smart_pr_summary`) to generate a smart summary from the diff and commits, enhancing the content with relevant context.
- **Custom Model Configuration**: Users can provide a custom model name using `custom_model` to optimize LLM responses.

## Class and Function Reference

### Parameters

1. **diff**: A string containing the difference between the base and head branches in Markdown format (`str`).
2. **commits**: A list of strings where each item represents a commit message in Markdown format (`list` of `str`) or `None`.
3. **base**: The base branch for the PR, which defaults to "develop".
4. **head**: The head branch from which changes are being pulled into the base branch, which defaults to "HEAD".
5. **changed_files**: A list of file paths that have changed in the pull request. If not provided, it defaults to an empty list.
6. **custom_model**: An optional string specifying a custom LLM model name for generating the smart summary (`str`).

### Return Types

- A `str` representing the rendered PR body.

### Exceptions Raised

- `ValueError`: If `commits` is not provided and no `changed_files` are available.
- `FileNotFoundError`: If the local template file `.specify/templates/pr-template.md` does not exist.

## Practical Usage Examples

#### Example 1: Using Local Template
```python
from pr_sync.render_pr_body import render_pr_body

diff = """
---
name: Bug Fix
description: Fixes a bug identified in the old codebase.
```

commits = [
    "- fix(old_code.py): Fixed an issue with the old logic.",
    "- refactor(new_code.py): Refactored the code to improve performance."
]

template_content = """## Summary

Introduce changes from branch {head} into {base}.

## Changes

- {changes_str}

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

rendered_body = render_pr_body(diff, commits, template_content=template_content)
print(rendered_body)
```

#### Example 2: Using Default LLM
```python
from pr_sync.render_pr_body import render_pr_body

diff = """
---
name: Feature Addition
description: Adds a new feature to the existing codebase.
```

commits = [
    "- add(new_feature.py): Added a new feature to handle user requests."
]

rendered_body = render_pr_body(diff, commits)
print(rendered_body)
```

#### Example 3: Customizing LLM Model
```python
from pr_sync.render_pr_body import render_pr_body

diff = """
---
name: Documentation Update
description: Updated the documentation for better clarity.
```

commits = [
    "- update(docs.md): Updated the documentation to reflect new features."
]

rendered_body = render_pr_body(diff, commits, custom_model="custom-model")
print(rendered_body)
```

These examples demonstrate how to use the `render_pr_body` function with different inputs, including a local template and customization of the LLM model.
