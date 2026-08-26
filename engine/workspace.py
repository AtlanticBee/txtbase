from engine.val_path import is_valid_pathname
from pathlib import Path
from engine.errors import ArgumentError, WorkspaceError

incorrect_num_args_text = """
*** Error: too many arguments supplied. Aborting... ***

Maximum number of arguments: 2 (program name + path to database)
Arguments supplied: XXX

To run txtbase use either:
\t1. txtbase
\t2. txtbase [PATH/TO/DATABASE]

If no path is supplied, the program will open the default DB directory, creating any relevant folders as required.
If a path is supplied and the database cannot be found, a new one under that name will be created.

Note: it is recommended to use a DB directory name with kebab case and using only alphanumerical values for consistency with the DB filenames.
"""

def prepare_workspace(arguments:list, default_path:Path):
    arg_count = len(arguments)

    if arg_count == 1:
        target_path = Path(default_path)
    elif arg_count == 2:
        target_path = Path(arguments[1])
    else:
        raise(ArgumentError(f"Incorrect number of arguments supplied: expected max 2, received {arg_count}"))

    db_dir = target_path.expanduser().resolve()

    if not is_valid_pathname(db_dir.name):
        raise ValueError(f"The database name {db_dir} does not meet the following requirements: minimum length 1 character, only numbers and lower case letters.")

    if db_dir.is_file():
        raise(WorkspaceError(f"Specified database must be a directory, not a file."))

    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir

