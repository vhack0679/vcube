"""Business operations that match the Employee Task Tracker requirements."""

import re
from datetime import date
from typing import Any

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError

from employee_task_tracker.database.connection import get_connection
from employee_task_tracker.exceptions import AuthenticationError, ValidationError

PRIORITIES = ("Low", "Medium", "High", "Critical")
STATUSES = ("Pending", "In Progress", "Completed", "On Hold")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
PASSWORD_HASHER = PasswordHasher()


def _required(value: str, label: str, max_length: int | None = None) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValidationError(f"{label} is required.")
    if max_length is not None and len(cleaned) > max_length:
        raise ValidationError(f"{label} must be at most {max_length} characters.")
    return cleaned


def _parse_date(value: str) -> date | None:
    if not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise ValidationError("Date must use YYYY-MM-DD format.") from exc


def _positive_id(value: int | str, label: str = "ID") -> int:
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise ValidationError(f"{label} must be a whole number.") from exc
    if result < 1:
        raise ValidationError(f"{label} must be greater than zero.")
    return result


def _employee_auth_columns(cursor: Any, database: str) -> set[str]:
    """Return employee column names with either tuple or dictionary cursors."""
    cursor.execute(
        "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'employees'",
        (database,),
    )
    columns = cursor.fetchall()
    return {row["COLUMN_NAME"] if isinstance(row, dict) else row[0] for row in columns}


