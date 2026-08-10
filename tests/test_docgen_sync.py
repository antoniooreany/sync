import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil
from docgen_sync.core import (
    generate_documentation_for_file,
    update_docs_index,
    scan_and_generate_all
)

class TestDocGenSync(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.docs_dir = self.test_dir / "docs"
        self.src_dir = self.test_dir / "src"
        self.src_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("docgen_sync.core.generate_llm_content", return_value="## Mocked Doc Content")
    def test_generate_documentation_for_file(self, mock_llm):
        source_file = self.src_dir / "module.py"
        source_file.write_text("def test(): pass", encoding="utf-8")

        doc_path = generate_documentation_for_file(source_file, self.docs_dir, "test-model")
        
        self.assertTrue(doc_path.exists())
        self.assertEqual(doc_path.name, "module.md")
        self.assertIn("Mocked Doc Content", doc_path.read_text(encoding="utf-8"))

    def test_update_docs_index(self):
        self.docs_dir.mkdir(exist_ok=True)
        (self.docs_dir / "module1.md").write_text("content", encoding="utf-8")
        (self.docs_dir / "module2.md").write_text("content", encoding="utf-8")

        readme_path = update_docs_index(self.docs_dir)

        self.assertTrue(readme_path.exists())
        content = readme_path.read_text(encoding="utf-8")
        self.assertIn("[module1](module1.md)", content)
        self.assertIn("[module2](module2.md)", content)

    @patch("docgen_sync.core.generate_llm_content", return_value="## Mocked Doc Content")
    def test_scan_and_generate_all(self, mock_llm):
        (self.src_dir / "main.py").write_text("def main(): pass", encoding="utf-8")
        (self.src_dir / "__init__.py").write_text("", encoding="utf-8")

        generated = scan_and_generate_all(self.src_dir, self.docs_dir, "test-model")

        self.assertEqual(len(generated), 1)
        self.assertEqual(generated[0].name, "main.md")
        self.assertTrue((self.docs_dir / "README.md").exists())
