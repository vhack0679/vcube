"""Role-based console menus for the Employee Task Tracking System."""

from collections.abc import Callable
from datetime import date, timedelta
from getpass import getpass
from typing import Any

import mysql.connector

from employee_task_tracker.core import services
from employee_task_tracker.database.schema import ensure_schema
from employee_task_tracker.exceptions import (
    AuthenticationError,
    ConfigurationError,
    DatabaseConnectionError,
    ValidationError,
)


def _pause() -> None:
    input("\nPress Enter to continue...")


def _read_int(prompt: str) -> int:
    return int(input(prompt).strip())


def _print_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> None:
    if not rows:
        print("\nNo records found.")
        return
    rendered = [
        ["-" if row.get(key) is None else str(row.get(key)) for key, _ in columns]
        for row in rows
    ]
    widths = [
        max(len(label), *(len(row[index]) for row in rendered))
        for index, (_, label) in enumerate(columns)
    ]
    print(
        "\n"
        + " | ".join(label.ljust(widths[i]) for i, (_, label) in enumerate(columns))
    )
    print("-+-".join("-" * width for width in widths))
    for row in rendered:
        print(" | ".join(value.ljust(widths[i]) for i, value in enumerate(row)))


def _employee_columns() -> list[tuple[str, str]]:
    return [("id", "ID"), ("name", "Name"), ("role", "Role"), ("email", "Email")]


def _task_columns() -> list[tuple[str, str]]:
    return [
        ("id", "ID"),
        ("title", "Title"),
        ("priority", "Priority"),
        ("status", "Status"),
        ("due_date", "Due date"),
        ("assignees", "Assigned employees"),
    ]


def _add_employee() -> None:
    name = input("Employee name: ")
    role = input("Job role: ")
    email = input("Email address: ")
    password = getpass("Login password (minimum 8 characters): ")
    employee_id = services.create_employee(name, role, email, password=password)
    print(f"Employee created. Employee ID: {employee_id}")


def _update_employee() -> None:
    employee_id = _read_int("Employee ID to update: ")
    existing = services.get_employee(employee_id)
    name = input(f"Name [{existing['name']}]: ") or existing["name"]
    role = input(f"Role [{existing['role']}]: ") or existing["role"]
    email = input(f"Email [{existing['email']}]: ") or existing["email"]
    services.update_employee(employee_id, name, role, email)
    print("Employee details updated.")


def _delete_employee(current_admin_id: int | None = None) -> None:
    employee_id = _read_int("Employee ID to delete: ")
    if current_admin_id is not None and employee_id == current_admin_id:
        raise ValidationError(
            "You cannot delete the currently signed-in admin account."
        )
    employee = services.get_employee(employee_id)
    if (
        input(
            f"Delete {employee['name']} and their assignments/comments? (yes/no): "
        ).lower()
        != "yes"
    ):
        print("Deletion cancelled.")
        return
    services.delete_employee(employee_id)
    print("Employee deleted.")


def _list_employees() -> None:
    _print_table(services.list_employees(), _employee_columns())


def _create_task() -> None:
    print("Priorities: " + ", ".join(services.PRIORITIES))
    task_id = services.create_task(
        input("Task title: "),
        input("Description: "),
        input("Priority [Medium]: ") or "Medium",
        input("Due date YYYY-MM-DD (optional): "),
    )
    print(f"Task created. Task ID: {task_id}")


def _update_task() -> None:
    task_id = _read_int("Task ID to update: ")
    existing_rows = [row for row in services.list_tasks() if row["id"] == task_id]
    if not existing_rows:
        raise ValidationError(f"Task {task_id} does not exist.")
    existing = existing_rows[0]
    title = input(f"Title [{existing['title']}]: ") or existing["title"]
    description = input(f"Description [{existing['description'] or ''}]: ") or (
        existing["description"] or ""
    )
    print("Priorities: " + ", ".join(services.PRIORITIES))
    priority = input(f"Priority [{existing['priority']}]: ") or existing["priority"]
    due_date = input(f"Due date [{existing['due_date'] or ''}]: ") or str(
        existing["due_date"] or ""
    )
    services.update_task(task_id, title, description, priority, due_date)
    print("Task details updated.")


