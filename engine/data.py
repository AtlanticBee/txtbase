from dataclasses import dataclass, field
from typing import Any
from engine.schema import Relationship

"""
Note: the default_factory option is required because Python sets one mutable object default value per class, not per instance. We want separate mutable objects per instance. The "field" is a part of dataclass functionality, not a Python global reserved word. I did consider whether or not the columns should be nested inside the table data structures. A benefit is you can have two columns of the same name in different tables. Another is that at one level of nesting, it's still readable to call "parent.child". Thirdly, it forbids automatically any duplicate table names. A downside is that long-term it makes the data structure more complex and possibly rigid or slower.
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