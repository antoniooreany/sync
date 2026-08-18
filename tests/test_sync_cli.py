import pytest
import subprocess
import sys
from unittest.mock import patch
from sync.__main__ import main, run_init

def test_run_init_success():
    with patch("subprocess.run") as mock_run:
        run_init()
        # Verify it called dp init and glnt init
        assert mock_run.call_count == 2
        
        args1, kwargs1 = mock_run.call_args_list[0]
        assert args1[0] == [sys.executable, "-m", "dependabot_sync.cli", "init"]
        assert kwargs1.get("check") is True
        
        args2, kwargs2 = mock_run.call_args_list[1]
        assert args2[0] == [sys.executable, "-m", "gitlint_sync.cli", "init"]
        assert kwargs2.get("check") is True

def test_run_init_failure():
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "cmd")
        with patch("sys.exit") as mock_exit:
            run_init()
            mock_exit.assert_called_once_with(1)

def test_main_routes_to_init():
    with patch("sys.argv", ["sync", "init"]):
        with patch("sync.__main__.run_init") as mock_run_init:
            main()
            mock_run_init.assert_called_once()