def _delete_task() -> None:
    task_id = _read_int("Task ID to delete: ")
    if (
        input("Delete this task and its comments/assignments? (yes/no): ").lower()
        != "yes"
    ):
        print("Deletion cancelled.")
        return
    services.delete_task(task_id)
    print("Task deleted.")


def _list_tasks() -> None:
    _print_table(services.list_tasks(), _task_columns())


def _filter_tasks() -> None:
    print("Leave any filter blank to skip it.")
    status = input(f"Status {services.STATUSES}: ")
    priority = input(f"Priority {services.PRIORITIES}: ")
    employee = input("Employee ID: ").strip()
    search = input("Text search (title, description, employee): ")
    due_from = input("Due on/after YYYY-MM-DD: ")
    due_to = input("Due on/before YYYY-MM-DD: ")
    _print_table(
        services.list_tasks(
            status,
            priority,
            employee or None,
            search,
            due_from=due_from,
            due_to=due_to,
        ),
        _task_columns(),
    )


def _assign_task() -> None:
    task_id = _read_int("Task ID: ")
    print("Employees:")
    _list_employees()
    employee_id = _read_int("Employee ID to assign: ")
    services.assign_task(task_id, employee_id)
    print("Task assigned successfully.")


def _update_status_for_employee(employee_id: int | None = None) -> None:
    task_id = _read_int("Task ID: ")
    if employee_id is not None:
        assigned_ids = {row["id"] for row in services.get_employee_tasks(employee_id)}
        if task_id not in assigned_ids:
            raise ValidationError(
                "You can update status only for a task assigned to you."
            )
    print("Statuses: " + ", ".join(services.STATUSES))
    status = input("New status: ")
    services.update_task_status(task_id, status)
    print("Task status updated.")


def _add_comment(employee_id: int | None = None) -> None:
    task_id = _read_int("Task ID: ")
    if employee_id is None:
        employee_id = _read_int("Commenting employee ID: ")
    else:
        assigned_ids = {row["id"] for row in services.get_employee_tasks(employee_id)}
        if task_id not in assigned_ids:
            raise ValidationError("You can comment only on a task assigned to you.")
    comment_id = services.add_comment(task_id, employee_id, input("Comment: "))
    print(f"Comment added. Comment ID: {comment_id}")


def _list_comments() -> None:
    task_id = _read_int("Task ID: ")
    _print_table(
        services.list_comments(task_id),
        [
            ("id", "ID"),
            ("employee_name", "Employee"),
            ("comment", "Comment"),
            ("created_at", "Created at"),
        ],
    )


def _view_report() -> None:
    report = services.get_report()
    print("\n========== DASHBOARD / REPORTS ==========")
    print(f"Total employees:   {report['employees']}")
    print(f"Total tasks:       {report['tasks']}")
    print(f"Completed tasks:   {report['status_counts'].get('Completed', 0)}")
    print(f"Pending tasks:     {report['status_counts'].get('Pending', 0)}")
    print(f"Overdue tasks:     {report['overdue']}")
    print(f"Due in next 7 days: {report['upcoming']}")
    print("\nTask statuses:")
    for status in services.STATUSES:
        print(f"  {status:<12} {report['status_counts'].get(status, 0)}")
    print("\nEmployee performance:")
    _print_table(
        report["employee_performance"],
        [
            ("id", "ID"),
            ("name", "Employee"),
            ("assigned_tasks", "Assigned"),
            ("completed_tasks", "Completed"),
        ],
    )


