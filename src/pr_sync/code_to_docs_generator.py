import subprocess
from pathlib import Path
from typing import Optional

from pr_sync.llm_engine import generate_llm_content


def run_git(args: list[str]) -> str:
    res = subprocess.run(
        ["git"] + args, capture_output=True, text=True, encoding="utf-8", check=True
    )
    return res.stdout.strip()


def generate_module_docs(filepath: Path, custom_model: Optional[str] = None) -> str:
    """Generate detailed markdown documentation for a source file using the LLM."""
    if not filepath.exists():
        return ""

    try:
        content = filepath.read_text(encoding="utf-8")
    except OSError:
        return ""

    lang_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".java": "Java",
        ".cpp": "C++",
        ".c": "C",
        ".h": "C",
        ".hpp": "C++",
        ".cs": "C#",
    }
    language = lang_map.get(filepath.suffix, "source code")

    prompt = f"""You are a professional technical writer. Generate a clean, detailed markdown documentation page for the following {language} file.
Include:
1. File/Module Description (purpose and design).
2. Class and Function reference (parameters, return types, exceptions raised).
3. Practical Usage Examples.

Source Code:
```{language.lower()}
{content}
```

Respond with ONLY the markdown documentation content. Do not include markdown block wrapping for the entire response.
"""
    doc_content = generate_llm_content(prompt, custom_model=custom_model)
    return doc_content.strip() if doc_content else ""


def run_code_to_docs(changed_files: list[str], custom_model: Optional[str] = None) -> list[Path]:
    """Scan changed files, generate API documentation, and stage them to git."""
    project_root = Path.cwd()
    docs_dir = project_root / "docs"
    docs_dir.mkdir(exist_ok=True)

    generated_files: list[Path] = []
    supported_extensions = {
        ".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".h", ".hpp", ".cs"
    }

    for filepath_str in changed_files:
        path = Path(filepath_str)
        if path.suffix not in supported_extensions:
            continue

        print(f"📄 Generating documentation for {filepath_str}...")
        doc_content = generate_module_docs(path, custom_model=custom_model)
        if not doc_content:
            continue

        doc_filename = f"{path.stem}.md"
        doc_path = docs_dir / doc_filename
        doc_path.write_text(doc_content + "\n", encoding="utf-8")

        try:
            run_git(["add", str(doc_path)])
            generated_files.append(doc_path)
            print(f"    ✓ Wrote and staged: docs/{doc_filename}")
        except Exception as e:
            print(f"    ⚠️  Failed to stage docs: {e}")

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
