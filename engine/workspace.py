import sys
from pathlib import Path
from engine import settings

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

def prepare_workspace(arguments, default_db_name = settings.global_settings.default_dir):
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