def _profile(employee_id: int) -> None:
    _print_table([services.get_employee(employee_id)], _employee_columns())
    if input("Update your name/role/email? (yes/no): ").lower() == "yes":
        current = services.get_employee(employee_id)
        name = input(f"Name [{current['name']}]: ") or current["name"]
        role = input(f"Role [{current['role']}]: ") or current["role"]
        email = input(f"Email [{current['email']}]: ") or current["email"]
        services.update_employee(employee_id, name, role, email)
        print("Profile updated.")
    if input("Change your login password? (yes/no): ").lower() == "yes":
        new_password = getpass("New password (minimum 8 characters): ")
        confirm = getpass("Confirm password: ")
        if new_password != confirm:
            raise ValidationError("Passwords do not match.")
        services.set_employee_password(employee_id, new_password)
        print("Password updated.")


def _employee_dashboard(employee_id: int) -> None:
    rows = services.get_employee_tasks(employee_id)
    today = date.today()
    next_week = today + timedelta(days=7)
    completed = sum(row["status"] == "Completed" for row in rows)
    overdue = sum(
        row["due_date"] is not None
        and row["due_date"] < today
        and row["status"] != "Completed"
        for row in rows
    )
    upcoming = sum(
        row["due_date"] is not None
        and today <= row["due_date"] <= next_week
        and row["status"] != "Completed"
        for row in rows
    )
    print(
        f"\nMy tasks: {len(rows)} | Completed: {completed} "
        f"| Remaining: {len(rows) - completed}"
    )
    print(f"Overdue: {overdue} | Due within 7 days: {upcoming}")
    _print_table(rows, _task_columns())


def _filter_employee_tasks(employee_id: int) -> None:
    print("Leave status and priority blank to show all assigned tasks.")
    status = input(f"Status {services.STATUSES}: ")
    priority = input(f"Priority {services.PRIORITIES}: ")
    due_from = input("Due on/after YYYY-MM-DD: ")
    due_to = input("Due on/before YYYY-MM-DD: ")
    _print_table(
        services.list_tasks(
            status=status,
            priority=priority,
            employee_id=employee_id,
            due_from=due_from,
            due_to=due_to,
        ),
        _task_columns(),
    )


def _employee_menu(user: dict[str, Any]) -> None:
    employee_id = int(user["id"])
    actions: dict[str, tuple[str, Callable[[], None]]] = {
        "1": ("Dashboard", lambda: _employee_dashboard(employee_id)),
        "2": ("My tasks", lambda: _employee_dashboard(employee_id)),
        "3": ("View task details", lambda: _show_employee_task(employee_id)),
        "4": (
            "Filter my tasks by status/priority",
            lambda: _filter_employee_tasks(employee_id),
        ),
        "5": ("Update task status", lambda: _update_status_for_employee(employee_id)),
        "6": ("Add task comment", lambda: _add_comment(employee_id)),
        "7": (
            "View completed tasks",
            lambda: _print_table(
                services.list_tasks(employee_id=employee_id, completed_only=True),
                _task_columns(),
            ),
        ),
        "8": ("Profile", lambda: _profile(employee_id)),
    }
    _run_menu("EMPLOYEE SECTION", actions)


def _show_employee_task(employee_id: int) -> None:
    task_id = _read_int("Task ID: ")
    rows = [
        row for row in services.get_employee_tasks(employee_id) if row["id"] == task_id
    ]
    if not rows:
        raise ValidationError("That task is not assigned to your account.")
    row = rows[0]
    print(f"\nTask ID: {row['id']}")
    print(f"Title: {row['title']}")
    print(f"Description: {row['description'] or '-'}")
    print(f"Due date: {row['due_date'] or '-'}")
    print(f"Priority: {row['priority']}")
    print(f"Status: {row['status']}")
    _print_table(rows, _task_columns())
    _print_table(
        services.list_comments(task_id),
        [
            ("id", "ID"),
            ("employee_name", "Employee"),
            ("comment", "Comment"),
            ("created_at", "Created at"),
        ],
    )


