import pytest
from pathlib import Path
from gitlint_sync.core import generate_gitlint_config, generate_commit_msg_hook, generate_workflow_config, write_configs

def test_config_generators():
    config = generate_gitlint_config()
    assert "[title-max-length]" in config
    assert "line-length=72" in config
    assert "[title-match-regex]" in config

    hook = generate_commit_msg_hook()
    assert "gitlint" in hook
    assert "--msg-filename" in hook

    wf = generate_workflow_config()
    assert "name: commit-lint" in wf
    assert "pip install gitlint" in wf

def test_write_configs(tmp_path):
    # Setup mock git repository structure (.git folder)
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    
    # 1. Success write first time
    written = write_configs(tmp_path, force=False)
    assert len(written) == 3
    assert (tmp_path / ".gitlint").exists()
    assert (git_dir / "hooks" / "commit-msg").exists()
    assert (tmp_path / ".github" / "workflows" / "commit-lint.yml").exists()

    # 2. FileExistsError on second write without force
    with pytest.raises(FileExistsError):
        write_configs(tmp_path, force=False)

    # 3. Success overwrite with force
    write_configs(tmp_path, force=True)
