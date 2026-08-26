import unittest
import tempfile
from pathlib import Path
from engine.config import *

CORRECT_CONFIG = """
# Global Settings
server_port = 8080
default_dir = "./temp/my-database"
null_string = "NULL"

# Ignored Files
ignored_prefixes = [".","__"]
ignored_infixes = []
ignored_suffixes = []
"""

CONFIG_WITH_TYPO = """
# Global Settings
server_port = 8080
default_dir = "./temp/my-database"
null_bling = "NULL"

# Ignored Files
ignored_prefixes = [".","__"]
ignored_infixes = []
ignored_suffixes = []
"""

CONFIG_MISSING_FIELD = """
# Global Settings
server_port = 8080
default_dir = "./temp/my-database"

# Ignored Files
ignored_prefixes = [".","__"]
ignored_infixes = []
ignored_suffixes = []
"""

CONFIG_WITH_INCORRECT_LIST_STRUCTURE = """
# Global Settings
server_port = 8080
default_dir = "./temp/my-database"
null_bling = "NULL"

# Ignored Files
ignored_prefixes = "."
ignored_infixes = []
ignored_suffixes = []
"""

CONFIG_WITH_JSON_NOT_TOML = """
{
    "key":"value",
    "key2":"value2"
}
"""

CONFIG_WITH_INVALID_TOML_SYNTAX = """
# Global Settings with missing value for key server_port
server_port
default_dir = "./temp/my-database"
null_bling = "NULL"

# Ignored Files
ignored_prefixes = "."
ignored_infixes = []
ignored_suffixes = []
"""

class TestConfigLoading(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def createTestFile(self, filename:str, contents:str):
        config_path = self.base_path / filename
        config_path.touch()
        with open(config_path, "w") as file:
            file.write(contents.strip())
    
    # Confirm a working example
    def test_valid_config_file(self):
        self.createTestFile("config.toml", CORRECT_CONFIG)
        config:Configuration = load_config("config.toml", self.base_path)
        self.assertIsInstance(config, Configuration)
        self.assertEqual(config.server_port, 8080)
        self.assertEqual(config.default_dir, "./temp/my-database")
        self.assertEqual(config.null_string, "NULL")
        self.assertEqual(config.ignored_prefixes, [".","__"])
        self.assertEqual(config.ignored_infixes, [])
        self.assertEqual(config.ignored_suffixes, [])

    # Confirm missing one row
    def test_config_missing_row_raises_type_error(self):
        self.createTestFile("config.toml", CONFIG_MISSING_FIELD)
        # Note: if we call load_config with parentheses, then it will error before it reaches the assertion check.
        self.assertRaises(TypeError, load_config,"config.toml", self.base_path)

    # Confirm non-list value in list field
    def test_config_with_missing_list_raises_type_error(self):
        self.createTestFile("config.toml", CONFIG_WITH_INCORRECT_LIST_STRUCTURE)
        self.assertRaises(TypeError, load_config, "config.toml", self.base_path)

    # Confirm missing file (or incorrectly named)
    def test_config_with_missing_config_file_raises_type_error(self):
        self.createTestFile("nofig.toml", CORRECT_CONFIG)
        self.assertRaises(FileNotFoundError, load_config, "config.toml", self.base_path)

    # Confirm typo in field leads to failure
    def test_typo_in_toml_raises_type_error(self):
        self.createTestFile("config.toml", CONFIG_WITH_TYPO)
        self.assertRaises(TypeError, load_config, "config.toml", self.base_path)

    # Confirm JSON cannot be decoded into TOML
    def test_json_craises_toml_decode_error(self):
        self.createTestFile("config.toml", CONFIG_WITH_JSON_NOT_TOML)
        self.assertRaises(tomllib.TOMLDecodeError, load_config, "config.toml", self.base_path)

    # Confirm invalid TOML with missing value for key-value pair fails
    def test_invalid_key_value_toml_raises_toml_decode_error(self):
        self.createTestFile("config.toml", CONFIG_WITH_INVALID_TOML_SYNTAX)
        self.assertRaises(tomllib.TOMLDecodeError, load_config, "config.toml", self.base_path)