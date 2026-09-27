import sys
import argparse
from pathlib import Path
from release_sync.constants import (
    EXIT_CODE_SUCCESS,
    EXIT_CODE_EXPECTED_ERROR,
    EXIT_CODE_ENV_ERROR,
    EXIT_CODE_OTHER_ERROR,
    DEFAULT_TO_REF,
    DEFAULT_CHANGELOG_FILENAME
)
from release_sync.core import (
    get_latest_tag,
    verify_tag_does_not_exist,
    get_commits_between,
    fetch_merged_prs,
    compile_release_notes,
    prepend_to_changelog,
    create_git_tag,
    push_git_tag,
    create_github_release,
    commit_and_push_release,
    sync_version_across_repo,
    detect_current_version,
    calculate_bump,
    run_git_command,
    run_gh_command
)

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

    parser = argparse.ArgumentParser(description="Release Sync CLI (rl)")
    parser.add_argument("version", nargs="?", help="Semantic version of the target release (e.g. 0.3.0) or bump level (major/minor/patch). Default: patch")
    parser.add_argument("--from", dest="from_ref", help="Exclusive starting git reference. Default: latest release tag")
    parser.add_argument("--to", dest="to_ref", default=DEFAULT_TO_REF, help="Inclusive ending git reference. Default: HEAD")
    parser.add_argument("--dry-run", action="store_true", help="Do not write files, tag commits, or create GitHub Releases")
    parser.add_argument("--force", action="store_true", help="Allow version downgrade")
    parser.add_argument("--changelog", default=DEFAULT_CHANGELOG_FILENAME, help="Path to CHANGELOG file. Default: CHANGELOG.md")

    args = parser.parse_args()

    project_root = Path.cwd()
    target_version = args.version
    if not target_version:
        target_version = "patch"

    if target_version in ["major", "minor", "patch"]:
        try:
            current_v = detect_current_version(project_root)
            bumped_v = calculate_bump(current_v, target_version)
            print(f"📈 Auto-detected version bump ({target_version}): {current_v} -> {bumped_v}")
            target_version = bumped_v
        except Exception as e:
            print(f"❌ Error auto-detecting current version: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

    # 1. Environment Verification: Git & GitHub CLI
    try:
        run_git_command(["rev-parse", "--is-inside-work-tree"])
    except Exception:
        print("❌ Error: Not inside a valid Git repository.", file=sys.stderr)
        sys.exit(EXIT_CODE_ENV_ERROR)

    try:
        run_gh_command(["auth", "status"])
    except Exception:
        print("❌ Error: GitHub CLI is not authenticated or not installed.", file=sys.stderr)
        sys.exit(EXIT_CODE_ENV_ERROR)

    # 2. Invariant: Check if version tag already exists
    if not args.dry_run:
        try:
            verify_tag_does_not_exist(target_version)
        except ValueError as e:
            print(f"❌ Error: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

    # 3. Resolve ref range
    from_ref = args.from_ref
    if not from_ref:
        from_ref = get_latest_tag()
        if from_ref:
            print(f"🏷️  Latest tag detected: {from_ref}")
        else:
            print("ℹ️  No tags found. Querying all history up to target ref.")

    print(f"🔍 Analyzing changes between {from_ref or 'beginning'} and {args.to_ref}...")

    # 4. Fetch commits in range
    try:
        commits = get_commits_between(from_ref, args.to_ref)
    except Exception as e:
        print(f"❌ Error resolving references: {e}", file=sys.stderr)
        sys.exit(EXIT_CODE_EXPECTED_ERROR)

    if not commits:
        print(f"❌ Error: No commits found between {from_ref or 'beginning'} and {args.to_ref}.", file=sys.stderr)
        sys.exit(EXIT_CODE_EXPECTED_ERROR)

    # 5. Fetch merged PRs and match them with commits
    print("📥 Fetching merged PRs from GitHub...")
    merged_prs = fetch_merged_prs()
    commit_set = set(commits)
    
    matched_prs = []
    for pr in merged_prs:
        merge_commit = pr.get("mergeCommit")
        if isinstance(merge_commit, dict):
            merge_hash = merge_commit.get("oid")
            if merge_hash and merge_hash in commit_set:
                matched_prs.append(pr)

    # 6. Compile release notes
    if matched_prs:
        notes = compile_release_notes(matched_prs)
    else:
        print("ℹ️  No merged PRs matched the commit range. Falling back to git log for release notes.")
        # Fallback: compile notes from raw git logs
        fallback_notes = []
        for c_hash in commits:
            try:
                c_subject = run_git_command(["show", "-s", "--format=%s", c_hash])
                fallback_notes.append(f"- {c_subject} ({c_hash[:7]})")
            except Exception:
                pass
        notes = "### Changes\n" + "\n".join(fallback_notes) if fallback_notes else "### Changes\n- Initial release / minor changes"
    
    # 7. Execute Actions or Dry-Run
    if args.dry_run:
        print(f"🔍 [DRY RUN] Would synchronize version to: {target_version}")
        print("\n--- [DRY RUN] Generated Release Notes ---")
        print(notes)
        print("-----------------------------------------\n")
        sys.exit(EXIT_CODE_SUCCESS)

    try:
        # Sync version across codebase
        print(f"📈 Synchronizing version to {target_version}...")
        project_root = Path.cwd()
        sync_version_across_repo(project_root, target_version, force=args.force)

        # Prepend to Changelog
        changelog_path = Path(args.changelog)
        prepend_to_changelog(changelog_path, target_version, notes)
        print(f"📝 Prepend release notes to: {changelog_path.name}")

        # Commit and push release changes (changelog + version configs)
        print("📦 Committing and pushing release changes...")
        commit_and_push_release(target_version, changelog_path)

        # Git tag
        create_git_tag(target_version)
        print(f"🏷️  Created git tag: v{target_version}")
        
        # Push tag
        print("🏷️  Pushing git tag to origin...")
        push_git_tag(target_version)

        # GitHub Release
        print("🚀 Creating GitHub Release...")
        create_github_release(target_version, notes)
        print(f"🎉 Successfully released v{target_version}!")
        sys.exit(EXIT_CODE_SUCCESS)
    except Exception as e:
        print(f"💥 Release failed: {e}", file=sys.stderr)
        sys.exit(EXIT_CODE_OTHER_ERROR)

if __name__ == "__main__":
    main()
