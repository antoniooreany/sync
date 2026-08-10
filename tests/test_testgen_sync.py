import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import tempfile
import shutil
from testgen_sync.core import (
    generate_test_for_file,
    scan_and_generate_tests
)

class TestTestGenSync(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.tests_dir = self.test_dir / "tests"
        self.src_dir = self.test_dir / "src"
        self.src_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    @patch("testgen_sync.core.generate_llm_content", return_value="import unittest\nclass TestSample(unittest.TestCase):\n  pass")
    def test_generate_test_for_file(self, mock_llm):
        source_file = self.src_dir / "module.py"
        source_file.write_text("def test(): pass", encoding="utf-8")

        test_path = generate_test_for_file(source_file, self.tests_dir, "test-model")
        
        self.assertTrue(test_path.exists())
        self.assertEqual(test_path.name, "test_module.py")
        self.assertIn("class TestSample", test_path.read_text(encoding="utf-8"))

    @patch("testgen_sync.core.generate_llm_content", return_value="import unittest\nclass TestSample(unittest.TestCase):\n  pass")
    def test_scan_and_generate_tests(self, mock_llm):
        (self.src_dir / "main.py").write_text("def main(): pass", encoding="utf-8")
        (self.src_dir / "__init__.py").write_text("", encoding="utf-8")

        generated = scan_and_generate_tests(self.src_dir, self.tests_dir, "test-model")

        self.assertEqual(len(generated), 1)
        self.assertEqual(generated[0].name, "test_main.py")
