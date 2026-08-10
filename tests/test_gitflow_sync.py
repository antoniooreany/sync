import unittest
from unittest.mock import patch, MagicMock
from gitflow_sync.core import (
    validate_branch_name,
    get_base_branches,
    check_gitflow_compliance,
    start_branch
)

class TestGitflowSync(unittest.TestCase):

    def test_validate_branch_name(self):
        self.assertTrue(validate_branch_name("main"))
        self.assertTrue(validate_branch_name("develop"))
        self.assertTrue(validate_branch_name("feature/login"))
        self.assertTrue(validate_branch_name("fix/bug-1"))
        self.assertFalse(validate_branch_name("my-custom-branch"))
        self.assertFalse(validate_branch_name("feat/something"))  # not in VALID_PREFIXES (feature/ is used)

    def test_get_base_branches(self):
        branches = ["main", "develop", "feature/abc"]
        base = get_base_branches(branches)
        self.assertEqual(base.get("production"), "main")
        self.assertEqual(base.get("development"), "develop")

    @patch("gitflow_sync.core.is_git_repo", return_value=True)
    @patch("gitflow_sync.core.list_local_branches", return_value=["main", "develop", "feature/test"])
    @patch("gitflow_sync.core.get_current_branch", return_value="develop")
    def test_check_compliance_success(self, mock_curr, mock_list, mock_repo):
        res = check_gitflow_compliance()
        self.assertTrue(res["is_compliant"])
        self.assertEqual(len(res["non_compliant_branches"]), 0)

    @patch("gitflow_sync.core.is_git_repo", return_value=True)
    @patch("gitflow_sync.core.list_local_branches", return_value=["develop", "invalid-branch"])
    @patch("gitflow_sync.core.get_current_branch", return_value="develop")
    def test_check_compliance_failure(self, mock_curr, mock_list, mock_repo):
        res = check_gitflow_compliance()
        self.assertFalse(res["is_compliant"])
        self.assertIn("invalid-branch", res["non_compliant_branches"])
        self.assertIn("Production branch ('main' or 'master') is missing locally.", res["warnings"])

    @patch("gitflow_sync.core.is_git_repo", return_value=True)
    @patch("gitflow_sync.core.list_local_branches", return_value=["main", "develop"])
    @patch("gitflow_sync.core.run_git")
    def test_start_branch(self, mock_run, mock_list, mock_repo):
        full_name = start_branch("feature", "new-ui")
        self.assertEqual(full_name, "feature/new-ui")
        mock_run.assert_any_call(["checkout", "develop"])
        mock_run.assert_any_call(["checkout", "-b", "feature/new-ui"])

    @patch("gitflow_sync.core.is_git_repo", return_value=True)
    @patch("gitflow_sync.core.get_current_branch", return_value="feature/new-ui")
    @patch("gitflow_sync.core.list_local_branches", return_value=["main", "develop", "feature/new-ui"])
    @patch("gitflow_sync.core.run_git")
    def test_finish_feature_branch(self, mock_run, mock_list, mock_curr, mock_repo):
        from gitflow_sync.core import finish_current_branch
        finish_current_branch(dry_run=False)
        mock_run.assert_any_call(["checkout", "develop"])
        mock_run.assert_any_call(["merge", "--no-ff", "feature/new-ui", "-m", "Merge feature/new-ui into develop"])
        mock_run.assert_any_call(["branch", "-d", "feature/new-ui"])

    @patch("gitflow_sync.core.is_git_repo", return_value=True)
    @patch("gitflow_sync.core.get_current_branch", return_value="release/1.0.0")
    @patch("gitflow_sync.core.list_local_branches", return_value=["main", "develop", "release/1.0.0"])
    @patch("gitflow_sync.core.run_git", return_value="")
    @patch("release_sync.core.sync_version_across_repo")
    def test_finish_release_branch(self, mock_sync, mock_run, mock_list, mock_curr, mock_repo):
        from gitflow_sync.core import finish_current_branch
        finish_current_branch(dry_run=False)
        mock_sync.assert_called_once()
        mock_run.assert_any_call(["checkout", "main"])
        mock_run.assert_any_call(["tag", "-a", "v1.0.0", "-m", "Release v1.0.0"])
        mock_run.assert_any_call(["checkout", "develop"])

