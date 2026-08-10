import sys
import pytest
from unittest.mock import patch, MagicMock
from gitlint_sync.commit_generator import generate_suggestion, main

def test_generate_suggestion():
    # Test verb cleanup and correct classification
    assert generate_suggestion("added new database connection") == "feat: new database connection"
    assert generate_suggestion("Fixed connection leak") == "fix: connection leak"
    assert generate_suggestion("Update documentation rules") == "docs: documentation rules"
    assert generate_suggestion("refactor old parser method") == "refactor: old parser method"
    assert generate_suggestion("test case for user login") == "test: case for user login"
    assert generate_suggestion("chore: bump version number") == "chore: bump version number"
    assert generate_suggestion("just some custom message") == "feat: just some custom message"

@patch("gitlint_sync.commit_generator.run_git")
@patch("gitlint_sync.commit_generator.has_staged_changes")
@patch("gitlint_sync.commit_generator.get_staged_diff")
@patch("gitlint_sync.commit_generator.generate_llm_content")
@patch("builtins.input")
@patch("subprocess.run")
def test_main_with_argument(mock_sub_run, mock_input, mock_llm, mock_get_diff, mock_has_changes, mock_run_git):
    # Verify behavior when raw message is provided as positional argument
    mock_run_git.return_value = "true"
    mock_input.return_value = "y"
    
    with patch("sys.argv", ["cm", "Added cool features"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        
    mock_sub_run.assert_called_with(["git", "commit", "-m", "feat: cool features"], check=True)

@patch("gitlint_sync.commit_generator.run_git")
@patch("gitlint_sync.commit_generator.has_staged_changes")
@patch("gitlint_sync.commit_generator.get_staged_diff")
@patch("gitlint_sync.commit_generator.generate_llm_content")
@patch("builtins.input")
@patch("subprocess.run")
def test_main_auto_ai_generation(mock_sub_run, mock_input, mock_llm, mock_get_diff, mock_has_changes, mock_run_git):
    # Verify AI generation when no message argument is provided
    mock_run_git.return_value = "true"
    mock_has_changes.return_value = True
    mock_get_diff.return_value = "mock staged diff"
    mock_llm.return_value = "feat(core): implementation details"
    mock_input.return_value = "y"
    
    with patch("sys.argv", ["cm"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        
    mock_llm.assert_called_once()
    mock_sub_run.assert_called_with(["git", "commit", "-m", "feat(core): implementation details"], check=True)

@patch("gitlint_sync.commit_generator.run_git")
@patch("gitlint_sync.commit_generator.has_staged_changes")
def test_main_no_staged_changes(mock_has_changes, mock_run_git):
    mock_run_git.return_value = "true"
    mock_has_changes.return_value = False
    
    with patch("sys.argv", ["cm"]):
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 1
