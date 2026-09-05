import sys
from pathlib import Path
from engine.errors import FatalAppError
from engine.config import load_config
from engine.workspace import prepare_workspace
from engine.data import Database
from engine.loader import load_tables

CURRENT_DIR = Path(__file__).resolve()

def run_txtbase():
    # Note: this try-catch block only handles unrecoverable/unexpected errors
    # Recoverable errors should be handled within the submodules.
    try:
        db_settings = load_config("config.toml", CURRENT_DIR)
        db_path = prepare_workspace(
            arguments=sys.argv,
            default_path=db_settings.default_dir
        )
        database = Database()
        database.tables = load_tables(
            db_path, 
            db_settings.ignored_paths
        )
        for name, table in database.tables.items():
            pass # TODO
    except (FatalAppError) as err:
        print(f"Error encountered. Aborting... {err.message}")
        sys.exit(err.exit_code)
    except (Exception) as err:
        print(f"Unexpected error encountered. Aborting... {err}")
        sys.exit(1)

    # With the validated directory...
    # Get set of tables that meet requirements (one level deep)
    # For each table gather valid .col files
    # Transfer data into database object using the parent as the table name
    
    # Next: load DB
    # Next: check DB integrity (even if empty) using rules engine
    # More stuff here... (server for API calls, HTTP viewer, stats...)
    # Shut down.
