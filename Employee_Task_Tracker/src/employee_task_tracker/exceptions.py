"""Application-specific exception types."""


class ConfigurationError(Exception):
    """Raised when application configuration is missing or invalid."""


class DatabaseConnectionError(Exception):
    """Raised when a database connection cannot be established."""


class AuthenticationError(Exception):
    """Raised when authentication fails."""


class AuthorizationError(Exception):
    """Raised when a user is not permitted to perform an operation."""


class ValidationError(Exception):
    """Raised when user input or business data is invalid."""
