import os
import json
import pytest
from pr_sync.config import expand_env, load_json_config, ConfigError

def test_expand_env_with_valid_var(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "hello_world")
    result = expand_env({"key": "value-${TEST_VAR}"})
    assert result == {"key": "value-hello_world"}

def test_expand_env_with_missing_var():
    with pytest.raises(ConfigError, match="Environment variable 'MISSING_VAR' is not set"):
        expand_env({"key": "${MISSING_VAR}"})

def test_expand_env_nested(monkeypatch):
    monkeypatch.setenv("VAR1", "v1")
    monkeypatch.setenv("VAR2", "v2")
    data = {
        "list": ["item1", "${VAR1}"],
        "dict": {"nested": "${VAR2}"}
    }
    result = expand_env(data)
    assert result["list"][1] == "v1"
    assert result["dict"]["nested"] == "v2"

def test_load_json_config(tmp_path, monkeypatch):
    monkeypatch.setenv("API_KEY", "secret123")
    config_file = tmp_path / "config.json"
    
    # Write a test config
    config_data = {"api_key": "${API_KEY}", "timeout": 30}
    config_file.write_text(json.dumps(config_data), encoding="utf-8")
    
    # Load and verify
    loaded = load_json_config(config_file)
    assert loaded["api_key"] == "secret123"
    assert loaded["timeout"] == 30
