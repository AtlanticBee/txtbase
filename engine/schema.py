from dataclasses import dataclass
from engine import types

"""
This relationship data class comes with two key rules:
- No columns are permitted to be nullable if they depend on foreign keys
- Cascading is not a feature of this database for the reasons below... 

The general philosphy of this database is to create a database system which, using a few simple rules, can be stored, read and modified without the overhead of binary files, user interfaces and knowledge of a language like SQL. The database should in essence be a set of textfiles that this Python engine can help maintain.

Operating Systems already have ways to display, modify, select, copy, paste and delete text. Trying not to reinvent the wheel here...

The engine will simply shout at you if foreign keys are not being honoured, rather than attempt to cascade all changes.
Perhaps in future, a command will be added as part of the "pruning" (which includes deleting rows with nulls too) to aid data integrity and database maintenance.
Perhaps this idea will change in future with ideas like a "strict" mode or more heavily audited one.

The Github CI/CD process will permit the option to fall back to the last time there were no warnings about foreign keys anyway.
"""

@dataclass
class Relationship:
    """
    The only stored relationship is a 1:1 relationship (i.e. a foreign key).
    1:M, M:1 and M:M relationships should be composed of this primitive and the relevant JOIN tables.
    """
    from_column: str
    from_table: str
    to_column: str
    to_table: str

@dataclass
class ColumnType:
    for_column: str
    column_type: types.DataType

@dataclass
class Schema:
    relationships: list[Relationship]
    column_types: list[ColumnType]