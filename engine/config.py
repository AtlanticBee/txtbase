import tomllib
from dataclasses import dataclass, field
from pathlib import Path

# There is a tight coupling here between the TOML and the Python
# The point is to make best use of TOML readability and Python to guarantee validity.

@dataclass
class Configuration:
    server_port:int
    default_dir:Path
    null_string:str
    ignored_prefixes:list[str] = field(default_factory=list)
    ignored_infixes:list[str] = field(default_factory=list)
    ignored_suffixes:list[str] = field(default_factory=list)

def load_config(filename:str, base_path:Path):
    config_path = base_path / filename
    # TOML Lib requires openening in RB (Read only binary) mode.
    with open(config_path, "rb") as file:
        raw_config = tomllib.load(file)
        return Configuration(**raw_config)