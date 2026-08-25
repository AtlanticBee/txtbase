import unittest
import tempfile
from pathlib import Path
from engine.val_path import *

# Here's a cool feature... Tempfile! :D

class TestColFilePathValidation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # Unit Tests

    def test_valid_colfile_returns_true(self):
        valid_names = [
            "valid-column-234.col",
            "valid-.col",
            "v.col",
            "1.col",
            "-.col",
            "a34-a1.col"
            ]
        for name in valid_names:
            file_path = self.base_path / name
            file_path.touch()
            with self.subTest(msg=f"Test if colfile name '{name}' is valid", path=file_path):
                print(f"subtest - colfile name validation - {name}")
                self.assertTrue(is_valid_colfile(file_path))

    def test_invalid_colfile_returns_false(self):
        invalid_names = [
            "valid-column-234col",
            "valid-column-234.mol",
            ".col",
            "valid-filename.Col",
            "valid-filename.COL",
            "valid-filename..col",
            "valid-filename...col",
            "valid-name"
        ]
        for name in invalid_names:
            file_path = self.base_path / name
            file_path.touch()
            with self.subTest(msg=f"Test if colfile name '{name}' is invalid", path=file_path):
                print(f"subtest - colfile name validation - {name}")
                self.assertFalse(is_valid_colfile(file_path))

    # Make sure valid name failes if it's a directory

    # Create new set of tests for TestTableDirPathValidation