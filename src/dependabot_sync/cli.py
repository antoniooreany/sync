import sys
import argparse
from pathlib import Path
from dependabot_sync.core import is_git_root, get_github_user, generate_dependabot_config, write_config

from sync import chdir_to_git_root

def main():
    chdir_to_git_root()
    # Reconfigure console output encoding on Windows to support emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass # Fallback for older python versions

    parser = argparse.ArgumentParser(description="Dependabot Sync CLI (dp)")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Subcommand: init
    init_parser = subparsers.add_parser("init", help="Initialize standard Dependabot config in the current repository")
    init_parser.add_argument("--weekly", action="store_true", help="Set update schedule to weekly (default)")
    init_parser.add_argument("--monthly", action="store_true", help="Set update schedule to monthly")
    init_parser.add_argument("--limit", type=int, default=3, help="Limit maximum open pull requests (default: 3)")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing configuration")

    args = parser.parse_args()

    if args.command == "init":
        # 1. Verification: Git Root
        if not is_git_root():
            print("❌ Error: Not inside the root of a Git repository.", file=sys.stderr)
            sys.exit(2)

        # 2. Extract configuration
        interval = "daily"
        if args.weekly:
            interval = "weekly"
        elif args.monthly:
            interval = "monthly"

        # 3. Detect assignee (using gh CLI)
        assignee = get_github_user()
        if assignee:
            print(f"👤 Detected GitHub user: {assignee} (automatically set as assignee)")
        else:
            print("ℹ️  No authenticated GitHub user found (assignees block skipped)")

        # 4. Generate & write
        config_file = Path.cwd() / ".github" / "dependabot.yml"
        force_write = args.force
        if config_file.exists() and not force_write:
            try:
                ans = input("⚠️  Dependabot configuration already exists. Overwrite? [y/N]: ").strip().lower()
                if ans in ["y", "yes"]:
                    force_write = True
                else:
                    print("Skipped.")
                    sys.exit(0)
            except KeyboardInterrupt:
                print("\nAborted.")
                sys.exit(1)

        try:
            config_content = generate_dependabot_config(interval, args.limit, assignee)
            written_path = write_config(Path.cwd(), config_content, force=force_write)
            print(f"🎉 Successfully initialized Dependabot configuration at: {written_path}")
            sys.exit(0)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            sys.exit(3)

if __name__ == "__main__":
    main()
