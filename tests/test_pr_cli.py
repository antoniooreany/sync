from unittest.mock import patch

from pr_sync.cli import main


@patch("pr_sync.cli.sys.argv", ["pr-sync"])
@patch("pr_sync.cli.get_current_branch", return_value="feature/test")
@patch("pr_sync.cli.get_diff", return_value="")
def test_cli_empty_diff(mock_diff, mock_branch):
    assert main() == 0


@patch("pr_sync.cli.sys.argv", ["pr-sync"])
@patch("pr_sync.cli.check_auth", return_value=True)
@patch("pr_sync.cli.get_current_branch", return_value="feature/test")
@patch("pr_sync.cli.get_diff", return_value="some diff")
@patch("pr_sync.cli.get_commits", return_value=["commit 1"])
@patch("pr_sync.cli.get_changed_files", return_value=["file1.txt"])
@patch("pr_sync.cli.find_open_pr", return_value=None)
@patch("pr_sync.cli.create_pr", return_value={"url": "https://example.com/pr/1"})
@patch("pr_sync.cli.add_labels", return_value=None)
@patch("pr_sync.code_to_docs_generator.run_code_to_docs", return_value=None)
def test_cli_create_pr(mock_docs, mock_labels, mock_create, mock_find, mock_changed_files, mock_commits, mock_diff, mock_branch, mock_auth):
    assert main() == 0
    mock_create.assert_called_once()


@patch("pr_sync.cli.sys.argv", ["pr-sync"])
@patch("pr_sync.cli.check_auth", return_value=True)
@patch("pr_sync.cli.get_current_branch", return_value="feature/test")
@patch("pr_sync.cli.get_diff", return_value="some diff")
@patch("pr_sync.cli.get_commits", return_value=["commit 1"])
@patch("pr_sync.cli.get_changed_files", return_value=["file1.txt"])
@patch(
    "pr_sync.cli.find_open_pr",
    return_value={"number": "123", "url": "https://example.com/pr/123", "title": "t", "body": "b"},
)
@patch("pr_sync.cli.update_pr", return_value={"number": "123"})
@patch("pr_sync.cli.add_labels", return_value=None)
@patch("pr_sync.code_to_docs_generator.run_code_to_docs", return_value=None)
def test_cli_update_pr(mock_docs, mock_labels, mock_update, mock_find, mock_changed_files, mock_commits, mock_diff, mock_branch, mock_auth):
    assert main() == 0
    mock_update.assert_called_once()


@patch("pr_sync.cli.sys.argv", ["pr-sync"])
@patch("pr_sync.cli.check_auth", return_value=False)
@patch("pr_sync.cli.get_current_branch", return_value="feature/test")
@patch("pr_sync.cli.get_diff", return_value="some diff")
def test_cli_no_auth(mock_diff, mock_branch, mock_auth):
    assert main() == 2
