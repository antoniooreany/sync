import subprocess
import sys
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Render the main UI page."""
    return render_template("index.html")

@app.route("/sync", methods=["POST"])
def sync():
    """Execute the PR sync process with parameters from the UI.

    Expected JSON payload:
        {"base": "branch-name", "model": "optional-model-name"}
    """
    data = request.get_json(silent=True) or {}
    base = data.get("base", "develop")
    model = data.get("model")

    # Build command line arguments for the existing CLI
    cmd = [sys.executable, "-m", "sync", "--base", base]
    if model:
        cmd.extend(["--model", model])

    # Run the sync process synchronously and capture output
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd="C:/Users/anton/Projects/sync",
    )

    response = {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

# New endpoint to create release zip using PowerShell Compress-Archive
@app.route("/compress", methods=["POST"])
def compress():
    """Run PowerShell Compress-Archive to bundle SboxGame Windows build."""
    ps_cmd = "Compress-Archive -Path 'C:/Users/anton/Projects/SboxGame/Builds/Windows/*' -DestinationPath 'C:/Users/anton/Projects/SboxGame/Release/SboxGame_v1.1.1.zip' -Force"
    result = subprocess.run([
        "powershell",
        "-Command",
        ps_cmd
    ], capture_output=True, text=True)
    return jsonify({
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    })
