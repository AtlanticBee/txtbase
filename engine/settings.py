from dataclasses import dataclass
from typing import ClassVar
import re

# Any folder or file containing one of the following strings in its name will not be inspected, even if it's a .col file or valid table name
# Two reasonable examples have been included - who knew the middle substrings were called infixes eh!?
# For immutable objects (during run time) tuples are superior and are automatically iterated in the is_ignored function.
@dataclass(frozen=True)
class IgnoredFileNames:
    prefixes: tuple[str,...] = (".", "__")
    infixes: tuple[str,...] = ()
    suffixes: tuple[str,...] = ()

    def is_ignored(self, name:str) -> bool:
        if name.startswith(self.prefixes) or name.endswith(self.suffixes):
            return True
        # This is cool - the any keyword returns true if a match is found, but otherwise is false.
        return any(infix in name for infix in self.infixes)

# System Settings - applies globally to the database being opened.

@dataclass
class GlobalSettings:
    # TODO: if server is used in the end...
    server_port: int = 8080
    default_dir: str = "./temp/my-database"
    # Do not replace this with the null string or you'll be in a world of poop (POSIX whitespace handling is variable)
    null_string: str = "NULL"
    ignored_filenames: ClassVar[IgnoredFileNames] = IgnoredFileNames()
    column_extension: str = ".col"
    table_schema_filename: str = "schema.json"
    accepted_file_chars: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9-]+$")

global_settings = GlobalSettings()

