import sys
import argparse
from pathlib import Path

from version_sync.constants import (
    EXIT_CODE_SUCCESS,
    EXIT_CODE_EXPECTED_ERROR,
    EXIT_CODE_ENV_ERROR,
)
from version_sync.core import (
    detect_current_version,
    calculate_bump,
    sync_version_across_repo,
)

def cmd_detect(args: argparse.Namespace) -> int:
    """Detect and print the current project version."""
    try:
        project_root = Path.cwd()
        current = detect_current_version(project_root)
        print(f"Current version: {current}")
        return EXIT_CODE_SUCCESS
    except Exception as e:
        print(f"❌ Error detecting version: {e}", file=sys.stderr)
        return EXIT_CODE_EXPECTED_ERROR

def cmd_bump(args: argparse.Namespace) -> int:
    """Bump the current version according to the supplied level."""
    if not args.level:
        print("❌ Bump level is required (major, minor, patch)", file=sys.stderr)
        return EXIT_CODE_EXPECTED_ERROR
    try:
        project_root = Path.cwd()
        current = detect_current_version(project_root)
        target = calculate_bump(current, args.level)
        print(f"📈 Bumping version from {current} -> {target} ({args.level})")
        return cmd_sync_internal(project_root, target, args)
    except Exception as e:
        print(f"❌ Error during bump: {e}", file=sys.stderr)
        return EXIT_CODE_EXPECTED_ERROR

def cmd_set(args: argparse.Namespace) -> int:
    """Set the project version to an explicit value."""
    if not args.version:
        print("❌ Version value is required", file=sys.stderr)
        return EXIT_CODE_EXPECTED_ERROR
    try:
        project_root = Path.cwd()
        target = args.version
        print(f"🔧 Setting version to {target}")
        return cmd_sync_internal(project_root, target, args)
    except Exception as e:
        print(f"❌ Error setting version: {e}", file=sys.stderr)
        return EXIT_CODE_EXPECTED_ERROR

def cmd_sync_internal(project_root: Path, target_version: str, args: argparse.Namespace) -> int:
    """Internal helper to perform the sync across repository files."""
    if args.dry_run:
        print(f"🔍 [DRY RUN] Would sync version to: {target_version}")
        return EXIT_CODE_SUCCESS
    try:
        modified_files = sync_version_across_repo(project_root, target_version, force=args.force)
        if not modified_files:
            print(f"ℹ️  No version fields matched. Version set to {target_version} (no files changed)")
        else:
            print(f"🎉 Successfully synchronized version '{target_version}' across:")
            for f in modified_files:
                print(f"  • {f.relative_to(project_root)}")
        return EXIT_CODE_SUCCESS
    except Exception as e:
        print(f"❌ Error syncing version: {e}", file=sys.stderr)
        return EXIT_CODE_EXPECTED_ERROR

def main() -> None:
    # Ensure Windows console can display emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass  # Older Python versions may not support reconfigure

    parser = argparse.ArgumentParser(description="Version Sync CLI (v)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Detect subcommand
    parser_detect = subparsers.add_parser("detect", help="Detect and display the current project version")
    parser_detect.set_defaults(func=cmd_detect)

    # Bump subcommand
    parser_bump = subparsers.add_parser("bump", help="Bump the current version (major, minor, patch)")
    parser_bump.add_argument("level", choices=["major", "minor", "patch"], help="Level to bump")
    parser_bump.add_argument("--dry-run", action="store_true", help="Show changes without writing them")
    parser_bump.add_argument("--force", action="store_true", help="Allow version downgrade")
    parser_bump.set_defaults(func=cmd_bump)

    # Set subcommand
    parser_set = subparsers.add_parser("set", help="Set the project version explicitly")
    parser_set.add_argument("version", help="Target version (e.g., 1.2.3)")
    parser_set.add_argument("--dry-run", action="store_true", help="Show changes without writing them")
    parser_set.add_argument("--force", action="store_true", help="Allow version downgrade")
    parser_set.set_defaults(func=cmd_set)

    # Sync subcommand (useful if version already set)
    parser_sync = subparsers.add_parser("sync", help="Synchronize an explicit version across the repo")
    parser_sync.add_argument("version", help="Version to sync across files")
    parser_sync.add_argument("--dry-run", action="store_true", help="Show changes without writing them")
    parser_sync.add_argument("--force", action="store_true", help="Allow overwriting existing version fields")
    parser_sync.set_defaults(func=lambda args: cmd_sync_internal(Path.cwd(), args.version, args))

    args = parser.parse_args()
    exit_code = args.func(args)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
