import pytest
from pr_sync.pr_body import render_pr_body
from pr_sync.invariants import check_sections_present

def test_render_pr_body():
    body = render_pr_body("diff", ["commit 1"])
    assert check_sections_present(body) is True
    assert "commit 1" in body
