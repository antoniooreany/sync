import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Union
from release_sync.constants import (
    DEFAULT_PR_LIMIT,
    LABELS_BREAKING,
    LABELS_FEATURES,
    LABELS_BUGFIXES,
    LABELS_DOCS
)

def run_git_command(args: list[str]) -> str:
    """Run a git command and return its stdout, stripping whitespace."""
    try:
        res = subprocess.run(["git"] + args, capture_output=True, text=True, encoding="utf-8", check=True)
        return res.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"Git command failed: {args}. Error: {e}")

def run_gh_command(args: list[str]) -> str:
    """Run a gh command and return its stdout, stripping whitespace."""
    try:
        res = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8", check=True)
        return res.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        raise RuntimeError(f"GitHub CLI command failed: {args}. Error: {e}")

def get_latest_tag() -> Optional[str]:
    """Retrieve the latest git tag in the repository."""
    try:
        # abbrev=0 returns the closest tag name without hash suffix
        return run_git_command(["describe", "--tags", "--abbrev=0"])
    except RuntimeError:
        return None

def verify_tag_does_not_exist(version: str) -> None:
    """Check if the version tag already exists in local git."""
    tag_name = f"v{version}"
    try:
        out = run_git_command(["tag", "-l", tag_name])
        if out == tag_name:
            raise ValueError(f"Tag {tag_name} already exists.")
    except RuntimeError:
        pass

def get_commits_between(start_ref: Optional[str], end_ref: str) -> list[str]:
    """Get all commit hashes between start_ref (exclusive) and end_ref (inclusive)."""
    if start_ref:
        args = ["log", f"{start_ref}..{end_ref}", "--format=%H"]
    else:
        args = ["log", end_ref, "--format=%H"]
    
    out = run_git_command(args)
    if not out:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]

def fetch_merged_prs(limit: int = DEFAULT_PR_LIMIT) -> list[dict]:
    """Fetch merged Pull Requests using GitHub CLI, gracefully returning empty if no remote is configured."""
    try:
        # Check if remote origin exists first to avoid gh CLI throwing an error in repos without remote
        remotes = run_git_command(["remote"])
        if not remotes:
            print("⚠️  No git remotes configured. Skipping GitHub PR fetch.")
            return []
    except Exception:
        return []

    try:
        out = run_gh_command([
            "pr", "list", 
            "--state", "merged", 
            "--limit", str(limit), 
            "--json", "number,title,body,labels,mergeCommit,author"
        ])
        if not out:
            return []
        return json.loads(out)
    except Exception as e:
        print(f"⚠️  Failed to fetch PRs via GitHub CLI (is gh auth configured?). Error: {e}")
        return []

def resolve_author(pr: dict) -> str:
    """Extract author login name from PR structure."""
    author_obj = pr.get("author")
    if isinstance(author_obj, dict):
        return author_obj.get("login", "unknown")
    return "unknown"

def compile_release_notes(prs: list[dict]) -> str:
    """Compile structured, alphabetical release notes from grouped PRs."""
    sections = {
        "Breaking Changes": [],
        "Features": [],
        "Bug Fixes": [],
        "Documentation": [],
        "Internal": []
    }

    for pr in prs:
        title = pr.get("title", "").strip()
        num = pr.get("number")
        author = resolve_author(pr)
        labels = [label.get("name", "").lower() for label in pr.get("labels", [])]

        # Categorize
        if any(lbl in LABELS_BREAKING for lbl in labels):
            sections["Breaking Changes"].append((num, title, author))
        elif any(lbl in LABELS_FEATURES for lbl in labels):
            sections["Features"].append((num, title, author))
        elif any(lbl in LABELS_BUGFIXES for lbl in labels):
            sections["Bug Fixes"].append((num, title, author))
        elif any(lbl in LABELS_DOCS for lbl in labels):
            sections["Documentation"].append((num, title, author))
        else:
            sections["Internal"].append((num, title, author))

    # Format into markdown with stable sorted output
    lines = []
    for section_name, items in sections.items():
        if not items:
            continue
        
        lines.append(f"### {section_name}")
        # Sort items by PR number to maintain deterministic output
        sorted_items = sorted(items, key=lambda x: x[0])
        for num, title, author in sorted_items:
            lines.append(f"- [#{num}] {title} (by @{author})")
        lines.append("") # empty line after section

    return "\n".join(lines).strip()

def prepend_to_changelog(changelog_path: Path, version: str, notes: str) -> None:
    """Prepend the release notes block into CHANGELOG.md."""
    date_str = datetime.now().strftime("%Y-%m-%d")
    heading = f"## v{version} — {date_str}"
    entry = f"{heading}\n\n{notes}\n"

    if not changelog_path.exists():
        # Create changelog with standard title
        changelog_path.write_text(f"# Changelog\n\n{entry}", encoding="utf-8")
        return

    content = changelog_path.read_text(encoding="utf-8")
    
    # Locate where to insert (usually after '# Changelog')
    header_marker = "# Changelog"
    if header_marker in content:
        parts = content.split(header_marker, 1)
        # Reconstruct with the new entry right after '# Changelog'
        new_content = f"{header_marker}\n\n{entry}\n{parts[1].lstrip()}"
    else:
        # Prepend to the file
        new_content = f"{entry}\n{content}"

    changelog_path.write_text(new_content, encoding="utf-8")

def get_current_branch() -> str:
    """Get the name of the current git branch."""
    return run_git_command(["branch", "--show-current"])

