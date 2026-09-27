import subprocess
import sys
import os
import io
import importlib
from contextlib import redirect_stdout, redirect_stderr

# Disable dotenv warnings and autoloading
os.environ.setdefault("FLASK_SKIP_DOTENV", "1")

from flask import Flask, render_template, request, jsonify

from sync import find_git_root

app = Flask(__name__)

_git_root = find_git_root()
CWD = str(_git_root) if _git_root else os.getcwd()

# Explicit allowlist of CLI modules the dashboard may invoke.
SCRIPT_MAP = {
    "pr": "pr_sync.cli",
    "rl": "release_sync.cli",
    "dp": "dependabot_sync.cli",
    "glnt": "gitlint_sync.cli",
    "cm": "gitlint_sync.commit_generator",
    "gf": "gitflow_sync.cli",
    "fs": "feature_sync.cli",
    "vs": "version_sync.cli",
    "doc": "doc_sync.cli",
    "sync": "sync.__main__",
}

# Lightweight CLIs safe to run in-process; heavier ones stay isolated in a subprocess.
IN_PROCESS_SCRIPTS = frozenset({"vs", "dp", "glnt", "gf", "cm", "doc"})


@app.route("/", methods=["GET"])
def index():
    """Render the main dashboard page with dynamic git branches list."""
    branches = ["develop", "main"]
    repo_name = os.path.basename(CWD)
    try:
        res = subprocess.run(
            ["git", "branch", "--format=%(refname:short)"],
            capture_output=True, text=True, cwd=CWD
        )
        if res.returncode == 0:
            local_branches = [b.strip() for b in res.stdout.splitlines() if b.strip()]
            if local_branches:
                branches = local_branches
    except Exception:
        pass

    if "develop" in branches:
        branches.remove("develop")
        branches.insert(0, "develop")
    elif "develop" not in branches:
        branches.insert(0, "develop")

    return render_template("index.html", branches=branches, repo_name=repo_name)


@app.route("/run", methods=["POST"])
def run_command():
    """Execute an allowlisted monorepo CLI with parameters.

    Expected JSON payload:
        {
            "script": "pr|rl|dp|glnt|cm|gf|fs|vs|doc|sync",
            "args": ["list", "of", "arguments"]
        }
    """
    data = request.get_json(silent=True) or {}
    script = data.get("script")
    args = data.get("args", [])

    if not isinstance(args, list) or not all(isinstance(a, str) for a in args):
        return jsonify({
            "returncode": 1,
            "stdout": "",
            "stderr": "args must be a list of strings",
        }), 400

    if not script or script not in SCRIPT_MAP:
        return jsonify({
            "returncode": 1,
            "stdout": "",
            "stderr": f"Invalid or missing script name: {script}. Allowed: {sorted(SCRIPT_MAP)}"
        }), 400

    module_name = SCRIPT_MAP[script]

    if script in IN_PROCESS_SCRIPTS:
        old_argv = sys.argv
        sys.argv = [script] + args

        f_stdout = io.StringIO()
        f_stderr = io.StringIO()

        returncode = 0
        cwd_backup = os.getcwd()
        try:
            os.chdir(CWD)
            mod = importlib.import_module(module_name)
            with redirect_stdout(f_stdout), redirect_stderr(f_stderr):
                try:
                    mod.main()
                except SystemExit as se:
                    if se.code is not None:
                        if isinstance(se.code, int):
                            returncode = se.code
                        else:
                            returncode = 1 if se.code else 0
        except Exception as e:
            f_stderr.write(f"Execution failed: {str(e)}")
            returncode = 1
        finally:
            sys.argv = old_argv
            os.chdir(cwd_backup)

        return jsonify({
            "returncode": returncode,
            "stdout": f_stdout.getvalue(),
            "stderr": f_stderr.getvalue()
        })

    cmd = [sys.executable, "-m", module_name] + args
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=CWD
    )

    return jsonify({
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
