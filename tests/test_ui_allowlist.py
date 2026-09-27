"""Smoke tests for UI /run allowlist."""
import pytest

from pr_sync.ui.app import app, SCRIPT_MAP


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_run_rejects_unknown_script(client):
    res = client.post("/run", json={"script": "rm", "args": ["-rf", "/"]})
    assert res.status_code == 400
    data = res.get_json()
    assert data["returncode"] == 1
    assert "Invalid" in data["stderr"]


def test_run_rejects_non_list_args(client):
    res = client.post("/run", json={"script": "vs", "args": "detect"})
    assert res.status_code == 400


def test_script_map_is_explicit_allowlist():
    expected = {"pr", "rl", "dp", "glnt", "cm", "gf", "fs", "vs", "doc", "sync"}
    assert set(SCRIPT_MAP.keys()) == expected
