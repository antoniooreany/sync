import subprocess
import sys
import os

# Disable dotenv warnings and autoloading
os.environ.setdefault("FLASK_SKIP_DOTENV", "1")

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from sync import find_git_root
# Base directory setup
_git_root = find_git_root()
CWD = str(_git_root) if _git_root else os.getcwd()

@app.route("/", methods=["GET"])
def index():
    """Render the main dashboard page with dynamic git branches list."""
    import subprocess
    import os
    branches = ["develop", "main"]
    repo_name = os.path.basename(CWD)
    try:
        # Get list of local git branches
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
    
    # Ensure develop is first or present, and main is also included
    if "develop" in branches:
        branches.remove("develop")
        branches.insert(0, "develop")
    elif "develop" not in branches:
        branches.insert(0, "develop")

    return render_template("index.html", branches=branches, repo_name=repo_name)

@app.route("/run", methods=["POST"])
def run_command():
    """Execute target monorepo script with parameters.
    
    Expected JSON payload:
        {
            "script": "pr|rl|dp|glnt|cm|gf|fs|vs",
            "args": ["list", "of", "arguments"]
        }
    """
    data = request.get_json(silent=True) or {}
    script = data.get("script")
    args = data.get("args", [])

    script_map = {
        "pr": "pr_sync.cli",
        "rl": "release_sync.cli",
        "dp": "dependabot_sync.cli",
        "glnt": "gitlint_sync.cli",
        "cm": "gitlint_sync.commit_generator",
        "gf": "gitflow_sync.cli",
        "fs": "feature_sync.cli",
        "vs": "version_sync.cli"
    }

    if not script or script not in script_map:
        return jsonify({
            "returncode": 1,
            "stdout": "",
            "stderr": f"Invalid or missing script name: {script}"
        }), 400

    module_name = script_map[script]
    
    # Speed optimization: For fast commands, we can run them in-process by mocking sys.argv.
    # This completely eliminates Python interpreter startup latency (which is ~100-300ms on Windows).
    # We execute this inside a clean sandbox context to prevent sys.exit() from stopping the Flask server.
    import io
    from contextlib import redirect_stdout, redirect_stderr
    import importlib
    
    # We still use subprocess for 'pr' and 'rl' because they make heavy network calls, write tags, 
    # and we want to keep them fully isolated, but simple utilities run directly and instantly.
    if script in ["vs", "dp", "glnt", "gf", "cm"]:
        old_argv = sys.argv
        sys.argv = [script] + args
        
        f_stdout = io.StringIO()
        f_stderr = io.StringIO()
        
        returncode = 0
        cwd_backup = os.getcwd()
        try:
            # Change directory to CWD so that functions relying on os.getcwd() or Path.cwd() resolve properly
            os.chdir(CWD)
            
            # Dynamically import the module and locate its main()
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

    # Fallback to subprocess for heavy scripts (pr, rl, etc.)
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

@app.route("/compress", methods=["POST"])
def compress():
    """Run PowerShell Compress-Archive to bundle SboxGame Windows build.
    Returns detailed result.
    """
    import pathlib, shlex
    build_dir = pathlib.Path(r"C:/Users/anton/Projects/SboxGame/Builds/Windows")
    if not build_dir.is_dir():
        return jsonify({
            "returncode": 1,
            "stderr": f"Build directory not found: {build_dir}",
            "stdout": "",
        })
    files = list(build_dir.glob("*"))
    if not files:
        return jsonify({
            "returncode": 1,
            "stderr": f"No files found in {build_dir}",
            "stdout": "",
        })
    # In PowerShell, multiple paths passed to -Path must be separated by commas, not spaces.
    # Alternatively, we can use a wildcard path string or comma-joined array.
    ps_cmd = (
        "Compress-Archive -Path "
        + ", ".join([f"'{str(p)}'" for p in files])
        + " -DestinationPath 'C:/Users/anton/Projects/SboxGame/Release/SboxGame_v1.1.1.zip' -Force"
    )
    result = subprocess.run([
        "powershell",
        "-Command",
        ps_cmd,
    ], capture_output=True, text=True)
    return jsonify({
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    })

@app.route("/download", methods=["GET"])
def download_release():
    """Download the generated release zip file."""
    from flask import send_file
    target_path = "C:/Users/anton/Projects/SboxGame/Release/SboxGame_v1.1.1.zip"
    if not os.path.exists(target_path):
        return "Archive not found. Please click 'Create Release Zip' first.", 404
    return send_file(target_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
