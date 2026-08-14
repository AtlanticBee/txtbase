import sys
from engine.workspace import prepare_workspace
from engine.loader import load_db
from engine.data import Database

def run_txtbase():
    db_path = prepare_workspace(arguments=sys.argv)
    database: Database = load_db(path=db_path)
    # Next: load DB
    # Next: check DB integrity (even if empty) using rules engine
    # More stuff here... (server for API calls, HTTP viewer, stats...)
    # Shut down.
