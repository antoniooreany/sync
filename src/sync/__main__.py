import subprocess
import sys

def main():
    """Entry point for the workspace sync tool.
    Synchronizes the local git repository with remote and updates dependencies.
    """
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
        subprocess.run([sys.executable, "-m", "pip", "install", "-e", "."], check=True)
        print("✅ Dependencies updated.")
        print("🎉 Workspace synchronized successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during sync: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
