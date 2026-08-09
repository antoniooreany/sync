import pytest
from unittest.mock import patch, MagicMock
from pr_sync.gh_api import check_auth, find_open_pr, create_pr, update_pr
import json

@patch("pr_sync.gh_api.subprocess.run")
def test_check_auth_success(mock_run):
    mock_run.return_value = MagicMock(returncode=0)
    assert check_auth() is True

@patch("pr_sync.gh_api.subprocess.run")
def test_check_auth_fail(mock_run):
    mock_run.return_value = MagicMock(returncode=1)
    assert check_auth() is False

@patch("pr_sync.gh_api.check_auth")
@patch("pr_sync.gh_api.subprocess.run")
def test_find_open_pr_single(mock_run, mock_auth):
    mock_auth.return_value = True
    mock_run.return_value = MagicMock(stdout=json.dumps([{"number": 1, "url": "http", "title": "t", "body": "b"}]), returncode=0)
    pr = find_open_pr("main", "feature")
    assert pr is not None
    assert pr["number"] == 1

@patch("pr_sync.gh_api.check_auth")
@patch("pr_sync.gh_api.subprocess.run")
def test_find_open_pr_multiple(mock_run, mock_auth):
    mock_auth.return_value = True
    mock_run.return_value = MagicMock(stdout=json.dumps([{"number": 1}, {"number": 2}]), returncode=0)
    with pytest.raises(ValueError, match="Found multiple open PRs"):
        find_open_pr("main", "feature")

@patch("pr_sync.gh_api.check_auth")
@patch("pr_sync.gh_api.subprocess.run")
def test_find_open_pr_none(mock_run, mock_auth):
    mock_auth.return_value = True
    mock_run.return_value = MagicMock(stdout="[]", returncode=0)
    pr = find_open_pr("main", "feature")
    assert pr is None

@patch("pr_sync.gh_api.check_auth")
@patch("pr_sync.gh_api.subprocess.run")
def test_create_pr(mock_run, mock_auth):
    mock_auth.return_value = True
    mock_run.return_value = MagicMock(stdout="https://github.com/pr/1\n", returncode=0)
    result = create_pr("title", "body", "main", "feature")
    assert result["url"] == "https://github.com/pr/1"
    mock_run.assert_called_once_with(["gh", "pr", "create", "--base", "main", "--head", "feature", "--title", "title", "--body", "body"], capture_output=True, text=True, encoding="utf-8", check=True)

@patch("pr_sync.gh_api.check_auth")
@patch("pr_sync.gh_api.subprocess.run")
def test_update_pr(mock_run, mock_auth):
    mock_auth.return_value = True
    mock_run.return_value = MagicMock(returncode=0)
    result = update_pr(1, "new title", "new body")
    assert result["number"] == 1
    mock_run.assert_called_once_with(["gh", "pr", "edit", "1", "--title", "new title", "--body", "new body"], capture_output=True, text=True, encoding="utf-8", check=True)

@patch("pr_sync.gh_api.check_auth")
def test_find_open_pr_unauthenticated(mock_auth):
    mock_auth.return_value = False
    with pytest.raises(RuntimeError, match="GitHub CLI is not authenticated"):
        find_open_pr("main", "feature")
