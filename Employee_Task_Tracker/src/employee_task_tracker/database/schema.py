"""Create and safely upgrade the application's MySQL schema."""

from typing import Any

from employee_task_tracker.database.connection import get_connection

CREATE_STATEMENTS = (
    """
    CREATE TABLE IF NOT EXISTS employees (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(150) NOT NULL,
        role VARCHAR(100) NOT NULL,
        email VARCHAR(200) NOT NULL,
        password_hash VARCHAR(255) NULL,
        account_role VARCHAR(20) NOT NULL DEFAULT 'employee',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        UNIQUE KEY uq_employees_email (email)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS `task` (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        priority VARCHAR(20) NOT NULL DEFAULT 'Medium',
        due_date DATE,
        status VARCHAR(20) NOT NULL DEFAULT 'Pending',
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS assigned_tasks (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        task_id INT NOT NULL,
        employee_id INT NOT NULL,
        assigned_date DATE NOT NULL DEFAULT (CURRENT_DATE),
        UNIQUE KEY uq_assigned_task_employee (task_id, employee_id),
        CONSTRAINT fk_assigned_tasks_employee FOREIGN KEY (employee_id)
            REFERENCES employees (id) ON DELETE CASCADE,
        CONSTRAINT fk_assigned_tasks_task FOREIGN KEY (task_id)
            REFERENCES `task` (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
    """
    CREATE TABLE IF NOT EXISTS comments (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        task_id INT NOT NULL,
        employee_id INT NOT NULL,
        comment TEXT NOT NULL,
        created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT fk_comments_employee FOREIGN KEY (employee_id)
            REFERENCES employees (id) ON DELETE CASCADE,
        CONSTRAINT fk_comments_task FOREIGN KEY (task_id)
            REFERENCES `task` (id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """,
)

ID_MIGRATIONS = (
    "ALTER TABLE employees MODIFY id INT NOT NULL AUTO_INCREMENT",
    "ALTER TABLE `task` MODIFY id INT NOT NULL AUTO_INCREMENT",
    "ALTER TABLE assigned_tasks MODIFY id INT NOT NULL AUTO_INCREMENT",
    "ALTER TABLE comments MODIFY id INT NOT NULL AUTO_INCREMENT",
)


def _quote_identifier(value: str) -> str:
    """Quote an identifier obtained from MySQL metadata."""
    return "`" + value.replace("`", "``") + "`"


def _ids_need_migration(cursor: Any, database: str) -> bool:
    """Return whether one or more existing ID columns lack AUTO_INCREMENT."""
    cursor.execute(
        "SELECT TABLE_NAME, EXTRA FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s "
        "AND TABLE_NAME IN ('employees', 'task', 'assigned_tasks', 'comments') "
        "AND COLUMN_NAME = 'id'",
        (database,),
    )
    rows = cursor.fetchall()
    return len(rows) < 4 or any("auto_increment" not in row[1].lower() for row in rows)


def _foreign_keys(cursor: Any, database: str) -> list[dict[str, str]]:
    """Read foreign keys that prevent the parent IDs from being altered."""
    cursor.execute(
        "SELECT k.TABLE_NAME, k.CONSTRAINT_NAME, k.COLUMN_NAME, "
        "k.REFERENCED_TABLE_NAME, k.REFERENCED_COLUMN_NAME, "
        "r.DELETE_RULE, r.UPDATE_RULE "
        "FROM information_schema.KEY_COLUMN_USAGE k "
        "JOIN information_schema.REFERENTIAL_CONSTRAINTS r "
        "ON r.CONSTRAINT_SCHEMA = k.CONSTRAINT_SCHEMA "
        "AND r.TABLE_NAME = k.TABLE_NAME "
        "AND r.CONSTRAINT_NAME = k.CONSTRAINT_NAME "
        "WHERE k.CONSTRAINT_SCHEMA = %s "
        "AND k.REFERENCED_TABLE_NAME IN ('employees', 'task') "
        "AND k.TABLE_NAME IN ('assigned_tasks', 'comments')",
        (database,),
    )
    names = (
        "table_name",
        "constraint_name",
        "column_name",
        "referenced_table_name",
        "referenced_column_name",
        "delete_rule",
        "update_rule",
    )
    return [dict(zip(names, row, strict=True)) for row in cursor.fetchall()]


def _ensure_employee_auth_columns(cursor: Any, database: str) -> None:
    """Add login columns to an existing employees table without dropping data."""
    cursor.execute(
        "SELECT COLUMN_NAME FROM information_schema.COLUMNS "
        "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'employees'",
        (database,),
    )
    existing = {row[0] for row in cursor.fetchall()}
    if "password_hash" not in existing:
        cursor.execute(
            "ALTER TABLE employees ADD COLUMN password_hash VARCHAR(255) NULL"
        )
    if "account_role" not in existing:
        cursor.execute(
            "ALTER TABLE employees ADD COLUMN account_role "
            "VARCHAR(20) NOT NULL DEFAULT 'employee'"
        )


def ensure_schema() -> None:
    """Create missing tables and perform additive, non-destructive migrations."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT DATABASE()")
        database = cursor.fetchone()[0]
        if not database:
            raise RuntimeError("DB_NAME must select a database before schema setup.")

        for statement in CREATE_STATEMENTS:
            cursor.execute(statement)
        _ensure_employee_auth_columns(cursor, database)

        if _ids_need_migration(cursor, database):
            # Existing starter tables have foreign keys without AUTO_INCREMENT IDs.
            # Temporarily remove these constraints, update ID definitions, then
            # restore their original names and referential actions.
            foreign_keys = _foreign_keys(cursor, database)
            for foreign_key in foreign_keys:
                cursor.execute(
                    f"ALTER TABLE {_quote_identifier(foreign_key['table_name'])} "
                    "DROP FOREIGN KEY "
                    f"{_quote_identifier(foreign_key['constraint_name'])}"
                )
            for statement in ID_MIGRATIONS:
                cursor.execute(statement)
            for foreign_key in foreign_keys:
                cursor.execute(
                    f"ALTER TABLE {_quote_identifier(foreign_key['table_name'])} "
                    "ADD CONSTRAINT "
                    f"{_quote_identifier(foreign_key['constraint_name'])} "
                    f"FOREIGN KEY ({_quote_identifier(foreign_key['column_name'])}) "
                    "REFERENCES "
                    f"{_quote_identifier(foreign_key['referenced_table_name'])} "
                    f"({_quote_identifier(foreign_key['referenced_column_name'])}) "
                    f"ON DELETE {foreign_key['delete_rule']} "
                    f"ON UPDATE {foreign_key['update_rule']}"
                )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
