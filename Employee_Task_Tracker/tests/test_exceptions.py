"""Tests for application-specific exceptions."""

import pytest

from employee_task_tracker.exceptions import (
    AuthenticationError,
    AuthorizationError,
    ConfigurationError,
    DatabaseConnectionError,
    ValidationError,
)


@pytest.mark.parametrize(
    "exception_type",
    [
        ConfigurationError,
        DatabaseConnectionError,
        AuthenticationError,
        AuthorizationError,
        ValidationError,
    ],
)
def test_custom_exceptions_are_exception_types(exception_type: type[Exception]) -> None:
    """Each application exception can be raised and caught by type."""
    with pytest.raises(exception_type):
        raise exception_type("example failure")
