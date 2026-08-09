import pytest
from pathlib import Path
from release_sync.core import compile_release_notes, prepend_to_changelog

def test_compile_release_notes():
    mock_prs = [
        {
            "number": 12,
            "title": "feat(core): add math logic",
            "labels": [{"name": "type:feat"}],
            "author": {"login": "antoniooreany"}
        },
        {
            "number": 5,
            "title": "fix(core): crash on null values",
            "labels": [{"name": "bug"}],
            "author": {"login": "tester"}
        },
        {
            "number": 20,
            "title": "docs: rewrite README",
            "labels": [{"name": "docs"}],
            "author": {"login": "antoniooreany"}
        },
        {
            "number": 15,
            "title": "chore: add lint rules",
            "labels": [],
            "author": {"login": "antoniooreany"}
        }
    ]

    notes = compile_release_notes(mock_prs)
    
    # Check sections presence
    assert "### Features" in notes
    assert "### Bug Fixes" in notes
    assert "### Documentation" in notes
    assert "### Internal" in notes

    # Check formatting
    assert "- [#12] feat(core): add math logic (by @antoniooreany)" in notes
    assert "- [#5] fix(core): crash on null values (by @tester)" in notes

def test_prepend_to_changelog_exists(tmp_path):
    changelog_path = tmp_path / "CHANGELOG.md"
    initial_content = "# Changelog\n\n## v0.1.0\n- Initial release\n"
    changelog_path.write_text(initial_content, encoding="utf-8")

    prepend_to_changelog(changelog_path, "0.2.0", "### Features\n- New feature")

    content = changelog_path.read_text(encoding="utf-8")
    assert "# Changelog" in content
    assert "## v0.2.0" in content
    assert "### Features" in content
    assert "## v0.1.0" in content