def create_employee(
    name: str,
    role: str,
    email: str,
    password: str | None = None,
    account_role: str = "employee",
) -> int:
    """Create an employee; password is optional for initial legacy records."""
    name = _required(name, "Name", 150)
    role = _required(role, "Role", 100)
    email = _required(email, "Email", 200).lower()
    account_role = _required(account_role, "Account role").lower()
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValidationError("Enter a valid email address.")
    if account_role not in {"admin", "employee"}:
        raise ValidationError("Account role must be admin or employee.")
    if password is not None and len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    password_hash = PASSWORD_HASHER.hash(password) if password else None

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()[0]
        columns = _employee_auth_columns(cursor, database)
        cursor.execute("SELECT id FROM employees WHERE LOWER(email) = %s", (email,))
        if cursor.fetchone():
            raise ValidationError("An employee with this email already exists.")
        if {"password_hash", "account_role"}.issubset(columns):
            cursor.execute(
                "INSERT INTO employees "
                "(name, role, email, password_hash, account_role, created_at) "
                "VALUES (%s, %s, %s, %s, %s, NOW())",
                (name, role, email, password_hash, account_role),
            )
        else:
            cursor.execute(
                "INSERT INTO employees (name, role, email, created_at) "
                "VALUES (%s, %s, %s, NOW())",
                (name, role, email),
            )
        connection.commit()
        return int(cursor.lastrowid)
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def update_employee(employee_id: int | str, name: str, role: str, email: str) -> None:
    """Update an employee's name, role, and email."""
    employee_id = _positive_id(employee_id, "Employee ID")
    name = _required(name, "Name", 150)
    role = _required(role, "Role", 100)
    email = _required(email, "Email", 200).lower()
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValidationError("Enter a valid email address.")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT id FROM employees WHERE LOWER(email) = %s AND id <> %s",
            (email, employee_id),
        )
        if cursor.fetchone():
            raise ValidationError("Another employee already uses this email.")
        cursor.execute(
            "UPDATE employees SET name = %s, role = %s, email = %s WHERE id = %s",
            (name, role, email, employee_id),
        )
        if cursor.rowcount == 0:
            cursor.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
            if cursor.fetchone() is None:
                raise ValidationError(f"Employee {employee_id} does not exist.")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def delete_employee(employee_id: int | str) -> None:
    """Delete an employee and their task assignments/comments."""
    employee_id = _positive_id(employee_id, "Employee ID")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT account_role FROM employees WHERE id = %s", (employee_id,)
        )
        record = cursor.fetchone()
        if record is None:
            raise ValidationError(f"Employee {employee_id} does not exist.")
        if record[0] == "admin":
            cursor.execute(
                "SELECT COUNT(*) FROM employees WHERE account_role = 'admin'"
            )
            if int(cursor.fetchone()[0]) <= 1:
                raise ValidationError("Cannot delete the last admin account.")
        cursor.execute("DELETE FROM comments WHERE employee_id = %s", (employee_id,))
        cursor.execute(
            "DELETE FROM assigned_tasks WHERE employee_id = %s", (employee_id,)
        )
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def list_employees() -> list[dict[str, Any]]:
    """Return employees ordered by their IDs, excluding password hashes."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, role, email, created_at FROM employees ORDER BY id"
        )
        return list(cursor.fetchall())
    finally:
        cursor.close()
        connection.close()


def get_employee(employee_id: int | str) -> dict[str, Any]:
    """Retrieve an employee profile without returning password data."""
    employee_id = _positive_id(employee_id, "Employee ID")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, name, role, email, created_at FROM employees WHERE id = %s",
            (employee_id,),
        )
        record = cursor.fetchone()
        if record is None:
            raise ValidationError(f"Employee {employee_id} does not exist.")
        return record
    finally:
        cursor.close()
        connection.close()


def authenticate(email: str, password: str) -> dict[str, Any]:
    """Authenticate a user using the Argon2 password hash."""
    email = _required(email, "Email", 200).lower()
    if not EMAIL_PATTERN.fullmatch(email) or not password:
        raise AuthenticationError("Invalid email or password.")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT DATABASE() AS database_name")
        database = cursor.fetchone()["database_name"]
        columns = _employee_auth_columns(cursor, database)
        if not {"password_hash", "account_role"}.issubset(columns):
            raise AuthenticationError(
                "Login columns are not installed. Run the application "
                "to upgrade the schema."
            )
        cursor.execute(
            "SELECT id, name, role, email, password_hash, account_role "
            "FROM employees WHERE LOWER(email) = %s",
            (email,),
        )
        user = cursor.fetchone()
        if not user or not user["password_hash"]:
            raise AuthenticationError("Invalid email or password.")
        try:
            PASSWORD_HASHER.verify(user["password_hash"], password)
        except (VerifyMismatchError, VerificationError, InvalidHashError) as exc:
            raise AuthenticationError("Invalid email or password.") from exc
        if PASSWORD_HASHER.check_needs_rehash(user["password_hash"]):
            cursor.execute(
                "UPDATE employees SET password_hash = %s WHERE id = %s",
                (PASSWORD_HASHER.hash(password), user["id"]),
            )
            connection.commit()
        user.pop("password_hash", None)
        return user
    finally:
        cursor.close()
        connection.close()


def set_employee_password(employee_id: int | str, password: str) -> None:
    """Set or reset an employee login password to a salted Argon2 hash."""
    employee_id = _positive_id(employee_id, "Employee ID")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    password_hash = PASSWORD_HASHER.hash(password)
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Employee {employee_id} does not exist.")
        cursor.execute(
            "UPDATE employees SET password_hash = %s WHERE id = %s",
            (password_hash, employee_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def create_task(title: str, description: str, priority: str, due_date: str = "") -> int:
    """Create a task with the priority values required by the specification."""
    title = _required(title, "Title", 200)
    description = description.strip()
    priority = _required(priority, "Priority").title()
    if priority not in PRIORITIES:
        raise ValidationError(f"Priority must be one of: {', '.join(PRIORITIES)}.")
    parsed_due_date = _parse_date(due_date)
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO `task` "
            "(title, description, priority, due_date, status, created_at) "
            "VALUES (%s, %s, %s, %s, 'Pending', NOW())",
            (title, description or None, priority, parsed_due_date),
        )
        connection.commit()
        return int(cursor.lastrowid)
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def update_task(
    task_id: int | str, title: str, description: str, priority: str, due_date: str
) -> None:
    """Update task details while preserving its workflow status."""
    task_id = _positive_id(task_id, "Task ID")
    title = _required(title, "Title", 200)
    priority = _required(priority, "Priority").title()
    if priority not in PRIORITIES:
        raise ValidationError(f"Priority must be one of: {', '.join(PRIORITIES)}.")
    parsed_due_date = _parse_date(due_date)
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE `task` SET title = %s, description = %s, "
            "priority = %s, due_date = %s "
            "WHERE id = %s",
            (title, description.strip() or None, priority, parsed_due_date, task_id),
        )
        if cursor.rowcount == 0:
            cursor.execute("SELECT id FROM `task` WHERE id = %s", (task_id,))
            if cursor.fetchone() is None:
                raise ValidationError(f"Task {task_id} does not exist.")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def delete_task(task_id: int | str) -> None:
    """Delete a task and its related assignments and comments."""
    task_id = _positive_id(task_id, "Task ID")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM `task` WHERE id = %s", (task_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Task {task_id} does not exist.")
        cursor.execute("DELETE FROM comments WHERE task_id = %s", (task_id,))
        cursor.execute("DELETE FROM assigned_tasks WHERE task_id = %s", (task_id,))
        cursor.execute("DELETE FROM `task` WHERE id = %s", (task_id,))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def list_tasks(
    status: str = "",
    priority: str = "",
    employee_id: int | str | None = None,
    search: str = "",
    completed_only: bool = False,
    due_from: str = "",
    due_to: str = "",
) -> list[dict[str, Any]]:
    """List tasks using the optional status, priority, employee, and text filters."""
    query = (
        "SELECT t.id, t.title, t.description, t.priority, t.due_date, t.status, "
        "t.created_at, GROUP_CONCAT(DISTINCT e.name ORDER BY e.name "
        "SEPARATOR ', ') AS assignees "
        "FROM `task` t LEFT JOIN assigned_tasks a ON a.task_id = t.id "
        "LEFT JOIN employees e ON e.id = a.employee_id"
    )
    conditions: list[str] = []
    params: list[Any] = []
    if status.strip():
        normalized = status.strip().title()
        if normalized not in STATUSES:
            raise ValidationError(f"Status must be one of: {', '.join(STATUSES)}.")
        conditions.append("t.status = %s")
        params.append(normalized)
    if priority.strip():
        normalized_priority = priority.strip().title()
        if normalized_priority not in PRIORITIES:
            raise ValidationError(f"Priority must be one of: {', '.join(PRIORITIES)}.")
        conditions.append("t.priority = %s")
        params.append(normalized_priority)
    if employee_id is not None and str(employee_id).strip():
        conditions.append("a.employee_id = %s")
        params.append(_positive_id(employee_id, "Employee ID"))
    if search.strip():
        conditions.append(
            "(t.title LIKE %s OR t.description LIKE %s OR e.name LIKE %s)"
        )
        pattern = f"%{search.strip()}%"
        params.extend((pattern, pattern, pattern))
    if due_from.strip():
        conditions.append("t.due_date >= %s")
        params.append(_parse_date(due_from))
    if due_to.strip():
        conditions.append("t.due_date <= %s")
        params.append(_parse_date(due_to))
    if completed_only:
        conditions.append("t.status = 'Completed'")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " GROUP BY t.id ORDER BY t.id"

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, tuple(params))
        return list(cursor.fetchall())
    finally:
        cursor.close()
        connection.close()


def assign_task(task_id: int | str, employee_id: int | str) -> None:
    """Assign a task to an existing employee without duplicate assignments."""
    task_id = _positive_id(task_id, "Task ID")
    employee_id = _positive_id(employee_id, "Employee ID")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM `task` WHERE id = %s", (task_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Task {task_id} does not exist.")
        cursor.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Employee {employee_id} does not exist.")
        cursor.execute(
            "SELECT id FROM assigned_tasks WHERE task_id = %s AND employee_id = %s",
            (task_id, employee_id),
        )
        if cursor.fetchone():
            raise ValidationError("This task is already assigned to that employee.")
        cursor.execute(
            "INSERT INTO assigned_tasks (task_id, employee_id, assigned_date) "
            "VALUES (%s, %s, %s)",
            (task_id, employee_id, date.today()),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def unassign_task(task_id: int | str, employee_id: int | str) -> None:
    """Remove one task assignment."""
    task_id = _positive_id(task_id, "Task ID")
    employee_id = _positive_id(employee_id, "Employee ID")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM assigned_tasks WHERE task_id = %s AND employee_id = %s",
            (task_id, employee_id),
        )
        if cursor.rowcount == 0:
            raise ValidationError("That task assignment was not found.")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def update_task_status(task_id: int | str, status: str) -> None:
    """Update a task status using Pending/In Progress/Completed/On Hold."""
    task_id = _positive_id(task_id, "Task ID")
    normalized = _required(status, "Status").title()
    if normalized not in STATUSES:
        raise ValidationError(f"Status must be one of: {', '.join(STATUSES)}.")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE `task` SET status = %s WHERE id = %s", (normalized, task_id)
        )
        if cursor.rowcount == 0:
            cursor.execute("SELECT id FROM `task` WHERE id = %s", (task_id,))
            if cursor.fetchone() is None:
                raise ValidationError(f"Task {task_id} does not exist.")
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def add_comment(task_id: int | str, employee_id: int | str, comment: str) -> int:
    """Add a comment to a task on behalf of an existing employee."""
    task_id = _positive_id(task_id, "Task ID")
    employee_id = _positive_id(employee_id, "Employee ID")
    comment = _required(comment, "Comment")
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM `task` WHERE id = %s", (task_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Task {task_id} does not exist.")
        cursor.execute("SELECT id FROM employees WHERE id = %s", (employee_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Employee {employee_id} does not exist.")
        cursor.execute(
            "INSERT INTO comments (task_id, employee_id, comment, created_at) "
            "VALUES (%s, %s, %s, NOW())",
            (task_id, employee_id, comment),
        )
        connection.commit()
        return int(cursor.lastrowid)
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def list_comments(task_id: int | str) -> list[dict[str, Any]]:
    """Return a task's comments with their employee names."""
    task_id = _positive_id(task_id, "Task ID")
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM `task` WHERE id = %s", (task_id,))
        if cursor.fetchone() is None:
            raise ValidationError(f"Task {task_id} does not exist.")
        cursor.execute(
            "SELECT c.id, c.comment, c.created_at, e.name AS employee_name "
            "FROM comments c JOIN employees e ON e.id = c.employee_id "
            "WHERE c.task_id = %s ORDER BY c.created_at, c.id",
            (task_id,),
        )
        return list(cursor.fetchall())
    finally:
        cursor.close()
        connection.close()


