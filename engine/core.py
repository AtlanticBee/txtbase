import sys
from engine.workspace import prepare_workspace
from engine.settings import load_settings

def run_txtbase():
    settings = load_settings("./engine/settings.json")
    database_path = prepare_workspace(arguments=sys.argv, default_db_name=settings["default_db_name"])
    print(database_path)
