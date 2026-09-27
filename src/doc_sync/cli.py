import sys
import argparse
import subprocess
from pathlib import Path

def run_git(args: list[str]) -> str:
    res = subprocess.run(["git"] + args, capture_output=True, text=True, encoding="utf-8", check=True)
    return res.stdout.strip()

def get_staged_files() -> list[str]:
    try:
        out = run_git(["diff", "--cached", "--name-only"])
        return [f for f in out.split("\n") if f.strip()]
    except subprocess.CalledProcessError:
        return []

def get_all_src_files() -> list[str]:
    # Return all .py files in src/
    root = Path.cwd()
    src_dir = root / "src"
    if not src_dir.exists():
        return []
    return [str(p.relative_to(root)) for p in src_dir.rglob("*.py") if p.is_file()]

def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="Documentation Generator (doc)")
    parser.add_argument("--all", action="store_true", help="Generate docs for all files in src/")
    parser.add_argument("--staged", action="store_true", help="Generate docs for staged files (default if no args)")
    parser.add_argument("files", nargs="*", help="Specific files to generate docs for")
    args = parser.parse_args()

    files_to_process = []
    if args.files:
        files_to_process = args.files
    elif args.all:
        files_to_process = get_all_src_files()
    else:
        # Default to staged files if --all or files not provided
        staged = get_staged_files()
        if not staged:
            print("ℹ️ No staged files. Use --all to generate for all files or provide specific files.")
            sys.exit(0)
        files_to_process = staged

    if not files_to_process:
        print("❌ No files to process.")
        sys.exit(1)

    # Use the existing generator
    try:
        from pr_sync.code_to_docs_generator import run_code_to_docs
    except ImportError:
        print("❌ Error: pr_sync.code_to_docs_generator module not found.")
        sys.exit(1)

    print(f"📚 Generating documentation for {len(files_to_process)} file(s)...")
    try:
        generated = run_code_to_docs(files_to_process)
        if generated:
            print(f"🎉 Successfully generated and staged docs for {len(generated)} file(s).")
        else:
            print("ℹ️ No documentation was generated (maybe no Python files were in the list).")
    except Exception as e:
        print(f"❌ Failed to generate documentation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
