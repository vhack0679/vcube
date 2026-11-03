"""Tests for configuration validation."""

import pytest

from employee_task_tracker.config import Settings


def test_settings_repr_does_not_expose_database_password() -> None:
    """The settings representation must not leak the database password."""
    settings = Settings(
        db_host="localhost",
        db_port=3306,
        db_name="test_database",
        db_user="test_user",
        db_password="very-secret-value",
    )

    assert "very-secret-value" not in repr(settings)
    assert "db_host='localhost'" in repr(settings)


def test_settings_is_immutable() -> None:
    """Settings fields cannot be reassigned after construction."""
    settings = Settings(
        db_host="localhost",
        db_port=3306,
        db_name="test_database",
        db_user="test_user",
        db_password="",
    )

    with pytest.raises(AttributeError):
        settings.db_port = 3307  # type: ignore[misc]
