import sys
import argparse
import time
from toolkit.git_api import get_current_branch, get_diff, get_commits, get_changed_files
from toolkit.gh_api import check_auth, find_open_pr, create_pr, update_pr, add_labels
from toolkit.pr_body import render_pr_body
from toolkit.invariants import check_no_empty_diff_action
from toolkit.docs_generator import infer_type_label, infer_area_labels

def main():
    try:
        # Reconfigure console output encoding on Windows to support emojis
        if sys.platform == "win32":
            try:
                sys.stdout.reconfigure(encoding="utf-8")
                sys.stderr.reconfigure(encoding="utf-8")
            except AttributeError:
                pass # Fallback for older python versions

        parser = argparse.ArgumentParser(description="PR Sync CLI")
        parser.add_argument("--base", default="develop", help="Base branch")
        parser.add_argument("--model", default=None, help="Custom Ollama model name")
        args, _ = parser.parse_known_args()

        start_time = time.time()
        print("🚀 Starting PR Sync...")


        # Step 1: Auth check
        print("🔍 [1/4] Checking GitHub CLI authentication...")
        if not check_auth():
            print("❌ GitHub CLI is not authenticated.")
            return 2

        # Step 2: Git analysis
        base = args.base
        print(f"📦 [2/4] Analyzing repository changes (head -> {base})...")
        head = get_current_branch()
        diff = get_diff(base, head)
        
        if not diff.strip():
            if not check_no_empty_diff_action(diff.strip(), True):
                print("⚠️  No changes found, skipping PR sync.")
                return 0

        commits = get_commits(base, head)
        changed_files = get_changed_files(base, head)
        print(f"    • Found {len(commits)} commits and {len(changed_files)} changed files")

        # Step 3: LLM generation
        print("🧠 [3/4] Generating PR body content...")
        body = render_pr_body(diff, commits, base=base, head=head, changed_files=changed_files, custom_model=args.model)
        title = f"Auto PR: {head}"
        
        # Infer labels
        type_label = infer_type_label(changed_files)
        area_labels = infer_area_labels(changed_files)
        labels = [type_label] + area_labels

        # Step 4: GitHub update
        print("📤 [4/4] Syncing Pull Request on GitHub...")
        pr = find_open_pr(base, head)
        if pr:
            update_pr(pr['number'], title, body)
            add_labels(pr['number'], labels)
            print(f"    ✓ Updated PR #{pr['number']} for {head}")
        else:
            result = create_pr(title, body, base, head)
            pr_after = find_open_pr(base, head)
            if pr_after:
                add_labels(pr_after['number'], labels)
            print(f"    ✓ Created new PR for {head}")
        
        print(f"    🏷️  Applied labels: {', '.join(labels)}")
        
        total_time = time.time() - start_time
        print(f"🎉 PR sync completed successfully in {total_time:.2f} seconds!")
        return 0
    except Exception as e:
        print(f"💥 Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())



