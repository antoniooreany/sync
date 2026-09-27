import subprocess
import sys
from pathlib import Path

def run_sync_workspace():
    print("🔄 Synchronizing local workspace...")
    try:
        subprocess.run(["git", "fetch", "--all", "--prune"], check=True)
        print("✅ Fetched from origin.")
        subprocess.run(["git", "pull", "--rebase"], check=True)
        print("✅ Pulled remote changes.")
        
        # Install dependencies based on project type
        root = Path.cwd()
        if (root / "package.json").exists():
            print("📦 Found package.json, running npm install...")
            subprocess.run(["npm", "install"], check=True)
            print("✅ Node dependencies updated.")
        elif (root / "pyproject.toml").exists() or (root / "setup.py").exists():
            print("🐍 Found Python project configuration, running pip install...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
            print("✅ Python dependencies updated.")
        elif (root / "requirements.txt").exists():
            print("🐍 Found requirements.txt, running pip install...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Python dependencies updated.")
        else:
            print("ℹ️ No recognized package manager configuration found. Skipping dependency update.")
            
        print("🎉 Workspace synchronized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during sync: {e}", file=sys.stderr)
        sys.exit(1)

def run_ui():
    from pr_sync.ui.app import app
    import webbrowser
    import threading
    import os

    print("🚀 Starting syNC UI...")
    
    # Open browser only in the main process (not the reloader child)
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(1.0, lambda: webbrowser.open("http://127.0.0.1:5000/")).start()
        
    app.run(host="127.0.0.1", port=5000, debug=True)

def run_init():
    print("🚀 Initializing repository (Dependabot + Gitlint)...")
    try:
        print("\n--- Running Dependabot Initialization ---")
        subprocess.run([sys.executable, "-m", "dependabot_sync.cli", "init"], check=True)
        print("\n--- Running Gitlint Initialization ---")
        subprocess.run([sys.executable, "-m", "gitlint_sync.cli", "init"], check=True)
        print("\n✅ Repository initialization complete.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during initialization: {e}", file=sys.stderr)
        sys.exit(1)

from sync import chdir_to_git_root

def main():
    """Entry point for the workspace sync tool.
    Synchronizes the local git repository or runs the web UI.
    """
    chdir_to_git_root()
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    if len(sys.argv) > 1:
        if sys.argv[1] == "ui":
            run_ui()
            return
        elif sys.argv[1] == "init":
            run_init()
            return

    run_sync_workspace()

if __name__ == "__main__":
    main()
