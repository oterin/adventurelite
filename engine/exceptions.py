# engine/exceptions.py

class AdventureLiteException(Exception):
    """Base exception for all custom errors in the application."""
    pass


class StoryNotFoundException(AdventureLiteException):
    """Raised when a specified story cannot be found."""
    pass


class StoryLoadException(AdventureLiteException):
    """Raised when a story file has syntax errors or validation issues."""
    pass


class GameStateException(AdventureLiteException):
    """Raised for logical errors within the game state, like a missing scene."""
    pass