def commit_and_push_release(version: str, changelog_path: Path) -> None:
    """Stage modified files, commit the release, and push to origin if configured."""
    # Stage changelog
    run_git_command(["add", str(changelog_path)])

    # Stage other configuration files if they are modified
    for name in ["pyproject.toml", "package.json", "Cargo.toml"]:
        config_file = changelog_path.parent / name
        if config_file.exists():
            # Check if file has unstaged or staged changes
            status = run_git_command(["status", "--porcelain", name])
            if status:
                run_git_command(["add", name])

    # Commit release
    commit_msg = f"chore(release): release v{version}"
    run_git_command(["commit", "-m", commit_msg])

    # Push commit if origin exists
    try:
        remotes = run_git_command(["remote"])
        if "origin" in remotes.split():
            branch = get_current_branch()
            if branch:
                print(f"⬆️  Pushing release commit to branch: {branch}...")
                run_git_command(["push", "origin", branch])
        else:
            print("⚠️  No 'origin' remote configured. Skipping release push.")
    except Exception as e:
        print(f"⚠️  Failed to push release commit: {e}")

def create_git_tag(version: str) -> None:
    """Create a local git tag for the release at HEAD."""
    run_git_command(["tag", f"v{version}", "HEAD"])

def push_git_tag(version: str) -> None:
    """Push the tag to the remote origin if configured."""
    try:
        remotes = run_git_command(["remote"])
        if "origin" in remotes.split():
            run_git_command(["push", "origin", f"v{version}"])
        else:
            print("⚠️  No 'origin' remote configured. Skipping tag push.")
    except Exception as e:
        print(f"⚠️  Failed to push git tag: {e}")

def create_github_release(version: str, notes: str) -> None:
    """Create a GitHub release using gh CLI if remote is configured."""
    try:
        remotes = run_git_command(["remote"])
        if not remotes:
            print("⚠️  No remotes configured. Skipping GitHub Release creation.")
            return
        tag_name = f"v{version}"
        run_gh_command([
            "release", "create", tag_name,
            "--title", tag_name,
            "--notes", notes
        ])
    except Exception as e:
        print(f"⚠️  Failed to create GitHub release: {e}")

# Version Sync logic integrated
import re

VERSION_TOML_PATTERN = r'^version\s*=\s*["\']([^"\']+)["\']'
VERSION_CODE_PATTERN = r'^(__version__|VERSION|version)\s*=\s*["\']([^"\']+)["\']'

def parse_semver(version_str: str) -> tuple[int, int, int]:
    """Parse a semantic version string into a tuple of integers."""
    match = re.match(r"^v?(\d+)\.(\d+)\.(\d+)$", version_str.strip())
    if not match:
        raise ValueError(f"Invalid SemVer format: '{version_str}'. Expected X.Y.Z")
    return int(match.group(1)), int(match.group(2)), int(match.group(3))

def detect_current_version(project_root: Path) -> str:
    """Detect current version in pyproject.toml."""
    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        raise FileNotFoundError(f"pyproject.toml not found at {pyproject}")
        
    content = pyproject.read_text(encoding="utf-8")
    for line in content.splitlines():
        match = re.match(VERSION_TOML_PATTERN, line.strip())
        if match:
            return match.group(1)
            
    raise ValueError("Could not find project version inside pyproject.toml")

def calculate_bump(current_version: str, level: str) -> str:
    """Increment version based on level (major, minor, patch)."""
    major, minor, patch = parse_semver(current_version)
    if level == "major":
        return f"{major + 1}.0.0"
    elif level == "minor":
        return f"{major}.{minor + 1}.0"
    elif level == "patch":
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Unknown bump level '{level}'. Choose major, minor, or patch.")

def update_file_version(filepath: Path, pattern: str, new_version: str) -> bool:
    """Search and replace version declaration lines in a file."""
    if not filepath.exists():
        return False
        
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()
    modified = False
    
    for i, line in enumerate(lines):
        match = re.match(pattern, line.strip())
        if match:
            quote_char = "'" if "'" in line else '"'
            variable_part = line.split("=")[0].rstrip()
            lines[i] = f"{variable_part} = {quote_char}{new_version}{quote_char}"
            modified = True
            
    if modified:
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
        
    return modified

def sync_version_across_repo(project_root: Path, target_version: str, force: bool = False) -> list[Path]:
    """Detect current version, run safety checks, and synchronize target_version across files."""
    new_version_tuple = parse_semver(target_version)
    clean_target = f"{new_version_tuple[0]}.{new_version_tuple[1]}.{new_version_tuple[2]}"
    
    try:
        current_version = detect_current_version(project_root)
        current_version_tuple = parse_semver(current_version)
        
        # Check downgrade protection
        if new_version_tuple < current_version_tuple and not force:
            raise ValueError(
                f"Version downgrade protection triggered: target '{clean_target}' is lower than current '{current_version}'. "
                "Use --force to override."
            )
    except Exception as e:
        if "pyproject.toml not found" in str(e) or "Could not find project version" in str(e):
            pass
        else:
            raise e

    updated_files = []

    # 1. Update pyproject.toml
    pyproject = project_root / "pyproject.toml"
    if pyproject.exists():
        if update_file_version(pyproject, VERSION_TOML_PATTERN, clean_target):
            updated_files.append(pyproject)

    # 2. Search recursively in src/
    src_dir = project_root / "src"
    if src_dir.exists():
        for pyfile in src_dir.rglob("*.py"):
            if update_file_version(pyfile, VERSION_CODE_PATTERN, clean_target):
                updated_files.append(pyfile)

    return updated_files
