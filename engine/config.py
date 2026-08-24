import tomllib
import sys
from dataclasses import dataclass, field
from pathlib import Path

# There is a tight coupling here between the TOML and the Python
# The point is to make best use of TOML readability and Python to guarantee validity.

CURRENT_FILE = Path(__file__).resolve()
CONFIG_DIR = CURRENT_FILE.parent

@dataclass
class Configuration:
    server_port:int
    default_dir:Path
    null_string:str
    ignored_prefixes:list[str] = field(default_factory=list)
    ignored_infixes:list[str] = field(default_factory=list)
    ignored_suffixes:list[str] = field(default_factory=list)

def load_config():
    config_path = CONFIG_DIR / "config.toml"
    # TOML Lib requires openening in RB (Read only binary) mode.
    with open(config_path, "rb") as file:
        try:
            raw_config = tomllib.load(file)
            return Configuration(**raw_config)
        except tomllib.TOMLDecodeError as e:
            print(f"Failed to parse TOML configuration file. Aborting... {e}")
            sys.exit(1)
        except FileNotFoundError as e:
            print(f"Database configuration file not found. There should be a 'config.toml' file in the root of the Python application. Aborting... {e}")
            sys.exit(1)