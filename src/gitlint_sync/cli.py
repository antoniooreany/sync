import sys
import argparse
from pathlib import Path
from gitlint_sync.core import is_git_root, write_configs

def main():
    # Reconfigure console output encoding on Windows to support emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass # Fallback for older python versions

    parser = argparse.ArgumentParser(description="Gitlint Sync CLI (glint)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Subcommand: init
    init_parser = subparsers.add_parser("init", help="Initialize Gitlint Conventional Commits config, hook, and workflow")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing configurations")

    args = parser.parse_args()

    if args.command == "init":
        # 1. Verification: Git Root
        if not is_git_root():
            print("❌ Error: Not inside the root of a Git repository.", file=sys.stderr)
            sys.exit(2)

        # 2. Write configs
        try:
            written_files = write_configs(Path.cwd(), force=args.force)
            print("🎉 Successfully initialized Gitlint configurations:")
            for f in written_files:
                # If path is under current dir, show relative, otherwise full
                try:
                    rel = f.relative_to(Path.cwd())
                    print(f"  • {rel}")
                except ValueError:
                    print(f"  • {f}")
            print("💡 Pro-Tip: Make sure you run 'pip install gitlint' globally to enable local commit hook!")
            sys.exit(0)
        except FileExistsError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            sys.exit(3)

if __name__ == "__main__":
    main()
