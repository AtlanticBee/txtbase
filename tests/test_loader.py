import unittest
import tempfile
from pathlib import Path
from engine.loader import *
from engine.data import Table

class TestTableLoader(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_db = Path(self.temp_dir.name) / "test-db"
        self.test_db.mkdir()
        self.ignored: IgnoredPaths = IgnoredPaths(
            ["pre", "good"],
            ["in", "a"],
            ["end", "hi", "suff"]
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_set_prefixes_are_ignored(self):
        ignored_pre = [
            "prefix",
            "goodbye",
        ]
        ignored_inf = [
            "actinium-00",
            "a",
            "lal",
            "loooooaooool"
        ]
        ignored_suff = [
            "bridgend",
            "ochi"
        ]
        accepted_names = [
            "byegood",
            "fixpre",
            "tiendti",
            "hight"
        ]

        for i in ignored_pre:
            path = self.test_db / i
            path.mkdir()
            with self.subTest(msg="prefix test for invalid names", desc=path):
                self.assertTrue(is_ignored(path, self.ignored))

        for i in ignored_inf:
            path = self.test_db / i
            path.mkdir()
            with self.subTest(msg="infix test for invalid names", desc=path):
                self.assertTrue(is_ignored(path, self.ignored))     

        for i in ignored_suff:
            path = self.test_db / i
            path.mkdir()
            with self.subTest(msg="suffix test for invalid names", desc=path):
                self.assertTrue(is_ignored(path, self.ignored))

        for i in accepted_names:
            path = self.test_db / i
            path.mkdir()
            with self.subTest(msg="prefix test for valid names", desc=path):
                self.assertFalse(is_ignored(path, self.ignored))

    def test_load_tables_returns_table_dict(self):
        valid_tables = [
            "crs",
            "houses",
            "colours",
            "colours-256"
        ]
        # Note Path.mkdir appears to forbid names that differ only in case here - hence I couldn't test "Colour" and "colour".
        invalid_tables = [
            "Cars-1",
            "Houses-2",
            "coloúrs",
            "colours_256"
        ]
        ignored_tables = [
            "pre-cars",
            "houses-inf-casas",
            "colurs-suff"
        ]
        invalid_files = [
            "my-file-123",
            "my-file-456"
        ]
        test_ignored = IgnoredPaths()
        for i in valid_tables:
            new_dir = self.test_db / i
            new_dir.mkdir()
        for i in invalid_tables:
            new_dir = self.test_db / i
            new_dir.mkdir()
        for i in ignored_tables:
            new_dir = self.test_db / i
            new_dir.mkdir()
        for i in invalid_files:
            new_file = self.test_db / i
            new_file.touch()
        result = load_tables(self.test_db, self.ignored)
        self.assertDictEqual(result, {
            "crs":Table(),
            "houses":Table(),
            "colours":Table(),
            "colours-256":Table()
        })

    def test_only_invalid_dirs_returns_empty_dict(self):
        invalid_tables = [
            "Cars-1",
            "Houses-2",
            "coloúrs",
            "colours_256"
        ]
        ignored_tables = [
            "pre-cars",
            "houses-inf-casas",
            "colurs-suff"
        ]
        invalid_files = [
            "my-file-123",
            "my-file-456"
        ]
        for i in invalid_tables:
            new_dir = self.test_db / i
            new_dir.mkdir()
        for i in ignored_tables:
            new_dir = self.test_db / i
            new_dir.mkdir()
        for i in invalid_files:
            new_file = self.test_db / i
            new_file.touch()
        result = load_tables(self.test_db, IgnoredPaths(["pre"],["inf"],["suff"]))
        self.assertDictEqual(result, {})

    def test_no_dirs_returns_empty_dict(self):
        result = load_tables(self.test_db, IgnoredPaths(["pre"],["inf"],["suff"]))
        self.assertDictEqual(result, {})