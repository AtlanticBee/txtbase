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

def parse_args(arguments, default_db_name):
    arg_count = len(arguments)

    if arg_count == 1:
        return str(Path(default_db_name).resolve())
    elif arg_count == 2:
        # This resolve() method return an absolute path. Leading "./" are taken into account automatically.
        # We may need to consider using the additional ".expanduser()" method chained beforehand for tilde handling?
        return str(Path(arguments[1]).resolve())
    else:
        print(incorrect_num_args_text.replace("XXX",str(arg_count)))
        sys.exit()

