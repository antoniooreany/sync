import subprocess
import sys
from pathlib import Path

def main():
    """Entry point for the workspace sync tool.
    Synchronizes the local git repository with remote and updates dependencies.
    """
    if len(sys.argv) > 1 and sys.argv[1] == "ui":
        from pr_sync.ui.app import app
        print("🚀 Starting syNC UI...")
        app.run(host="127.0.0.1", port=5000, debug=True)
        return

    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

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

if __name__ == "__main__":
    main()

