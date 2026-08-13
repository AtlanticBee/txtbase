from enum import Enum
from typing import Any
from datetime import datetime

"""
The Enum class is... just a class! You can add your own methods.
In our case, we are specifying here the data types supported and a validation method. It's somewhere between OOP and regular functional programming?
"""

class DataType(Enum):
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    ISO_TIME = "ISO_TIME"

    def validate(self, value: Any) -> bool:
        match self:
            case DataType.INTEGER:
                # Guard against booleans - a subclass of integers in Python.
                return isinstance(value, int) and not isinstance(value, bool)

            case DataType.FLOAT:
                # Guard against booleans - which would still be inferred as ints
                return isinstance(value, float) and not isinstance(value, bool)

            case DataType.STRING:
                return isinstance(value, str)

            case DataType.BOOLEAN:
                return isinstance(value, bool)

            case DataType.ISO_TIME:
                # Must be string and parse cleanly as an ISO timestamp

                if not isinstance(value, str):
                    return False
                try:
                    datetime.fromisoformat(value)
                    return True
                except ValueError:
                    return False