def _admin_menu(user: dict[str, Any]) -> None:
    actions: dict[str, tuple[str, Callable[[], None]]] = {
        "1": ("Dashboard", _view_report),
        "2": ("Manage employees - list", _list_employees),
        "3": ("Manage employees - add", _add_employee),
        "4": ("Manage employees - update", _update_employee),
        "5": ("Manage employees - delete", lambda: _delete_employee(int(user["id"]))),
        "6": ("Create task", _create_task),
        "7": ("Assign task", _assign_task),
        "8": ("View all tasks", _list_tasks),
        "9": ("Search / filter tasks", _filter_tasks),
        "10": ("Update / delete task", _admin_edit_delete_task),
        "11": ("Add comment", _add_comment),
        "12": ("View comments", _list_comments),
        "13": ("Reports and analytics", _view_report),
        "14": ("Set/reset employee password", _admin_reset_password),
    }
    _run_menu("ADMIN SECTION", actions)


def _admin_edit_delete_task() -> None:
    print("1. Update task details  2. Delete task  3. Update status")
    choice = input("Choose action: ").strip()
    if choice == "1":
        _update_task()
    elif choice == "2":
        _delete_task()
    elif choice == "3":
        _update_status_for_employee()
    else:
        print("Invalid option.")


def _admin_reset_password() -> None:
    employee_id = _read_int("Employee ID: ")
    new_password = getpass("New password (minimum 8 characters): ")
    confirm = getpass("Confirm password: ")
    if new_password != confirm:
        raise ValidationError("Passwords do not match.")
    services.set_employee_password(employee_id, new_password)
    print("Password reset successfully.")


def _run_menu(title: str, actions: dict[str, tuple[str, Callable[[], None]]]) -> None:
    while True:
        print(f"\n{'=' * 15} {title} {'=' * 15}")
        for key, (label, _) in actions.items():
            print(f"{key:>2}. {label}")
        print(" L. Logout")
        choice = input("Choose an option: ").strip().lower()
        if choice == "l":
            print("Logged out.")
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid option.")
            _pause()
            continue
        try:
            action[1]()
        except (ValidationError, AuthenticationError, DatabaseConnectionError) as exc:
            print(f"Error: {exc}")
        except mysql.connector.Error:
            print(
                "A database operation failed. Check the database settings and schema."
            )
        except (ValueError, EOFError, KeyboardInterrupt):
            print("Invalid input or operation cancelled.")
        _pause()


def _setup_first_admin() -> None:
    print("\nNo admin account exists. Create the first admin account.")
    name = input("Admin name: ")
    role = input("Job role [Administrator]: ") or "Administrator"
    email = input("Admin email: ")
    password = getpass("Admin password (minimum 8 characters): ")
    confirm = getpass("Confirm password: ")
    if password != confirm:
        raise ValidationError("Passwords do not match.")
    admin_id = services.create_first_admin(name, role, email, password)
    print(f"First admin created with employee ID {admin_id}. Please log in.")


def main() -> None:
    """Ensure the schema exists, then provide login and role-based sections."""
    print("=" * 48)
    print("       EMPLOYEE TASK TRACKING SYSTEM")
    print("=" * 48)
    try:
        ensure_schema()
        if services.get_admin_count() == 0:
            _setup_first_admin()
        while True:
            print("\n1. Login\n0. Exit")
            choice = input("Choose an option: ").strip()
            if choice == "0":
                print("Goodbye.")
                return
            if choice != "1":
                print("Invalid option.")
                continue
            try:
                email = input("Email: ")
                password = getpass("Password: ")
                user = services.authenticate(email, password)
                print(f"Welcome, {user['name']} ({user['account_role']}).")
                if user["account_role"] == "admin":
                    _admin_menu(user)
                else:
                    _employee_menu(user)
            except (AuthenticationError, ValidationError) as exc:
                print(f"Login failed: {exc}")
    except (
        ConfigurationError,
        DatabaseConnectionError,
        mysql.connector.Error,
        ValueError,
        RuntimeError,
        ValidationError,
    ) as exc:
        print(f"Could not start the application: {exc}")
        print("Check MySQL service and DB_* settings in .env.")
    except (EOFError, KeyboardInterrupt):
        print("Setup or login cancelled.")
