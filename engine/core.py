import sys
from engine.workspace import prepare_workspace
from engine.settings import global_settings

def run_txtbase():
    database_path = prepare_workspace(arguments=sys.argv, default_db_name=system_settings["default_db_name"])
    # Next: load DB
    # Next: check DB integrity (even if empty) using rules engine
    # More stuff here... (server for API calls, HTTP viewer, stats...)
    # Shut down.
