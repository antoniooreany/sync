import unittest
from pathlib import Path
import tempfile
import shutil
from feature_sync.core import get_porter_features, copy_feature_configs

class TestFeatureSync(unittest.TestCase):

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_porter_features(self):
        feats = get_porter_features()
        self.assertIn("gitflow_sync", feats)
        self.assertIn("gitlint_sync", feats)

    def test_copy_feature_configs_gitlint(self):
        copied = copy_feature_configs("gitlint_sync", self.test_dir)
        self.assertEqual(len(copied), 1)
        self.assertTrue((self.test_dir / ".gitlint").exists())
