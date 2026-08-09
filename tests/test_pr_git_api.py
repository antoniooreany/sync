import pytest
from unittest.mock import patch, MagicMock
import subprocess
from pr_sync.git_api import get_current_branch, get_diff

@patch("pr_sync.git_api.subprocess.run")
def test_get_current_branch(mock_run):
    mock_run.return_value = MagicMock(stdout="feature-branch\n", returncode=0)
    branch = get_current_branch()
    assert branch == "feature-branch"
    mock_run.assert_called_once_with(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True, encoding="utf-8", check=True)

@patch("pr_sync.git_api.subprocess.run")
def test_get_diff_empty(mock_run):
    mock_run.return_value = MagicMock(stdout="", returncode=0)
    diff = get_diff("main", "feature")
    assert diff == ""
    mock_run.assert_called_once_with(["git", "diff", "main..feature"], capture_output=True, text=True, encoding="utf-8", check=True)

@patch("pr_sync.git_api.subprocess.run")
def test_get_diff_with_content(mock_run):
    mock_run.return_value = MagicMock(stdout="diff content", returncode=0)
    diff = get_diff("main", "feature")
    assert diff == "diff content"

@patch("pr_sync.git_api.subprocess.run")
def test_get_diff_git_error(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, ["git", "diff"], stderr="Not a git repository")
    with pytest.raises(RuntimeError, match="Git diff error: Not a git repository"):
        get_diff("main", "feature")

@patch("pr_sync.git_api.subprocess.run")
def test_get_current_branch_git_not_found(mock_run):
    mock_run.side_effect = FileNotFoundError()
    with pytest.raises(RuntimeError, match="Git executable not found in PATH"):
        get_current_branch()
