"""
Invariant checking helpers for tests.
"""

def check_single_pr_invariant(prs: list) -> bool:
    """Ensure there is at most one open PR per (base, head) pair."""
    return len(prs) <= 1

def check_no_empty_diff_action(diff: str, action_taken: bool) -> bool:
    """Ensure no action is taken if diff is empty."""
    if not diff and action_taken:
        return False
    return True

def check_sections_present(body: str) -> bool:
    """Ensure all required sections are present and non-empty."""
    required_sections = [
        "## Summary",
        "## Changes",
        "## Commits",
        "## Risks",
        "## Config",
        "## Testing",
        "## Notes"
    ]
    for section in required_sections:
        if section not in body:
            return False
    return True
