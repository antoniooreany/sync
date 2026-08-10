import sys
import argparse
from pathlib import Path
from testgen_sync.constants import (
    EXIT_CODE_SUCCESS,
    EXIT_CODE_EXPECTED_ERROR,
    EXIT_CODE_ENV_ERROR,
    DEFAULT_TESTS_DIR,
    DEFAULT_MODEL
)
from testgen_sync.core import (
    is_git_repo,
    generate_test_for_file,
    scan_and_generate_tests
)

def main():
    # Reconfigure console output encoding on Windows to support emojis
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except AttributeError:
            pass

    parser = argparse.ArgumentParser(description="TestGen Sync CLI (tg)")
    parser.add_argument("--tests-dir", default=DEFAULT_TESTS_DIR, help="Output directory for tests")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Model name for Ollama")
    parser.add_argument("--force", action="store_true", help="Overwrite existing test files")
    
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: file
    file_parser = subparsers.add_parser("file", help="Generate unit test for a single source file")
    file_parser.add_argument("path", help="Path to the python source file")

    # Subcommand: scan
    subparsers.add_parser("scan", help="Scan repository src/ and generate tests for missing coverage")

    args = parser.parse_args()

    project_root = Path.cwd()
    tests_dir = project_root / args.tests_dir

    if args.command == "file":
        filepath = Path(args.path)
        if not filepath.exists():
            print(f"❌ Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

        print(f"🧪 Generating test suite for {filepath.name}...")
        try:
            test_path = generate_test_for_file(filepath, tests_dir, args.model, force=args.force)
            print(f"🎉 Successfully generated unit test at: {test_path.relative_to(project_root)}")
            sys.exit(EXIT_CODE_SUCCESS)
        except Exception as e:
            print(f"💥 Error: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

    elif args.command == "scan":
        src_dir = project_root / "src"
        if not src_dir.exists():
            print(f"❌ Error: Source directory 'src' not found in workspace root.", file=sys.stderr)
            sys.exit(EXIT_CODE_ENV_ERROR)

        print("🔍 Scanning source files to detect missing unit tests...")
        try:
            generated = scan_and_generate_tests(src_dir, tests_dir, args.model, force=args.force)
            if not generated:
                print("ℹ️  No missing test suites detected.")
            else:
                print(f"🎉 Successfully generated {len(generated)} test suite(s):")
                for test in generated:
                    print(f"  • {test.relative_to(project_root)}")
            sys.exit(EXIT_CODE_SUCCESS)
        except Exception as e:
            print(f"💥 Error scanning repository: {e}", file=sys.stderr)
            sys.exit(EXIT_CODE_EXPECTED_ERROR)

if __name__ == "__main__":
    main()
