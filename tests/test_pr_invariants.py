from pr_sync.invariants import (
    check_single_pr_invariant,
    check_no_empty_diff_action,
    check_sections_present,
)

def test_check_single_pr_invariant():
    assert check_single_pr_invariant([]) is True
    assert check_single_pr_invariant([{}]) is True
    assert check_single_pr_invariant([{}, {}]) is False

def test_check_no_empty_diff_action():
    assert check_no_empty_diff_action("", False) is True
    assert check_no_empty_diff_action("", True) is False
    assert check_no_empty_diff_action("diff", False) is True
    assert check_no_empty_diff_action("diff", True) is True

def test_check_sections_present():
    valid_body = "\n".join([
        "## Summary\ncontent",
        "## Changes\ncontent",
        "## Commits\ncontent",
        "## Risks\ncontent",
        "## Config\ncontent",
        "## Testing\ncontent",
        "## Notes\ncontent",
    ])
    assert check_sections_present(valid_body) is True
    assert check_sections_present("## Summary") is False
