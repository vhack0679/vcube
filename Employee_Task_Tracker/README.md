# Employee Task Tracking System

A Python 3.11+ CLI application using MySQL, implementing the requirements from the supplied Employee Task Tracking System specification image.

## Admin section

- Dashboard totals for tasks, completed and pending tasks, overdue tasks, and employee performance.
- Manage employees: add, list, update, delete.
- Create tasks with title, description, priority, and due date.
- Assign tasks to employees.
- View all tasks; search/filter by status, priority, employee, title, and description.
- Update/delete task details.
- Add/view task comments.
- Reports and analytics.
- Set/reset employee login passwords.
- Logout.

## Employee section

- Dashboard showing assigned, completed, and remaining tasks.
- View assigned tasks and details.
- Filter tasks by status/priority.
- Update status of assigned tasks.
- Add comments to assigned tasks and view comment history.
- View completed tasks.
- View/update profile and change password.
- Logout.

## Exact choices from the specification

- Status values: `Pending`, `In Progress`, `Completed`, `On Hold`.
- Priority values: `Low`, `Medium`, `High`, `Critical`.
- Tables: `employees`, `task`, `assigned_tasks`, `comments`.
- Technologies: Python 3, MySQL, MySQL Connector, CLI.

## Windows setup

1. Start MySQL Server and confirm `.env` contains the correct local `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` values. Do not share or commit `.env`.
2. From this project folder, optionally create and activate a virtual environment, then install dependencies:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -e ".[dev]"
   ```

3. Launch:

   ```powershell
   python -m employee_task_tracker
   ```

4. On first launch, create the initial admin account. If you use the email of an existing employee, that employee record is promoted to admin and gets the password you choose; existing tasks and other records are preserved. Otherwise, a new admin employee record is created. Sign in as admin, add employee accounts, and set their passwords from the admin section.

The migration is additive: it adds login columns and enables generated IDs on existing tables; it does not drop tables or delete existing application records. Back up important data before schema changes.

## Tests and lint

```powershell
python -m pytest -q
python -m ruff check .
```

This is deliberately a console app, in line with the supplied requirement. It does not include AI prediction or unrelated features.
