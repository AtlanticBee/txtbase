import unittest
import tempfile
from pathlib import Path
from engine.errors import CLIArgumentError
from engine.workspace import *

class TestWorkSpacePreparation(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)
        self.default_db = self.base_path / "my-database"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_no_args_creates_default_db(self):
        db_dir = prepare_workspace(
            arguments=["my_script"], 
            default_path=self.default_db
            )
        self.assertTrue(db_dir.name == self.default_db.name)

    def test_too_many_args_raises_args_error(self):
        self.assertRaises(CLIArgumentError, prepare_workspace, ["my-script", "my-db", "another-var"], self.default_db)

    def test_file_raises_workspace_error(self):
        new_file = self.base_path / "actually-a-file"
        new_file.touch()
        # Note we pass in the stringified full path or it defaults to the CWD of the __main__ caller.
        self.assertRaises(CLIArgumentError, prepare_workspace, ["my-script", str(new_file)], self.default_db)

    def test_invalid_name_raises_value_error(self):
        # We'll make the database directory anyway to demonstrate that's not the issue. (Full testing of the name validation is already achieved in test_val_path.py)
        new_dir = self.base_path / "My-Database-1"
        new_dir.mkdir()
        self.assertRaises(CLIArgumentError, prepare_workspace, ["my-script", str(new_dir)], self.default_db)