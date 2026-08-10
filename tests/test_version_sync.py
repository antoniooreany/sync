import pytest
from pathlib import Path
from version_sync.core import parse_semver, calculate_bump, sync_version_across_repo

def test_parse_semver():
    assert parse_semver("1.2.3") == (1, 2, 3)
    assert parse_semver("v0.10.15") == (0, 10, 15)
    with pytest.raises(ValueError):
        parse_semver("1.2")
    with pytest.raises(ValueError):
        parse_semver("abc")

def test_calculate_bump():
    assert calculate_bump("1.2.3", "major") == "2.0.0"
    assert calculate_bump("1.2.3", "minor") == "1.3.0"
    assert calculate_bump("1.2.3", "patch") == "1.2.4"

def test_sync_version_across_repo(tmp_path):
    # Setup mock files
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("[project]\nversion = \"1.0.0\"\n", encoding="utf-8")
    
    src_dir = tmp_path / "src" / "package"
    src_dir.mkdir(parents=True)
    init_file = src_dir / "__init__.py"
    init_file.write_text("__version__ = '1.0.0'\n", encoding="utf-8")

    # 1. Success sync
    modified = sync_version_across_repo(tmp_path, "1.1.0", force=False)
    assert len(modified) == 2
    assert "version = \"1.1.0\"" in pyproject.read_text(encoding="utf-8")
    assert "__version__ = '1.1.0'" in init_file.read_text(encoding="utf-8")

    # 2. Prevent downgrade
    with pytest.raises(ValueError):
        sync_version_across_repo(tmp_path, "1.0.0", force=False)

    # 3. Allow downgrade with force=True
    modified_downgrade = sync_version_across_repo(tmp_path, "1.0.0", force=True)
    assert len(modified_downgrade) == 2
