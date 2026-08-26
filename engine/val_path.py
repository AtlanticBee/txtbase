import re
from pathlib import Path

"""
Key txtbase rule:
File and folder names must consist of one or more:
- alphanumerical characters but not upper case (prevents issues with OS variations)
- hyphens
No underscores or other characters are permitted.
This ensures stylistic consistency and avoids issues if a server implementation is made later on (URLs have more strict formatting).
"""
ACCEPTED_NAMES: re.Pattern[str] = re.compile(r"^[a-z0-9-]+$")

"""
In our case, since the pattern explicitly states the pattern must start at the beginning (^), and include the final character ($) it will behave like the full,match method below even if we just used name.search(). It's just a bit more explicit. Since it return a match object, we need to convert to boolean first.
"""
def is_valid_pathname(name:str, pattern:re.Pattern[str]):
    return bool(pattern.fullmatch(name))

def is_valid_colfile(path:Path):
    return path.is_file() and is_valid_pathname(path.stem, ACCEPTED_NAMES) and path.suffix == ".col"

def is_valid_tabledir(path:Path):
    return path.is_dir() and is_valid_pathname(path.name, ACCEPTED_NAMES)