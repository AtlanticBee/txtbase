from pathlib import Path
from engine import settings
from engine import data
from engine import relationships
import json

def is_valid_name(name:str):
    return bool(settings.global_settings.accepted_file_chars.fullmatch(name))

def get_columns(path:Path, filters:settings.IgnoredFileNames) -> dict[str,data.Column]:
    file_list: list[Path] = []
    result: dict[str,data.Column] = {}

    for child in path.iterdir():
        if (child.suffix == settings.global_settings.column_extension) and child.is_file() and is_valid_name(child.stem) and not filters.is_ignored(child.name):
            file_list.append(child)

    for col_path in file_list:
        lines = col_path.read_text(encoding="utf-8").strip().splitlines(keepends=False)
        # For now, typing will be silent (everything will ultimately be a string if necessary, with warnings)
        # However, to type succesfully we also need to know about the schema. So in reality... the schema parsing must come first.
        # May need to refactor to achieve a Strict mode...
        typed_data = 
        result[col_path.stem] = data.Column(typed_data)

def parse_column(col_path: Path) -> list[str]:
    return col_path.read_text(encoding="utf-8").strip().splitlines(keepends=False)

def get_relationships(schema_path: Path) -> list[relationships.Relationship]:
    json_data = json.loads(schema_path.read_text(encoding="utf-8"))

def load_db(db_path: Path, filters:settings.IgnoredFileNames = settings.global_settings.ignored_filenames):
    table_paths: list[Path] = []

    db = data.Database()

    for child in db_path.iterdir():
        # We supply the full name as no extensions should be present in a folder name
        if child.is_dir() and is_valid_name(child.name) and not filters.is_ignored(child.name):
            table_paths.append(child)

    for path in table_paths:
        # Save tables in DB and get column data and schema data per table.
        db.tables[path.stem] = data.Table(
            columns=get_columns(path, filters),
            relationships=get_relationships(path)
        )
            
            for grandchild in child.iterdir():
                if grandchild.is_file() and is_valid_name(grandchild.stem) and not filters.is_ignored(grandchild.name):
                    if (grandchild.suffix == settings.global_settings.column_extension):
                        db.tables[child.name].columns[grandchild.stem] = data.Column(parse_column(grandchild))
                    if (grandchild.name == settings.global_settings.table_schema_filename):
                        relationships = get_relationships(grandchild)
                        schema.relationships[child.name] = blah