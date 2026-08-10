import os
import sys
from pathlib import Path
from testgen_sync.constants import DEFAULT_TESTS_DIR, DEFAULT_MODEL
from pr_sync.llm_engine import generate_llm_content

def is_git_repo() -> bool:
    """Check if inside a git repository."""
    return Path(".git").exists()

def generate_test_for_file(filepath: Path, tests_dir: Path, model: str, force: bool = False) -> Path:
    """Generate unit test file using Ollama local LLM for a given source code file."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read source file {filepath}: {e}")

    # Build output test filename
    test_filename = f"test_{filepath.stem}.py"
    test_path = tests_dir / test_filename

    if test_path.exists() and not force:
        raise FileExistsError(f"Test file already exists: {test_path}. Use --force to overwrite.")

    prompt = f"""You are a professional Python QA engineer. Generate a comprehensive unit test suite using unittest (standard Python library) for the following source code module.
Make sure to mock external APIs, file operations, or subprocess calls where appropriate.
Include comments and test structure, testing both success states and error states.

Source Code ({filepath.name}):
```python
{content}
```

Respond with ONLY the Python unit test code content. Do not include markdown code block wrapping around your entire response.
"""
    test_code = generate_llm_content(prompt, custom_model=model)
    if not test_code:
        raise RuntimeError("Failed to generate test code from LLM API.")

    # Write generated test
    tests_dir.mkdir(parents=True, exist_ok=True)
    
    # Simple clean up if LLM included block wrappers
    clean_code = test_code.strip()
    if clean_code.startswith("```python"):
        clean_code = clean_code[9:]
    if clean_code.endswith("```"):
        clean_code = clean_code[:-3]
        
    test_path.write_text(clean_code.strip() + "\n", encoding="utf-8")
    return test_path

def scan_and_generate_tests(src_dir: Path, tests_dir: Path, model: str, force: bool = False) -> list[Path]:
    """Scan src directory, locate untested files, and generate tests."""
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {src_dir}")

    generated = []
    for pyfile in src_dir.rglob("*.py"):
        if "__" in pyfile.name:  # Skip __init__ modules
            continue
            
        test_filename = f"test_{pyfile.name}"
        test_path = tests_dir / test_filename
        
        # Only generate if the test file doesn't exist yet, or force is set
        if not test_path.exists() or force:
            try:
                out_path = generate_test_for_file(pyfile, tests_dir, model, force=True)
                generated.append(out_path)
            except Exception as e:
                print(f"⚠️  Skipped test generation for {pyfile.name}: {e}", file=sys.stderr)
                
    return generated
