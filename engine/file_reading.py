from pathlib import Path
import json

def read_textfile(path_str):
    path = Path(path_str)
    return path.read_text(encoding="utf-8")

def read_json(path_str):
    path = Path(path_str)
    return json.loads(path.read_text(encoding="utf-8"))