def get_report() -> dict[str, Any]:
    """Return dashboard totals, status totals, overdue and per-employee workload."""
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total FROM employees")
        employees = int(cursor.fetchone()["total"])
        cursor.execute("SELECT COUNT(*) AS total FROM `task`")
        tasks = int(cursor.fetchone()["total"])
        cursor.execute("SELECT status, COUNT(*) AS total FROM `task` GROUP BY status")
        status_counts = {row["status"]: int(row["total"]) for row in cursor.fetchall()}
        cursor.execute(
            "SELECT COUNT(*) AS total FROM `task` "
            "WHERE due_date < CURDATE() AND status <> 'Completed'"
        )
        overdue = int(cursor.fetchone()["total"])
        cursor.execute(
            "SELECT COUNT(*) AS total FROM `task` "
            "WHERE due_date BETWEEN CURDATE() "
            "AND DATE_ADD(CURDATE(), INTERVAL 7 DAY) "
            "AND status <> 'Completed'"
        )
        upcoming = int(cursor.fetchone()["total"])
        cursor.execute(
            "SELECT e.id, e.name, COUNT(DISTINCT a.task_id) AS assigned_tasks, "
            "COALESCE(SUM(t.status = 'Completed'), 0) AS completed_tasks "
            "FROM employees e LEFT JOIN assigned_tasks a ON a.employee_id = e.id "
            "LEFT JOIN `task` t ON t.id = a.task_id GROUP BY e.id ORDER BY e.name"
        )
        employee_performance = list(cursor.fetchall())
        return {
            "employees": employees,
            "tasks": tasks,
            "status_counts": status_counts,
            "overdue": overdue,
            "upcoming": upcoming,
            "employee_performance": employee_performance,
        }
    finally:
        cursor.close()
        connection.close()


