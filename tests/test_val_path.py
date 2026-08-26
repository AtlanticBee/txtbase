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
            "valid-Column.col"
            "valid-column-234col",
            "valid-column-234.mol",
            ".col",
            "valid-filename.Col",
            "valid-filename.COL",
            "valid-filename..col",
            "valid-filename...col",
            "valid-name",
            "invalid-nàme"
        ]
        for name in invalid_names:
            file_path = self.base_path / name
            file_path.touch()
            with self.subTest(msg=f"Test if colfile name '{name}' is invalid", path=file_path):
                print(f"subtest - colfile name validation - {name}")
                self.assertFalse(is_valid_colfile(file_path))

    def test_colfile_cannot_be_directory(self):
        dir_path = self.base_path / "test"
        dir_path.mkdir(parents=False, exist_ok=False)
        self.assertFalse(is_valid_colfile(dir_path))

class TestTableDirPathValidation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    # Unit Tests

    def test_valid_table_name_returns_true(self):
        valid_directories = [
            "valid-name",
            "valid-name-123",
            "123",
            "a",
            "0",
            "-"
        ]
        for name in valid_directories:
            # Decided to make sure we're not looking at a pre-existing directory
            # Don't want parents to be created automatically either
            dir_path = self.base_path / name
            dir_path.mkdir(parents=False, exist_ok=False)
            with self.subTest(msg=f"Test if table dir name '{name}' is valid", path=dir_path):
                print(f"subtest - table dir name validation - {name}")
                self.assertTrue(is_valid_tabledir(dir_path))

    def test_invalid_table_name_returns_false(self):
        invalid_directories = [
            "Invalid-name",
            "invalid-Name-123",
            "123.",
            "A",
            "ó",
            "_"
        ]
        for name in invalid_directories:
            # Decided to make sure we're not looking at a pre-existing directory
            # Don't want parents to be created automatically either
            dir_path = self.base_path / name
            dir_path.mkdir(parents=False, exist_ok=False)
            with self.subTest(msg=f"Test if table dir name '{name}' is valid", path=dir_path):
                print(f"subtest - table dir name validation - {name}")
                self.assertFalse(is_valid_tabledir(dir_path))

    def test_table_cannot_be_file(self):
        dir_path = self.base_path / "test"
        dir_path.touch()
        self.assertFalse(is_valid_tabledir(dir_path))