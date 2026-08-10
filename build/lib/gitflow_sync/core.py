import subprocess
import re
from pathlib import Path
from gitflow_sync.constants import VALID_PREFIXES, REQUIRED_BASE_BRANCHES

def run_git(args: list[str]) -> str:
    """Run a git command and return its stdout. Raises exception if failed."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True
    )
    return result.stdout.strip()

def is_git_repo() -> bool:
    """Check if inside a valid git repository."""
    try:
        run_git(["rev-parse", "--is-inside-work-tree"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_current_branch() -> str:
    """Return the name of the current active branch."""
    return run_git(["rev-parse", "--abbrev-ref", "HEAD"])

def list_local_branches() -> list[str]:
    """Get all local branch names."""
    out = run_git(["branch", "--format=%(refname:short)"])
    return [line.strip() for line in out.splitlines() if line.strip()]

def get_base_branches(branches: list[str]) -> dict[str, str]:
    """Return map of standard base branches (main/master, develop)."""
    result = {}
    for b in branches:
        if b in ["main", "master"]:
            result["production"] = b
        elif b == "develop":
            result["development"] = b
    return result

def validate_branch_name(name: str) -> bool:
    """Check if branch name adheres to Gitflow standards."""
    if name in REQUIRED_BASE_BRANCHES:
        return True
    return any(name.startswith(pref) for pref in VALID_PREFIXES)

def check_gitflow_compliance() -> dict:
    """Assess current repository compliance with Gitflow."""
    if not is_git_repo():
        raise FileNotFoundError("Not a git repository.")

    branches = list_local_branches()
    base_map = get_base_branches(branches)
    
    warnings = []
    non_compliant = []
    
    # Check base branches
    if "production" not in base_map:
        warnings.append("Production branch ('main' or 'master') is missing locally.")
    if "development" not in base_map:
        warnings.append("Development branch ('develop') is missing locally.")
        
    # Check individual branches
    for b in branches:
        if not validate_branch_name(b):
            non_compliant.append(b)
            
    return {
        "current_branch": get_current_branch(),
        "production_branch": base_map.get("production"),
        "development_branch": base_map.get("development"),
        "warnings": warnings,
        "non_compliant_branches": non_compliant,
        "is_compliant": len(warnings) == 0 and len(non_compliant) == 0
    }

def start_branch(branch_type: str, name: str) -> str:
    """Start a new branch of given type from correct base branch."""
    if not is_git_repo():
        raise FileNotFoundError("Not a git repository.")

    # Validate type
    normalized_type = branch_type.rstrip("/") + "/"
    if normalized_type not in VALID_PREFIXES:
        valid_types = [p.rstrip("/") for p in VALID_PREFIXES]
        raise ValueError(f"Invalid branch type '{branch_type}'. Must be one of: {', '.join(valid_types)}")

    # Clean name
    clean_name = re.sub(r"[^\w\-\/]", "-", name).strip("-")
    full_name = f"{normalized_type}{clean_name}"
    
    # Determine base branch
    branches = list_local_branches()
    base_map = get_base_branches(branches)
    
    # Defaults
    dev_branch = base_map.get("development", "develop")
    prod_branch = base_map.get("production", "main")
    
    base_branch = dev_branch
    if normalized_type in ["hotfix/", "support/"]:
        base_branch = prod_branch
        
    # Check if base exists, if not fallback/error
    if base_branch not in branches:
        raise ValueError(f"Base branch '{base_branch}' does not exist locally. Please create it or fetch it first.")

    # Checkout base and update (optional, but let's just branch off local state)
    run_git(["checkout", base_branch])
    run_git(["checkout", "-b", full_name])
    return full_name

def finish_current_branch(dry_run: bool = False, force: bool = False) -> None:
    """Finish the current Gitflow branch with version and release synchronization."""
    if not is_git_repo():
        raise FileNotFoundError("Not a git repository.")

    current = get_current_branch()
    if current in REQUIRED_BASE_BRANCHES:
        raise ValueError(f"Cannot finish base branch '{current}'.")

    # Resolve branch type
    branch_type = None
    branch_name = None
    for pref in VALID_PREFIXES:
        if current.startswith(pref):
            branch_type = pref.rstrip("/")
            branch_name = current[len(pref):]
            break

    if not branch_type:
        raise ValueError(f"Branch '{current}' does not follow Gitflow naming conventions.")

    branches = list_local_branches()
    base_map = get_base_branches(branches)
    dev_branch = base_map.get("development", "develop")
    prod_branch = base_map.get("production", "main")

    print(f"🏁 Finishing {branch_type} branch: {current}")

    if branch_type in ["feature", "fix", "bugfix"]:
        # Merge into development
        if dry_run:
            print(f"🔍 [DRY RUN] Would checkout {dev_branch} and merge {current}")
            return
        run_git(["checkout", dev_branch])
        run_git(["merge", "--no-ff", current, "-m", f"Merge {current} into {dev_branch}"])
        print(f"✓ Merged {current} into {dev_branch}")
        
        # Clean up branch locally
        run_git(["branch", "-d", current])
        print(f"🗑️  Deleted branch: {current}")

    elif branch_type in ["release", "hotfix"]:
        # Releases and hotfixes trigger version bumps & release sync (changelog, tag, main & develop merge)
        project_root = Path.cwd()
        
        # Branch name should be a version like '1.2.0' or 'v1.2.0'
        # Let's clean it up to get clean semver
        version_tag = branch_name.lstrip("v")
        
        if dry_run:
            print(f"🔍 [DRY RUN] Would synchronize version to {version_tag}")
            print(f"🔍 [DRY RUN] Would merge {current} into {prod_branch} (production)")
            print(f"🔍 [DRY RUN] Would merge {current} into {dev_branch} (development)")
            print(f"🔍 [DRY RUN] Would create git tag: v{version_tag}")
            return

        # 1. Sync versions across the repository
        from release_sync.core import sync_version_across_repo
        print(f"📈 Synchronizing version to {version_tag}...")
        sync_version_across_repo(project_root, version_tag, force=force)

        # 2. Commit version updates if there are any
        status = run_git(["status", "--porcelain"])
        if status:
            run_git(["add", "."])
            run_git(["commit", "-m", f"chore(release): bump version to {version_tag}"])

        # 3. Merge into production (main)
        run_git(["checkout", prod_branch])
        run_git(["merge", "--no-ff", current, "-m", f"Merge {current} into {prod_branch}"])
        print(f"✓ Merged {current} into {prod_branch}")

        # 4. Tag the production merge
        tag_name = f"v{version_tag}"
        run_git(["tag", "-a", tag_name, "-m", f"Release {tag_name}"])
        print(f"🏷️  Created tag: {tag_name}")

        # 5. Merge into development (develop)
        run_git(["checkout", dev_branch])
        run_git(["merge", "--no-ff", current, "-m", f"Merge {current} into {dev_branch}"])
        print(f"✓ Merged {current} into {dev_branch}")

        # 6. Delete release/hotfix branch
        run_git(["branch", "-d", current])
        print(f"🗑️  Deleted branch: {current}")
        print(f"🎉 Successfully finished release v{version_tag}!")

