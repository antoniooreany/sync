"""Spec-backed tests for docs/maturity-hygiene-specification.md."""
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[1]


def test_r1_runtime_deps_match_policy():
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "google-genai" not in text
    assert '"requests"' not in text and "'requests'" not in text
    assert "flask" in text.lower()
    assert "[project.optional-dependencies]" in text
    assert "pytest" in text
    assert "ruff" in text


def test_r2_ci_workflow_exists():
    ci = ROOT / ".github" / "workflows" / "ci.yml"
    assert ci.is_file()
    text = ci.read_text(encoding="utf-8")
    assert "pytest" in text
    assert "ruff check" in text
    assert "3.9" in text
    assert "3.12" in text


def test_r3_no_duplicate_core_tests():
    assert not (ROOT / "tests" / "test_core.py").exists()
    assert (ROOT / "tests" / "test_release_sync.py").is_file()


def test_r4_no_sbox_routes_or_template_hooks():
    from pr_sync.ui import app as ui_app

    rules = {rule.rule for rule in ui_app.app.url_map.iter_rules()}
    assert "/compress" not in rules
    assert "/download" not in rules

    template = (
        ROOT / "src" / "pr_sync" / "ui" / "templates" / "index.html"
    ).read_text(encoding="utf-8")
    assert "SboxGame" not in template
    assert "/compress" not in template
    assert "compressBtn" not in template


def test_r5_debug_false():
    main_src = (ROOT / "src" / "sync" / "__main__.py").read_text(encoding="utf-8")
    app_src = (ROOT / "src" / "pr_sync" / "ui" / "app.py").read_text(encoding="utf-8")
    assert "debug=False" in main_src
    assert "debug=False" in app_src
    assert "debug=True" not in main_src
    assert "debug=True" not in app_src


def test_r6_no_gemini_helper():
    import pr_sync.llm_engine as llm

    assert not hasattr(llm, "_get_best_gemini_model")
    src = (ROOT / "src" / "pr_sync" / "llm_engine.py").read_text(encoding="utf-8")
    assert "gemini" not in src.lower()


def test_r7_generate_module_docs_uses_llm(tmp_path):
    from pr_sync.code_to_docs_generator import generate_module_docs

    sample = tmp_path / "sample.py"
    sample.write_text("def hello():\n    return 1\n", encoding="utf-8")

    with patch(
        "pr_sync.code_to_docs_generator.generate_llm_content",
        return_value="  # Docs\n",
    ) as mock_llm:
        out = generate_module_docs(sample)
    mock_llm.assert_called_once()
    assert out == "# Docs"

    missing = tmp_path / "missing.py"
    assert generate_module_docs(missing) == ""


def test_r9_docs_and_license():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for token in ("gf", "fs", "vs", "doc", "sync", "pip install", "Ollama", "gh"):
        assert token in readme

    assert (ROOT / "docs" / "architecture.md").is_file()
    assert (ROOT / "LICENSE").is_file()
    assert "MIT" in (ROOT / "LICENSE").read_text(encoding="utf-8")

    docs_readme = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    assert "draft" in docs_readme.lower() or "AI-generated" in docs_readme


def test_spec_document_exists():
    assert (ROOT / "docs" / "maturity-hygiene-specification.md").is_file()
