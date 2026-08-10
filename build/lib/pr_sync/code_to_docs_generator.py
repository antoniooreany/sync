import os
import sys
import subprocess
from pathlib import Path
from pr_sync.llm_engine import generate_smart_pr_summary

def run_git(args: list[str]) -> str:
    res = subprocess.run(["git"] + args, capture_output=True, text=True, encoding="utf-8", check=True)
    return res.stdout.strip()

def generate_module_docs(filepath: Path, custom_model: str = None) -> str:
    """Generate detailed markdown documentation for a python module using the LLM."""
    if not filepath.exists():
        return ""

    file_content = filepath.read_text(encoding="utf-8")
    
    # We will reuse the LLM engine but with a custom prompt.
    # Since generate_smart_pr_summary accepts prompts implicitly via its structure,
    # let's construct a prompt to feed to LLM engine.
    # Wait, generate_smart_pr_summary handles prompt logic internally. Let's make a generic helper in llm_engine
    # or write a specific helper.
    # Let's check llm_engine.py: it supports OLLAMA, Anthropic, and Gemini.
    # We can add a function generate_llm_content(prompt: str, custom_model: str = None) -> str
    # in llm_engine.py, and call it here.
    pass

def run_code_to_docs(changed_files: list[str], custom_model: str = None) -> list[Path]:
    """Scan changed files, generate API documentation, and stage them to git."""
    from pr_sync.llm_engine import generate_llm_content

    project_root = Path.cwd()
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    generated_files = []

    # Process python source files in src/
    for filepath_str in changed_files:
        path = Path(filepath_str)
        if path.suffix == ".py" and filepath_str.startswith("src/"):
            print(f"📄 Generating documentation for {filepath_str}...")
            
            try:
                content = path.read_text(encoding="utf-8")
            except Exception:
                continue

            prompt = f"""You are a professional technical writer. Generate a clean, detailed markdown documentation page for the following Python module.
Include:
1. Module Description (purpose and design).
2. Class and Function reference (parameters, return types, exceptions raised).
3. Practical Usage Examples.

Module Source Code:
```python
{content}
```

Respond with ONLY the markdown documentation content. Do not include markdown block wrapping for the entire response.
"""
            doc_content = generate_llm_content(prompt, custom_model=custom_model)
            if doc_content:
                # Save as docs/module_name.md
                doc_filename = f"{path.stem}.md"
                doc_path = docs_dir / doc_filename
                doc_path.write_text(doc_content.strip() + "\n", encoding="utf-8")
                
                # Stage to git
                try:
                    run_git(["add", str(doc_path)])
                    generated_files.append(doc_path)
                    print(f"    ✓ Wrote and staged: docs/{doc_filename}")
                except Exception as e:
                    print(f"    ⚠️  Failed to stage docs: {e}")

    # Generate or update docs index docs/README.md
    if generated_files:
        readme_path = docs_dir / "README.md"
        new_entry = "# Code Reference Documentation\n\nAutomatically generated module guides:\n\n"
        for gf in docs_dir.glob("*.md"):
            if gf.name != "README.md":
                new_entry += f"- [{gf.stem}]({gf.name})\n"
        
        try:
            readme_path.write_text(new_entry, encoding="utf-8")
            run_git(["add", str(readme_path)])
            generated_files.append(readme_path)
        except Exception as e:
            print(f"    ⚠️  Failed to write docs README: {e}")

    return generated_files
