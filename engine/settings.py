import sys
from engine.file_reading import read_json

def load_settings(path_str):
    settings = read_json(path_str)
    if not settings:
        print("No system settings found. Aborting...")
        sys.exit(1)

    return settings