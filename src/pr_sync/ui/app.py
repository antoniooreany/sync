import subprocess
import sys
import os

# Disable dotenv warnings and autoloading
os.environ.setdefault("FLASK_SKIP_DOTENV", "1")

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Base directory setup
CWD = "C:/Users/anton/Projects/sync"

@app.route("/", methods=["GET"])
def index():
    """Render the main dashboard page."""
    return render_template("index.html")

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
    ps_cmd = (
        "Compress-Archive -Path "
        + " ".join([shlex.quote(str(p)) for p in files])
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

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
