import sys
from engine.config import load_config
from engine.workspace import prepare_workspace
from engine.data import Database

def run_txtbase():
    db_settings = load_config()
    db_path = prepare_workspace(arguments=sys.argv, default_path=db_settings.default_dir)
    database = Database()
    
    # Next: load DB
    # Next: check DB integrity (even if empty) using rules engine
    # More stuff here... (server for API calls, HTTP viewer, stats...)
    # Shut down.
