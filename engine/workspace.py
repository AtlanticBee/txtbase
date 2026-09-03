from engine.val_path import is_valid_pathname
from pathlib import Path
from engine.errors import CLIArgumentError

def prepare_workspace(arguments:list, default_path:Path):
    arg_count = len(arguments)

    if arg_count == 1:
        target_path = Path(default_path)
    elif arg_count == 2:
        target_path = Path(arguments[1])
    else:
        raise(CLIArgumentError(f"Incorrect number of arguments supplied: expected max 2, received {arg_count}"))

    db_dir = target_path.expanduser().resolve()

    if not is_valid_pathname(db_dir.name):
        raise CLIArgumentError(f"The database name {db_dir} does not meet the following requirements: minimum length 1 character, only numbers and lower case letters.")

    if db_dir.is_file():
        raise(CLIArgumentError(f"Specified database must be a directory, not a file."))

    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir

