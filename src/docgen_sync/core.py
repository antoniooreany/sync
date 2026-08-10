import os
import sys
from pathlib import Path
from docgen_sync.constants import DEFAULT_DOCS_DIR, DEFAULT_MODEL
from pr_sync.llm_engine import generate_llm_content

def is_git_repo() -> bool:
    """Check if the current working directory is a git repository."""
    return Path(".git").exists()

def generate_documentation_for_file(filepath: Path, docs_dir: Path, model: str) -> Path:
    """Generate Markdown documentation for a specific file and save it."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        raise ValueError(f"Failed to read file {filepath}: {e}")

    prompt = f"""You are a professional technical writer. Generate a clean, detailed markdown documentation page for the following source code file.
Include:
1. Module Description (purpose and design).
2. Class and Function reference (parameters, return types, exceptions raised).
3. Practical Usage Examples.

Source Code ({filepath.name}):
```python
{content}
```

Respond with ONLY the markdown documentation content. Do not include markdown block wrapping for the entire response.
"""
    doc_content = generate_llm_content(prompt, custom_model=model)
    if not doc_content:
        raise RuntimeError("Failed to generate documentation from LLM API.")

    docs_dir.mkdir(parents=True, exist_ok=True)
    doc_filename = f"{filepath.stem}.md"
    doc_path = docs_dir / doc_filename
    doc_path.write_text(doc_content.strip() + "\n", encoding="utf-8")
    return doc_path

def update_docs_index(docs_dir: Path) -> Path:
    """Update or create docs/README.md with all generated markdown references."""
    readme_path = docs_dir / "README.md"
    new_entry = "# Code Reference Documentation\n\nAutomatically generated module guides:\n\n"
    
    # Sort files to keep stable indexing
    for gf in sorted(docs_dir.glob("*.md")):
        if gf.name != "README.md":
            new_entry += f"- [{gf.stem}]({gf.name})\n"
            
    readme_path.write_text(new_entry, encoding="utf-8")
    return readme_path

def scan_and_generate_all(src_dir: Path, docs_dir: Path, model: str) -> list[Path]:
    """Scan directory and generate documentation for all source files."""
    if not src_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {src_dir}")

    generated = []
    # Currently focuses on python files
    for pyfile in src_dir.rglob("*.py"):
        if "__" in pyfile.name:  # Skip __init__.py and internal files
            continue
        try:
            doc_path = generate_documentation_for_file(pyfile, docs_dir, model)
            generated.append(doc_path)
        except Exception as e:
            print(f"⚠️  Skipped {pyfile.name}: {e}", file=sys.stderr)
            
    if generated:
        update_docs_index(docs_dir)
        
    return generated
