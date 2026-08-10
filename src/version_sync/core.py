import re
from pathlib import Path
from typing import Optional
from version_sync.constants import VERSION_TOML_PATTERN, VERSION_CODE_PATTERN

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
            # Reconstruct the line preserving its style, but changing version
            # E.g. version = "0.1.0" -> version = "0.2.0"
            quote_char = "'" if "'" in line else '"'
            variable_part = line.split("=")[0].rstrip()
            lines[i] = f"{variable_part} = {quote_char}{new_version}{quote_char}"
            modified = True
            
    if modified:
        # Re-write the file with newline preserving
        filepath.write_text("\n".join(lines) + "\n", encoding="utf-8")
        
    return modified

def sync_version_across_repo(project_root: Path, target_version: str, force: bool = False) -> list[Path]:
    """Detect current version, run safety checks, and synchronize target_version across files."""
    new_version_tuple = parse_semver(target_version)
    
    # Resolve target version string (strip leading v)
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
        # If no previous version detected (e.g. initial setup), we bypass downgrade checks
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

    # 2. Search recursively in src/ for py files containing version variables
    src_dir = project_root / "src"
    if src_dir.exists():
        for pyfile in src_dir.rglob("*.py"):
            if update_file_version(pyfile, VERSION_CODE_PATTERN, clean_target):
                updated_files.append(pyfile)

    return updated_files
