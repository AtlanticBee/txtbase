from dataclasses import dataclass, field
from typing import Any
from relationships import Relationship

"""
Note: the default_factory option is required because Python sets one mutable object default value per class, not per instance. We want separate mutable objects per instance. The "field" is a part of dataclass functionality, not a Python global reserved word.
"""

@dataclass
class Column:
    """
    Contains list of values (rows).
    """
    data: list[Any] = field(default_factory=list)

@dataclass
class Table:
    """
    Contains dictionary of columns and schema information by name lookup. Can add more schema info here as required.
    Schema name corresponds to the "to_column" i.e. which column is using a FK.
    """
    columns: dict[str, Column] = field(default_factory=dict)
    relationships: dict[str, Relationship] = field(default_factory=dict)

@dataclass
class Database:
    """
    Contains dictionary of tables by name lookup.
    """
    tables: dict[str, Table] = field(default_factory=dict)