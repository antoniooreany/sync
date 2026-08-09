import sys
import argparse
import subprocess
from pathlib import Path
from pr_sync.llm_engine import generate_llm_content

def run_git(args: list[str]) -> str:
    res = subprocess.run(["git"] + args, capture_output=True, text=True, encoding="utf-8", check=True)
    return res.stdout.strip()

def get_staged_diff() -> str:
    """Retrieve the diff of currently staged changes."""
    return run_git(["diff", "--cached"])

def has_staged_changes() -> bool:
    """Check if there are any staged changes."""
    try:
        subprocess.run(["git", "diff", "--cached", "--quiet"], check=True)
        return False
    except subprocess.CalledProcessError:
        return True

def generate_suggestion(msg: str) -> str:
    """Rule-based cleanup to generate a Conventional Commit suggestion."""
    CONVENTIONAL_TYPES = ("feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci", "build", "revert")

    # Return as-is if already a valid conventional commit
    for ctype in CONVENTIONAL_TYPES:
        if msg.lower().startswith(f"{ctype}:") or msg.lower().startswith(f"{ctype}("):
            return msg

    msg_lower = msg.lower()
    clean_msg = msg

    # Clean up typical leading verbs
    for word in ["added", "add", "created", "create", "fixed", "fix", "updated", "update",
                 "cleaned", "clean", "refactored", "refactor", "tested", "test"]:
        if msg_lower.startswith(word + " ") or msg_lower == word:
            clean_msg = msg[len(word):].strip().strip(":")
            break

    if any(w in msg_lower for w in ["fix", "bug", "resolve", "error", "crash"]):
        return f"fix: {clean_msg.lower()}"
    elif any(w in msg_lower for w in ["test", "mock", "spec", "coverage"]):
        return f"test: {clean_msg.lower()}"
    elif any(w in msg_lower for w in ["doc", "readme", "guide", "markdown"]):
        return f"docs: {clean_msg.lower()}"
    elif any(w in msg_lower for w in ["refactor", "cleanup", "clean"]):
        return f"refactor: {clean_msg.lower()}"
    elif any(w in msg_lower for w in ["chore", "bump", "build", "update"]):
        return f"chore: {clean_msg.lower()}"
    else:
        return f"feat: {clean_msg.lower()}"

def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="Conventional Commit Helper (cm)")
    parser.add_argument("message", nargs="?", help="Raw commit message to format and commit")
    args = parser.parse_args()

    # Verify we are inside git root
    try:
        run_git(["rev-parse", "--is-inside-work-tree"])
    except Exception:
        print("❌ Error: Not inside a valid Git repository.", file=sys.stderr)
        sys.exit(1)

    target_message = ""

    if args.message:
        # Step A: Format provided message
        target_message = generate_suggestion(args.message)
        print(f"✨ Formatted commit message: \"{target_message}\"")
    else:
        # Step B: Auto-generate from staged diff using LLM
        if not has_staged_changes():
            print("❌ Error: No staged changes. Use 'git add' to stage files first.", file=sys.stderr)
            sys.exit(1)

        print("🤖 Analyzing staged changes with AI...")
        diff = get_staged_diff()
        
        prompt = f"""You are a helper that generates Conventional Commit messages.
Analyze the following staged Git changes (diff) and generate a single line commit message.
It must follow the Conventional Commits format exactly:
<type>(<scope>): <subject>

Where:
- type is one of: feat, fix, docs, refactor, test, chore
- scope is optional and lowercase (e.g. ui, core, dp, glnt)
- subject is lowercase, concise, describes what changed, no trailing period.

Staged Diff:
```diff
{diff}
```

Respond with ONLY the final commit message line (no explanation, no markdown block).
"""
        try:
            ai_msg = generate_llm_content(prompt).strip()
            # Basic validation
            if "\n" in ai_msg:
                ai_msg = ai_msg.split("\n")[0]
            target_message = ai_msg
            print(f"🤖 AI Suggested Message: \"{target_message}\"")
        except Exception as e:
            print(f"💥 Failed to generate message using AI: {e}", file=sys.stderr)
            sys.exit(1)

    # Ask for confirmation before committing
    try:
        ans = input("❓ Confirm and commit? [Y/n]: ").strip().lower()
        if ans in ["", "y", "yes"]:
            # Perform commit
            subprocess.run(["git", "commit", "-m", target_message], check=True)
            print("🎉 Successfully committed!")
            sys.exit(0)
        else:
            print("Aborted.")
            sys.exit(0)
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(1)

if __name__ == "__main__":
    main()
