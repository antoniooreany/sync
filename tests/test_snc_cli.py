import sys
import subprocess
from snc.cli import run_cmd

def test_run_cmd_success():
    # Use python executable to run a quick inline script returning 0
    code = run_cmd([sys.executable, "-c", "import sys; sys.exit(0)"])
    assert code == 0

def test_run_cmd_error():
    # Return code 5
    code = run_cmd([sys.executable, "-c", "import sys; sys.exit(5)"])
    assert code == 5

def test_run_cmd_missing():
    # Non-existent command
    code = run_cmd(["non_existent_command_12345"])
    assert code == 127
