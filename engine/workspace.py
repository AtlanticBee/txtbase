import sys
from pathlib import Path

incorrect_num_args_text = """
*** Error: too many arguments supplied. Aborting... ***

Maximum number of arguments: 2 (program name + path to database)
Arguments supplied: XXX

To run txtbase use either:
\t1. txtbase
\t2. txtbase [/PATH/TO/DATABASE]

If no path is supplied, the program will open the default DB file name, or create a new one.
If a path is supplied and the database cannot be found, a new one under that name will be created.
"""

def prepare_workspace(arguments, default_db_name):
    arg_count = len(arguments)

    if arg_count == 1:
        target_path = Path(default_db_name)
    elif arg_count == 2:
        target_path = Path(arguments[1])
    else:
        print(incorrect_num_args_text.replace("XXX",str(arg_count)))
        sys.exit(1)

    db_dir = target_path.expanduser().resolve()

    if db_dir.is_file():
        print(f"Error: Target path {db_dir} is an existing file, not a directory. Aborting...")
        sys.exit(1)

    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir

