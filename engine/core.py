import sys
from pathlib import Path
import tomllib
from engine.errors import WorkspaceError, ArgumentError
from engine.config import load_config
from engine.workspace import prepare_workspace
from engine.data import Database
from engine.loader import load_tables

CURRENT_DIR = Path(__file__).resolve()

def run_txtbase():
    # Load configuration
    try:
        db_settings = load_config("config.toml", CURRENT_DIR)
    except (tomllib.TOMLDecodeError, TypeError, FileNotFoundError) as err:
        print(f"Error during config.toml parsing. Aborting... {err}")
        sys.exit(1)
    # Validate and/or create the database folder
    try:
        db_path = prepare_workspace(
            arguments=sys.argv,
            default_path=db_settings.default_dir
            )
    except (ArgumentError, WorkspaceError, ValueError) as err:
        print(f"Error encoutered during workspace preparation. Aborting... {err}")

    database = Database()
    database.tables = load_tables(db_path)
    # With the validated directory...
    # Get set of tables that meet requirements (one level deep)
    # For each table gather valid .col files
    # Transfer data into database object using the parent as the table name
    
    # Next: load DB
    # Next: check DB integrity (even if empty) using rules engine
    # More stuff here... (server for API calls, HTTP viewer, stats...)
    # Shut down.
