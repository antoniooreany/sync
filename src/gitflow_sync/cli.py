import sys
import argparse
from gitflow_sync.constants import (
    EXIT_CODE_SUCCESS,
    EXIT_CODE_EXPECTED_ERROR,
    EXIT_CODE_ENV_ERROR,
    EXIT_CODE_OTHER_ERROR
)
from gitflow_sync.core import (
    is_git_repo,
    check_gitflow_compliance,
    start_branch
)

def main():
    # Reconfigure console output encoding on Windows to support emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="Gitflow Sync CLI (gf)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: check
    subparsers.add_parser("check", help="Verify Gitflow compliance of the local repository")

    # Subcommand: start
    start_parser = subparsers.add_parser("start", help="Start a new Gitflow branch")
    start_parser.add_argument("type", choices=["feature", "fix", "bugfix", "release", "hotfix", "support"], help="Type of branch to create")
    start_parser.add_argument("name", help="Name of the branch (e.g. login-page)")

    # Subcommand: finish
    finish_parser = subparsers.add_parser("finish", help="Finish the current Gitflow branch")
    finish_parser.add_argument("--dry-run", action="store_true", help="Print updates but do not write changes")
    finish_parser.add_argument("--force", action="store_true", help="Allow version downgrade/override")

    args = parser.parse_args()

    if not is_git_repo():
        print("❌ Error: Not inside a valid Git repository.", file=sys.stderr)
        sys.exit(EXIT_CODE_ENV_ERROR)

    if args.command == "check":
        try:
            res = check_gitflow_compliance()
            print(f"ℹ️  Current Branch: {res['current_branch']}")
            print(f"📦 Production Branch: {res['production_branch'] or 'None'}")
            print(f"🛠️  Development Branch: {res['development_branch'] or 'None'}")
            
            if res["warnings"]:
                print("\n⚠️  Warnings:")
                for w in res["warnings"]:
                    print(f"  • {w}")
            
            if res["non_compliant_branches"]:
                print("\n❌ Non-compliant branches found locally:")
                for b in res["non_compliant_branches"]:
                    print(f"  • {b}")
            
            if res["is_compliant"]:
                print("\n🎉 Repository is fully compliant with Gitflow standards!")
                sys.exit(EXIT_CODE_SUCCESS)
            else:
                sys.exit(EXIT_CODE_EXPECTED_ERROR)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_OTHER_ERROR)

    elif args.command == "start":
        try:
            full_name = start_branch(args.type, args.name)
            print(f"🌱 Created and switched to branch: {full_name}")
            sys.exit(EXIT_CODE_SUCCESS)
        except Exception as e:
            print(f"💥 Error starting branch: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

    elif args.command == "finish":
        from gitflow_sync.core import finish_current_branch
        try:
            finish_current_branch(dry_run=args.dry_run, force=args.force)
            sys.exit(EXIT_CODE_SUCCESS)
        except Exception as e:
            print(f"💥 Error finishing branch: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

if __name__ == "__main__":
    main()
