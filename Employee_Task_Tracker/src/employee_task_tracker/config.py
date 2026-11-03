"""Application configuration management."""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from employee_task_tracker.exceptions import ConfigurationError

# Find the project root directory.
# config.py -> employee_task_tracker -> src -> project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """Store validated application configuration."""

    db_host: str
    db_port: int
    db_name: str
    db_user: str

    # Prevent the database password from appearing in repr(Settings(...)).
    db_password: str = field(repr=False)

    app_env: str = "development"
    log_level: str = "INFO"


def load_config() -> Settings:
    """Load and validate configuration from environment variables."""

    # Load the project's .env file.
    # Existing operating-system environment variables take precedence.
    env_file = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=env_file, override=False)

    # Read required database settings.
    required_variables = ("DB_HOST", "DB_NAME", "DB_USER")
    missing_variables = [
        name for name in required_variables if not os.getenv(name, "").strip()
    ]

    if missing_variables:
        missing = ", ".join(missing_variables)
        raise ConfigurationError(f"Missing required environment variable(s): {missing}")

    # Read and validate the database port.
    raw_port = os.getenv("DB_PORT", "3306")

    try:
        db_port = int(raw_port)
    except ValueError as exc:
        raise ValueError("DB_PORT must be a valid integer.") from exc

    if not 1 <= db_port <= 65535:
        raise ValueError("DB_PORT must be between 1 and 65535.")

    # Normalize and validate the application environment.
    app_env = os.getenv("APP_ENV", "development").strip().lower()
    allowed_environments = {"development", "testing", "production"}

    if app_env not in allowed_environments:
        raise ValueError("APP_ENV must be development, testing, or production.")

    # Normalize and validate the logging level.
    log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()
    allowed_log_levels = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }

    if log_level not in allowed_log_levels:
        raise ValueError("LOG_LEVEL must be DEBUG, INFO, WARNING, ERROR, or CRITICAL.")

    # An empty password may be allowed for local development,
    # but never allow it for production.
    db_password = os.getenv("DB_PASSWORD", "")

    if app_env == "production" and not db_password:
        raise ValueError("DB_PASSWORD must be configured in production.")

    # Return one validated configuration object.
    return Settings(
        db_host=os.environ["DB_HOST"].strip(),
        db_port=db_port,
        db_name=os.environ["DB_NAME"].strip(),
        db_user=os.environ["DB_USER"].strip(),
        db_password=db_password,
        app_env=app_env,
        log_level=log_level,
    )
