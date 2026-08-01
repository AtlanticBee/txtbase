import sys
from engine.parse_args import parse_args
from engine.settings import load_settings

def run_txtbase():
    settings = load_settings("./engine/settings.json")
    database_path = parse_args(arguments=sys.argv, default_db_name=settings["default_db_name"])
    print(database_path)
