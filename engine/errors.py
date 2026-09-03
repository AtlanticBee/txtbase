class AppError(Exception):
    def __init__(self, message:str):
        """
        Note: The base class Exception itself inherits from BaseException which expects a message argument. We also create a specific copy of it for easy access.
        The Exception class is described as a non-exit Exception - not because it shouldn't lead us to exit the App, but because it shouldn't kill the underlying interpreter - as other Errors might.
        The super() keyword ensures base class initialisation runs first before our added behaviour.
        """
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message

# Divide errors types into two branches: fatal and recoverable

class FatalAppError(AppError):
    """
    Raised when an error is encountered that required the application to abort.
    """
    def __init__(self, message:str, exit_code:int = 1):
        super().__init__(message)
        self.exit_code = exit_code

class RecoverableAppError(AppError):
    """
    Raised when an error is encountered that should be logged/handled without aborting the application.
    """
    pass

# Fatal Errors

class CLIArgumentError(FatalAppError):
    """
    Raised when txtbase is called with invalid arguments.
    """
    pass

# Recoverable Errors