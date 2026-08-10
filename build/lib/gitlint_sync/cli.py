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
        target_dir = Path.cwd()
        gitlint_file = target_dir / ".gitlint"
        hook_file = target_dir / ".git" / "hooks" / "commit-msg"
        workflow_file = target_dir / ".github" / "workflows" / "commit-lint.yml"

        existing = []
        if gitlint_file.exists():
            existing.append(".gitlint")
        if hook_file.exists():
            existing.append(".git/hooks/commit-msg")
        if workflow_file.exists():
            existing.append(".github/workflows/commit-lint.yml")

        force_write = args.force
        if existing and not force_write:
            try:
                print(f"⚠️  Configuration files already exist: {', '.join(existing)}")
                ans = input("Overwrite all? [y/N]: ").strip().lower()
                if ans in ["y", "yes"]:
                    force_write = True
                else:
                    print("Skipped.")
                    sys.exit(0)
            except KeyboardInterrupt:
                print("\nAborted.")
                sys.exit(1)

        try:
            written_files = write_configs(target_dir, force=force_write)
            print("🎉 Successfully initialized Gitlint configurations:")
            for f in written_files:
                try:
                    rel = f.relative_to(target_dir)
                    print(f"  • {rel}")
                except ValueError:
                    print(f"  • {f}")
            print("💡 Pro-Tip: Make sure you run 'pip install gitlint' globally to enable local commit hook!")
            sys.exit(0)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            sys.exit(3)

if __name__ == "__main__":
    main()
