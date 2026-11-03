"""Manage connections to the MySQL database."""

import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract

from employee_task_tracker.config import load_config
from employee_task_tracker.exceptions import DatabaseConnectionError


def get_connection() -> MySQLConnectionAbstract:
    """Create and return a MySQL database connection.

    Raises:
        DatabaseConnectionError: If MySQL cannot establish a connection.
        ValueError: If the application configuration is invalid.
    """
    # Load and validate database settings.
    settings = load_config()

    try:
        # Establish the connection using validated settings.
        connection = mysql.connector.connect(
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
            user=settings.db_user,
            password=settings.db_password,
            connection_timeout=10,
            autocommit=False,
        )

        return connection

    except mysql.connector.Error as exc:
        # Avoid exposing database details in the error message.
        raise DatabaseConnectionError(
            "Unable to connect to the database. "
            "Check that MySQL is running and the DB_* settings are correct."
        ) from exc
