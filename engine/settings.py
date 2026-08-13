from dataclasses import dataclass

# System Settings - applies globally to the database being opened.

@dataclass
class GlobalSettings:
    # TODO: if server is used in the end...
    server_port: int = 8080
    default_dir: str = "./temp/my-database"
    # Do not replace this with the null string or you'll be in a world of poop (POSIX whitespace handling is variable)
    null_string: str = "NULL"
    # Any folder or file containing one of the following strings in its name will not be inspected, even if it's a .col file or valid table name
    # Two reasonable examples have been included - who knew the middle substrings were called infixes eh!?
    ignored_path_prefixes: list[str] = [".", "__"]
    ignored_path_infixes: list[str] = []
    ignored_path_suffixes: list[str] = []

global_settings = GlobalSettings()

