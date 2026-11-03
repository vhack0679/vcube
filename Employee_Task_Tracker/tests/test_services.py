"""Unit tests for service-layer validation that does not need MySQL."""

import pytest

from employee_task_tracker.core.services import (
    PRIORITIES,
    STATUSES,
    _parse_date,
    _positive_id,
    create_employee,
    create_task,
)
from employee_task_tracker.exceptions import ValidationError


def test_parse_optional_date() -> None:
    assert _parse_date("") is None
    assert _parse_date("2026-10-23").isoformat() == "2026-10-23"


def test_parse_date_rejects_invalid_date() -> None:
    with pytest.raises(ValidationError, match="YYYY-MM-DD"):
        _parse_date("23-10-2026")


@pytest.mark.parametrize("value", [0, -1, "abc", "1.5"])
def test_positive_id_rejects_invalid_values(value: object) -> None:
    with pytest.raises(ValidationError):
        _positive_id(value)  # type: ignore[arg-type]


def test_create_employee_rejects_invalid_email_before_database_access() -> None:
    with pytest.raises(ValidationError, match="valid email"):
        create_employee("Test Employee", "Developer", "not-an-email")


def test_create_task_rejects_unknown_priority_before_database_access() -> None:
    with pytest.raises(ValidationError, match="Priority must be one of"):
        create_task("Test task", "", "Urgent")


def test_specification_status_and_priority_values() -> None:
    assert STATUSES == ("Pending", "In Progress", "Completed", "On Hold")
    assert PRIORITIES == ("Low", "Medium", "High", "Critical")


def test_old_status_value_is_rejected_before_database_access() -> None:
    from employee_task_tracker.core.services import update_task_status

    with pytest.raises(ValidationError, match="Status must be one of"):
        update_task_status(1, "Blocked")


def test_old_priority_value_is_rejected_before_database_access() -> None:
    with pytest.raises(ValidationError, match="Priority must be one of"):
        create_task("Test task", "", "Urgent")