def get_employee_tasks(employee_id: int | str) -> list[dict[str, Any]]:
    """Return tasks assigned to the selected employee."""
    employee_id = _positive_id(employee_id, "Employee ID")
    return list_tasks(employee_id=employee_id)


def get_admin_count() -> int:
    """Count admin accounts, when login columns are installed."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()[0]
        columns = _employee_auth_columns(cursor, database)
        if "account_role" not in columns:
            return 0
        cursor.execute("SELECT COUNT(*) FROM employees WHERE account_role = 'admin'")
        return int(cursor.fetchone()[0])
    finally:
        cursor.close()
        connection.close()


def create_first_admin(name: str, role: str, email: str, password: str) -> int:
    """Create the first admin or promote a matching existing employee account."""
    if get_admin_count() > 0:
        raise ValidationError("An admin account already exists.")
    name = _required(name, "Name", 150)
    role = _required(role or "Administrator", "Role", 100)
    email = _required(email, "Email", 200).lower()
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValidationError("Enter a valid email address.")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    password_hash = PASSWORD_HASHER.hash(password)

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id FROM employees WHERE LOWER(email) = %s", (email,))
        existing = cursor.fetchone()
        if existing:
            admin_id = int(existing[0])
            cursor.execute(
                "UPDATE employees SET name = %s, role = %s, password_hash = %s, "
                "account_role = 'admin' WHERE id = %s",
                (name, role, password_hash, admin_id),
            )
        else:
            cursor.execute(
                "INSERT INTO employees "
                "(name, role, email, password_hash, account_role, created_at) "
                "VALUES (%s, %s, %s, %s, 'admin', NOW())",
                (name, role, email, password_hash),
            )
            admin_id = int(cursor.lastrowid)
        connection.commit()
        return admin_id
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


# Public service names matching the project specification.
def add_employee(
    name: str,
    role: str,
    email: str,
    password: str | None = None,
    account_role: str = "employee",
) -> int:
    """Add a new employee account."""
    return create_employee(name, role, email, password, account_role)


def view_tasks(
    status: str = "",
    priority: str = "",
    due_from: str = "",
    due_to: str = "",
    employee_id: int | str | None = None,
) -> list[dict[str, Any]]:
    """View tasks with status, priority, date-range, and employee filters."""
    return list_tasks(
        status=status,
        priority=priority,
        employee_id=employee_id,
        due_from=due_from,
        due_to=due_to,
    )


def search_tasks(
    keyword: str,
    status: str = "",
    priority: str = "",
    due_from: str = "",
    due_to: str = "",
    employee_id: int | str | None = None,
) -> list[dict[str, Any]]:
    """Search task titles, descriptions, and employee names with optional filters."""
    return list_tasks(
        status=status,
        priority=priority,
        employee_id=employee_id,
        search=keyword,
        due_from=due_from,
        due_to=due_to,
    )


def generate_reports() -> dict[str, Any]:
    """Generate dashboard and employee-performance reporting data."""
    return get_report()
