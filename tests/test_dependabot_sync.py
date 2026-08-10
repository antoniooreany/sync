import pytest
from pathlib import Path
from dependabot_sync.core import generate_dependabot_config, write_config

def test_generate_dependabot_config_weekly():
    config = generate_dependabot_config(interval="weekly", limit=3, assignee="antoniooreany")
    assert "version: 2" in config
    assert 'interval: "weekly"' in config
    assert "open-pull-requests-limit: 3" in config
    assert "assignees:\n      - antoniooreany" in config

def test_generate_dependabot_config_no_assignee():
    config = generate_dependabot_config(interval="monthly", limit=5, assignee=None)
    assert 'interval: "monthly"' in config
    assert "open-pull-requests-limit: 5" in config
    assert "assignees" not in config

def test_write_config_safety(tmp_path):
    config_content = "test_content"
    
    # 1. Success write first time
    written = write_config(tmp_path, config_content, force=False)
    assert written.exists()
    assert written.read_text() == config_content
    
    # 2. FileExistsError on second write
    with pytest.raises(FileExistsError):
        write_config(tmp_path, "new_content", force=False)
        
    # 3. Success overwrite with force=True
    written_force = write_config(tmp_path, "new_content", force=True)
    assert written_force.read_text() == "new_content"
