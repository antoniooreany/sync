"""Smoke tests for gitflow_sync CLI exit codes."""
from unittest.mock import patch

import pytest

from gitflow_sync.constants import (
    EXIT_CODE_ENV_ERROR,
    EXIT_CODE_EXPECTED_ERROR,
    EXIT_CODE_SUCCESS,
)


def test_gf_check_not_a_repo_exits_env_error():
    with patch("gitflow_sync.cli.chdir_to_git_root"), \
         patch("gitflow_sync.cli.is_git_repo", return_value=False), \
         patch("sys.argv", ["gf", "check"]):
        with pytest.raises(SystemExit) as exc:
            from gitflow_sync.cli import main
            main()
        assert exc.value.code == EXIT_CODE_ENV_ERROR


def test_gf_check_compliant_exits_success():
    compliant = {
        "current_branch": "develop",
        "production_branch": "main",
        "development_branch": "develop",
        "warnings": [],
        "non_compliant_branches": [],
        "is_compliant": True,
    }
    with patch("gitflow_sync.cli.chdir_to_git_root"), \
         patch("gitflow_sync.cli.is_git_repo", return_value=True), \
         patch("gitflow_sync.cli.check_gitflow_compliance", return_value=compliant), \
         patch("sys.argv", ["gf", "check"]):
        with pytest.raises(SystemExit) as exc:
            from gitflow_sync.cli import main
            main()
        assert exc.value.code == EXIT_CODE_SUCCESS


def test_gf_check_noncompliant_exits_expected_error():
    noncompliant = {
        "current_branch": "develop",
        "production_branch": None,
        "development_branch": "develop",
        "warnings": ["Production branch missing"],
        "non_compliant_branches": ["weird"],
        "is_compliant": False,
    }
    with patch("gitflow_sync.cli.chdir_to_git_root"), \
         patch("gitflow_sync.cli.is_git_repo", return_value=True), \
         patch("gitflow_sync.cli.check_gitflow_compliance", return_value=noncompliant), \
         patch("sys.argv", ["gf", "check"]):
        with pytest.raises(SystemExit) as exc:
            from gitflow_sync.cli import main
            main()
        assert exc.value.code == EXIT_CODE_EXPECTED_ERROR


def test_gf_start_success():
    with patch("gitflow_sync.cli.chdir_to_git_root"), \
         patch("gitflow_sync.cli.is_git_repo", return_value=True), \
         patch("gitflow_sync.cli.start_branch", return_value="feature/login"), \
         patch("sys.argv", ["gf", "start", "feature", "login"]):
        with pytest.raises(SystemExit) as exc:
            from gitflow_sync.cli import main
            main()
        assert exc.value.code == EXIT_CODE_SUCCESS
