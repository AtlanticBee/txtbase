from pathlib import Path
from engine import settings
from engine import data
from engine import schema
from engine import errors
from engine import types
from dataclasses import fields
from typing import Any
import json

"""
Collect set of valid subdirectories - table paths
Add table names to DB
For each table, parse JSON schema and save if valid (fail if not with descriptive message)
For each table, collect valid column files
For each column file:
- parse data, check if schema specifies type and convert - fail if impossible
- alternatively induce the type - skipping NULLS and parse ALL rows to infer type (basically pass through each type and infer from that)
- later modifications can auto-add the type to the schema for ease of use, or at least warn about it
Add data to table column objects
Return database
"""

def is_valid_name(name:str):
    return bool(settings.global_settings.accepted_file_chars.fullmatch(name))

# def get_columns(path:Path, filters:settings.IgnoredFileNames) -> dict[str,data.Column]:
#     file_list: list[Path] = []
#     result: dict[str,data.Column] = {}

#     for child in path.iterdir():
#         if (child.suffix == settings.global_settings.column_extension) and child.is_file() and is_valid_name(child.stem) and not filters.is_ignored(child.name):
#             file_list.append(child)

#     for col_path in file_list:
#         lines = col_path.read_text(encoding="utf-8").strip().splitlines(keepends=False)
#         # For now, typing will be silent (everything will ultimately be a string if necessary, with warnings)
#         # However, to type succesfully we also need to know about the schema. So in reality... the schema parsing must come first.
#         # May need to refactor to achieve a Strict mode...
#         typed_data = 
#         result[col_path.stem] = data.Column(typed_data)

# def parse_column(col_path: Path) -> list[str]:
#     return col_path.read_text(encoding="utf-8").strip().splitlines(keepends=False)

def get_raw_schema(path: Path) -> dict[str, Any]:
    # We can assume there is only one exact match of schema.json - operating systems won't allow two.
    return json.loads(path.read_text(encoding="utf-8"))

# When extracting relationships, this function checks the basic JSON structure, but does not check engine rules. That comes later.
def get_relationships(raw_json: dict[str, Any]) -> list[schema.Relationship]:
    required_keys:tuple = {f.name for f in fields(schema.Relationship)}
    result: list[schema.Relationship] = []
    raw_relationships = raw_json.get("relationships", [])

    if not isinstance(raw_relationships, list):
        raise errors.SchemaError(f"The Schema File for the table {path.stem} is invalid. Relationships must be an array.")

    for idx, item in enumerate(raw_relationships):
        if not isinstance(item, dict):
            raise errors.SchemaError(f"The Schema File for the table {path.stem} is invalid. The relationship at index {idx} must be a dictionary.")

    for item in raw_relationships:
        if item.keys() != required_keys:
            err_msg = f"Attempted to add {path.stem} relationship to schema. Keys do not match."
            missing_keys = required_keys - item.keys()
            extra_keys = item.keys() - required_keys
            if missing_keys:
                err_msg += f" Missing keys: {missing_keys}"
            if extra_keys:
                err_msg += f" Extra keys: {extra_keys}"
            raise errors.SchemaError(err_msg)

        # The double asterisk is a shorthand for unpacking dictionaries (a single one would be for lists and tuples)
        result.append(schema.Relationship(**item))

    return result

# When extracting types, this function checks the basic JSON structure, but does not check engine rules, as with with relationships.
def get_column_types(raw_json: dict[str, Any]) -> list[schema.ColumnType]:
    required_keys:tuple = {f.name for f in fields(schema.ColumnType)}
    result: list[schema.ColumnType] = []
    raw_relationships = raw_json.get("column_types", [])

    json_data = json.loads(path.read_text(encoding="utf-8"))
    raw_types: list[dict]

def load_db(db_path: Path, filters:settings.IgnoredFileNames = settings.global_settings.ignored_filenames):
    table_paths: list[Path] = []
    db = data.Database()

    for child in db_path.iterdir():
        # We supply the full name as no extensions should be present in a folder name
        if child.is_dir() and is_valid_name(child.name) and not filters.is_ignored(child.name):
            table_paths.append(child)

    schema_filename = settings.global_settings.table_schema_filename

    for path in table_paths:
        schema_path = path / schema_filename
        raw_schema = get_raw_schema(schema_path)
        db.tables[path.stem] = data.Table(
            relationships=get_relationships(raw_schema),
            column_types = get_column_types(raw_schema)
        )
        # Schema validation can't happen until all data and schemas are loaded...