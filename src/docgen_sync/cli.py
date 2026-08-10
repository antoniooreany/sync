import sys
import argparse
from pathlib import Path
from docgen_sync.constants import (
    EXIT_CODE_SUCCESS,
    EXIT_CODE_EXPECTED_ERROR,
    EXIT_CODE_ENV_ERROR,
    DEFAULT_DOCS_DIR,
    DEFAULT_MODEL
)
from docgen_sync.core import (
    is_git_repo,
    generate_documentation_for_file,
    update_docs_index,
    scan_and_generate_all
)

def main():
    # Reconfigure console output encoding on Windows to support emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="DocGen Sync CLI (dg)")
    parser.add_argument("--docs-dir", default=DEFAULT_DOCS_DIR, help="Output directory for documentation")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name for Ollama")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: file
    file_parser = subparsers.add_parser("file", help="Generate documentation for a single file")
    file_parser.add_argument("path", help="Path to the source code file")

    # Subcommand: scan
    subparsers.add_parser("scan", help="Scan repository src directory and generate docs for all files")

    args = parser.parse_args()

    project_root = Path.cwd()
    docs_dir = project_root / args.docs_dir

    if args.command == "file":
        filepath = Path(args.path)
        if not filepath.exists():
            print(f"❌ Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

        print(f"📄 Generating documentation for {filepath.name}...")
        try:
            doc_path = generate_documentation_for_file(filepath, docs_dir, args.model)
            update_docs_index(docs_dir)
            print(f"🎉 Successfully generated docs at: {doc_path.relative_to(project_root)}")
            sys.exit(EXIT_CODE_SUCCESS)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

    elif args.command == "scan":
        src_dir = project_root / "src"
        if not src_dir.exists():
            print(f"❌ Error: Source directory 'src' not found in workspace root.", file=sys.stderr)
            sys.exit(EXIT_CODE_ENV_ERROR)

        print("🔍 Scanning source files for documentation...")
        try:
            generated = scan_and_generate_all(src_dir, docs_dir, args.model)
            if not generated:
                print("ℹ️  No files found to generate documentation.")
            else:
                print(f"🎉 Successfully generated {len(generated)} document(s):")
                for doc in generated:
                    print(f"  • {doc.relative_to(project_root)}")
            sys.exit(EXIT_CODE_SUCCESS)
        except Exception as e:
            print(f"💥 Error scanning repository: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

if __name__ == "__main__":
    main()
