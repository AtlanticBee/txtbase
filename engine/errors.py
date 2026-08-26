class SchemaError(Exception):
    """
    Raised when a Schema File is structurally invalid.
    """
    pass

class ArgumentError(Exception):
    """
    Raised when workspace preparation fails.
    """
    pass

class WorkspaceError(Exception):
    """
    Error preparing the workspace
    """
    pass