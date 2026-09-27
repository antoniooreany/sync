"""Smoke tests for doc_sync CLI."""
from unittest.mock import patch

import pytest


def test_doc_main_no_staged_exits_zero():
    with patch("doc_sync.cli.chdir_to_git_root"), \
         patch("doc_sync.cli.get_staged_files", return_value=[]), \
         patch("sys.argv", ["doc"]):
        with pytest.raises(SystemExit) as exc:
            from doc_sync.cli import main
            main()
        assert exc.value.code == 0


def test_doc_main_with_files_calls_generator():
    with patch("doc_sync.cli.chdir_to_git_root"), \
         patch("sys.argv", ["doc", "src/foo.py"]), \
         patch("pr_sync.code_to_docs_generator.run_code_to_docs", return_value=["docs/foo.md"]) as mock_gen:
        from doc_sync.cli import main
        main()
        mock_gen.assert_called_once_with(["src/foo.py"])


def test_doc_main_empty_explicit_list_exits_one():
    with patch("doc_sync.cli.chdir_to_git_root"), \
         patch("doc_sync.cli.get_all_src_files", return_value=[]), \
         patch("sys.argv", ["doc", "--all"]):
        with pytest.raises(SystemExit) as exc:
            from doc_sync.cli import main
            main()
        assert exc.value.code == 1
