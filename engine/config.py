import tomllib
from dataclasses import dataclass, field
from engine.data import IgnoredPaths
from pathlib import Path

# There is a tight coupling here between the TOML and the Python
# The point is to make best use of TOML readability and Python to guarantee validity.

@dataclass
class Configuration:
    server_port:int
    default_dir:Path
    null_string:str
    ignored_paths:IgnoredPaths

    # What to do with the variables after initialisation - required to coerce into relevant classes
    def __post_init__(self):
        if isinstance(self.default_dir, str):
            self.default_dir = Path(self.default_dir)

        if isinstance(self.ignored_paths, IgnoredPaths):
            self.ignored_paths = IgnoredPaths(**self.ignored_paths)

def load_config(filename:str, base_path:Path):
    config_path = base_path / filename
    # TOML Lib requires openening in RB (Read only binary) mode.
    with open(config_path, "rb") as file:
        raw_config = tomllib.load(file)
        return Configuration(**raw_config)