from pathlib import Path
from engine.val_path import is_valid_tabledir
from engine.data import Table, IgnoredPaths

def is_ignored(path:Path, ignored_paths:IgnoredPaths):
    table_name = path.name
    # Using the 'any' keyword short-circuits when it reaches a single match
    has_prefix = any(table_name.startswith(x) for x in ignored_paths.prefixes)
    has_infix = any(x in table_name for x in ignored_paths.infixes)
    has_suffix = any(table_name.endswith(x) for x in ignored_paths.suffixes)

    return has_prefix or has_infix or has_suffix

def load_tables(path:Path, ignored_paths:IgnoredPaths) -> dict[str, Table]:
    """
    Iterate through database directory
    Collect list of tables
    Filter out the ones with invalid and ignored names
    Return them as a list of Table objects ready for column data
    """
    # Get list of directories 1 level down
    table_list = [x for x in path.iterdir() if is_valid_tabledir(x)]
    filtered_list = [x for x in table_list if not is_ignored(x, ignored_paths)]

    return {x.name:Table() for x in filtered_list}