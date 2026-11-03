from datetime import date
from getpass import getpass
import os
import re
import mysql.connector
from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError, VerifyMismatchError
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "employeetaskmanagmentsystem"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "connection_timeout": 10,
}
STATUSES = ("Pending", "In Progress", "Completed", "On Hold")
PRIORITIES = ("Low", "Medium", "High", "Critical")
PASSWORD_HASHER = PasswordHasher()
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class AppError(Exception):
    """Expected user-facing application error."""


def connect():
    
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as exc:
        raise AppError(
            "Cannot connect to MySQL. Check that MySQL is running and DB_* values in .env are correct."
        ) from exc


def setup_database():
    """Create the four required tables and add login fields to older employee tables."""
    db = connect()
    cur = db.cursor()
    try:
        cur.execute("""CREATE TABLE IF NOT EXISTS employees (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL, role VARCHAR(100) NOT NULL,
            email VARCHAR(200) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NULL,
            account_role VARCHAR(20) NOT NULL DEFAULT 'employee',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
        cur.execute("""CREATE TABLE IF NOT EXISTS `task` (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(200) NOT NULL, description TEXT,
            priority VARCHAR(20) NOT NULL DEFAULT 'Medium',
            due_date DATE NULL, status VARCHAR(20) NOT NULL DEFAULT 'Pending',
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
        cur.execute("""CREATE TABLE IF NOT EXISTS assigned_tasks (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            task_id INT NOT NULL, employee_id INT NOT NULL,
            assigned_date DATE NOT NULL,
            UNIQUE KEY uq_assigned_task_employee (task_id, employee_id),
            CONSTRAINT fk_assigned_task FOREIGN KEY (task_id) REFERENCES `task`(id) ON DELETE CASCADE,
            CONSTRAINT fk_assigned_employee FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
        cur.execute("""CREATE TABLE IF NOT EXISTS comments (
            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
            task_id INT NOT NULL, employee_id INT NOT NULL,
            comment TEXT NOT NULL,
            created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_comment_task FOREIGN KEY (task_id) REFERENCES `task`(id) ON DELETE CASCADE,
            CONSTRAINT fk_comment_employee FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4""")
        # Add login columns if the database was created by an earlier project version.
        cur.execute("SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=%s AND TABLE_NAME='employees'", (DB_CONFIG["database"],))
        columns = {row[0] for row in cur.fetchall()}
        if "password_hash" not in columns:
            cur.execute("ALTER TABLE employees ADD COLUMN password_hash VARCHAR(255) NULL")
        if "account_role" not in columns:
            cur.execute("ALTER TABLE employees ADD COLUMN account_role VARCHAR(20) NOT NULL DEFAULT 'employee'")
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        cur.close()
        db.close()


def ask_id(prompt):
    """Read a positive integer ID from the console."""
    try:
        value = int(input(prompt).strip())
        if value < 1:
            raise ValueError
        return value
    except ValueError as exc:
        raise AppError("Enter a valid positive numeric ID.") from exc


def required(value, label, max_length=None):
    """Validate required text fields."""
    value = value.strip()
    if not value:
        raise AppError(f"{label} is required.")
    if max_length and len(value) > max_length:
        raise AppError(f"{label} must be no longer than {max_length} characters.")
    return value


def parse_date(value):
    """Parse an optional ISO date, YYYY-MM-DD."""
    if not value.strip():
        return None
    try:
        return date.fromisoformat(value.strip())
    except ValueError as exc:
        raise AppError("Date must use YYYY-MM-DD format.") from exc


def rows(sql, params=()):
    """Run a read query and return dictionary records."""
    db = connect()
    cur = db.cursor(dictionary=True)
    try:
        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        cur.close()
        db.close()


def execute(sql, params=(), return_id=False):
    """Run one write query with a transaction and optional inserted ID."""
    db = connect()
    cur = db.cursor()
    try:
        cur.execute(sql, params)
        result = cur.lastrowid if return_id else cur.rowcount
        db.commit()
        return result
    except Exception:
        db.rollback()
        raise
    finally:
        cur.close()
        db.close()


def print_table(records, fields):
    """Print records in a readable console table."""
    if not records:
        print("No records found.")
        return
    values = [["-" if r.get(key) is None else str(r.get(key)) for key, _ in fields] for r in records]
    widths = [max(len(label), *(len(row[i]) for row in values)) for i, (_, label) in enumerate(fields)]
    print(" | ".join(label.ljust(widths[i]) for i, (_, label) in enumerate(fields)))
    print("-+-".join("-" * width for width in widths))
    for record in values:
        print(" | ".join(value.ljust(widths[i]) for i, value in enumerate(record)))


EMPLOYEE_FIELDS = [("id", "ID"), ("name", "Name"), ("role", "Role"), ("email", "Email")]
TASK_FIELDS = [("id", "ID"), ("title", "Title"), ("priority", "Priority"), ("status", "Status"), ("due_date", "Due date"), ("assignees", "Assigned employees")]


def employee_list():
    """List employees without exposing password hashes."""
    print_table(rows("SELECT id,name,role,email FROM employees ORDER BY id"), EMPLOYEE_FIELDS)


def add_employee(account_role="employee"):
    """Add an employee or admin account with an Argon2-hashed password."""
    name = required(input("Name: "), "Name", 150)
    role = required(input("Job role: "), "Role", 100)
    email = required(input("Email: "), "Email", 200).lower()
    if not EMAIL_RE.fullmatch(email):
        raise AppError("Enter a valid email address.")
    password = getpass("Login password (minimum 8 characters): ")
    if len(password) < 8:
        raise AppError("Password must be at least 8 characters long.")
    if rows("SELECT id FROM employees WHERE LOWER(email)=%s", (email,)):
        raise AppError("That email address is already registered.")
    password_hash = PASSWORD_HASHER.hash(password)
    new_id = execute("INSERT INTO employees(name,role,email,password_hash,account_role,created_at) VALUES(%s,%s,%s,%s,%s,NOW())", (name, role, email, password_hash, account_role), True)
    print(f"{account_role.title()} created. Employee ID: {new_id}")


def update_employee():
    """Update employee name, job role, and email."""
    employee_id = ask_id("Employee ID: ")
    found = rows("SELECT id,name,role,email FROM employees WHERE id=%s", (employee_id,))
    if not found:
        raise AppError("Employee not found.")
    old = found[0]
    name = input(f"Name [{old['name']}]: ").strip() or old["name"]
    role = input(f"Role [{old['role']}]: ").strip() or old["role"]
    email = input(f"Email [{old['email']}]: ").strip().lower() or old["email"]
    if not EMAIL_RE.fullmatch(email):
        raise AppError("Enter a valid email address.")
    if rows("SELECT id FROM employees WHERE LOWER(email)=%s AND id<>%s", (email, employee_id)):
        raise AppError("Another employee already uses this email.")
    execute("UPDATE employees SET name=%s,role=%s,email=%s WHERE id=%s", (name, role, email, employee_id))
    print("Employee updated.")


def delete_employee(current_user):
    """Delete an employee after confirmation; protect the current/last admin."""
    employee_id = ask_id("Employee ID to delete: ")
    if employee_id == current_user["id"]:
        raise AppError("You cannot delete the account currently signed in.")
    found = rows("SELECT id,name,account_role FROM employees WHERE id=%s", (employee_id,))
    if not found:
        raise AppError("Employee not found.")
    if found[0]["account_role"] == "admin" and len(rows("SELECT id FROM employees WHERE account_role='admin'")) <= 1:
        raise AppError("Cannot delete the last admin account.")
    if input(f"Delete {found[0]['name']} and their assignments/comments? (yes/no): ").lower() != "yes":
        print("Cancelled.")
        return
    execute("DELETE FROM employees WHERE id=%s", (employee_id,))
    print("Employee deleted.")


def create_task():
    """Create a task using only the specified priority values."""
    title = required(input("Title: "), "Title", 200)
    description = input("Description: ").strip()
    print("Priorities:", ", ".join(PRIORITIES))
    priority = (input("Priority [Medium]: ").strip() or "Medium").title()
    if priority not in PRIORITIES:
        raise AppError("Choose Low, Medium, High, or Critical.")
    due_date = parse_date(input("Due date YYYY-MM-DD (blank if none): "))
    task_id = execute("INSERT INTO `task`(title,description,priority,due_date,status,created_at) VALUES(%s,%s,%s,%s,'Pending',NOW())", (title, description or None, priority, due_date), True)
    print(f"Task created. Task ID: {task_id}")


def task_records(status="", priority="", employee_id=None, keyword="", due_from="", due_to="", completed=False):
    """View/search/filter tasks by status, priority, employee, text, or due-date range."""
    sql = ("SELECT t.id,t.title,t.description,t.priority,t.due_date,t.status,t.created_at, "
           "GROUP_CONCAT(DISTINCT e.name ORDER BY e.name SEPARATOR ', ') AS assignees "
           "FROM `task` t LEFT JOIN assigned_tasks a ON a.task_id=t.id "
           "LEFT JOIN employees e ON e.id=a.employee_id")
    conditions, params = [], []
    if status:
        status = status.strip().title()
        if status not in STATUSES:
            raise AppError("Invalid status. Use: " + ", ".join(STATUSES))
        conditions.append("t.status=%s"); params.append(status)
    if priority:
        priority = priority.strip().title()
        if priority not in PRIORITIES:
            raise AppError("Invalid priority. Use: " + ", ".join(PRIORITIES))
        conditions.append("t.priority=%s"); params.append(priority)
    if employee_id:
        conditions.append("a.employee_id=%s"); params.append(employee_id)
    if keyword.strip():
        conditions.append("(t.title LIKE %s OR t.description LIKE %s OR e.name LIKE %s)")
        pattern = "%" + keyword.strip() + "%"; params.extend([pattern, pattern, pattern])
    if due_from.strip():
        conditions.append("t.due_date >= %s"); params.append(parse_date(due_from))
    if due_to.strip():
        conditions.append("t.due_date <= %s"); params.append(parse_date(due_to))
    if completed:
        conditions.append("t.status='Completed'")
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " GROUP BY t.id ORDER BY t.id"
    return rows(sql, tuple(params))


def view_tasks(employee_id=None, completed=False):
    """View tasks, optionally limited to one employee or completed tasks."""
    status = input(f"Status {STATUSES} (blank for all): ").strip() if input("Filter by status? (y/n): ").lower() == "y" else ""
    priority = input(f"Priority {PRIORITIES} (blank for all): ").strip() if input("Filter by priority? (y/n): ").lower() == "y" else ""
    keyword = input("Search title/description/employee (blank for none): ").strip()
    due_from = input("Due on/after YYYY-MM-DD (blank for none): ").strip()
    due_to = input("Due on/before YYYY-MM-DD (blank for none): ").strip()
    print_table(task_records(status, priority, employee_id, keyword, due_from, due_to, completed), TASK_FIELDS)


def assign_task():
    """Assign a task to one employee; call again to assign another employee."""
    task_id, employee_id = ask_id("Task ID: "), ask_id("Employee ID: ")
    if not rows("SELECT id FROM `task` WHERE id=%s", (task_id,)):
        raise AppError("Task not found.")
    if not rows("SELECT id FROM employees WHERE id=%s", (employee_id,)):
        raise AppError("Employee not found.")
    if rows("SELECT id FROM assigned_tasks WHERE task_id=%s AND employee_id=%s", (task_id, employee_id)):
        raise AppError("That task is already assigned to this employee.")
    execute("INSERT INTO assigned_tasks(task_id,employee_id,assigned_date) VALUES(%s,%s,%s)", (task_id, employee_id, date.today()))
    print("Task assigned.")


def update_task():
    """Edit task title, description, priority, and due date."""
    task_id = ask_id("Task ID: ")
    found = rows("SELECT * FROM `task` WHERE id=%s", (task_id,))
    if not found:
        raise AppError("Task not found.")
    old = found[0]
    title = input(f"Title [{old['title']}]: ").strip() or old["title"]
    description = input(f"Description [{old['description'] or ''}]: ").strip() or (old["description"] or "")
    priority = (input(f"Priority {PRIORITIES} [{old['priority']}]: ").strip() or old["priority"]).title()
    if priority not in PRIORITIES:
        raise AppError("Invalid priority.")
    due = input(f"Due date [{old['due_date'] or ''}]: ").strip()
    due_date = parse_date(due) if due else old["due_date"]
    execute("UPDATE `task` SET title=%s,description=%s,priority=%s,due_date=%s WHERE id=%s", (title, description or None, priority, due_date, task_id))
    print("Task details updated.")


def delete_task():
    """Delete a task after explicit confirmation."""
    task_id = ask_id("Task ID: ")
    if not rows("SELECT id FROM `task` WHERE id=%s", (task_id,)):
        raise AppError("Task not found.")
    if input("Delete task and its assignments/comments? (yes/no): ").lower() != "yes":
        print("Cancelled."); return
    execute("DELETE FROM `task` WHERE id=%s", (task_id,))
    print("Task deleted.")


def update_task_status(employee_id=None):
    """Update task status; employees can update only their assigned tasks."""
    task_id = ask_id("Task ID: ")
    if employee_id and not rows("SELECT id FROM assigned_tasks WHERE task_id=%s AND employee_id=%s", (task_id, employee_id)):
        raise AppError("You can update only tasks assigned to you.")
    print("Statuses:", ", ".join(STATUSES))
    status = required(input("New status: "), "Status").title()
    if status not in STATUSES:
        raise AppError("Invalid status.")
    if not rows("SELECT id FROM `task` WHERE id=%s", (task_id,)):
        raise AppError("Task not found.")
    execute("UPDATE `task` SET status=%s WHERE id=%s", (status, task_id))
    print("Task status updated.")


def add_comment(current_user):
    """Add a comment to a task, respecting employee task assignments."""
    task_id = ask_id("Task ID: ")
    if current_user["account_role"] == "employee" and not rows("SELECT id FROM assigned_tasks WHERE task_id=%s AND employee_id=%s", (task_id, current_user["id"])):
        raise AppError("You can comment only on tasks assigned to you.")
    if not rows("SELECT id FROM `task` WHERE id=%s", (task_id,)):
        raise AppError("Task not found.")
    comment = required(input("Comment: "), "Comment")
    execute("INSERT INTO comments(task_id,employee_id,comment,created_at) VALUES(%s,%s,%s,NOW())", (task_id, current_user["id"], comment))
    print("Comment added.")


def view_comments(employee_id=None):
    """View task comment history."""
    task_id = ask_id("Task ID: ")
    if employee_id and not rows("SELECT id FROM assigned_tasks WHERE task_id=%s AND employee_id=%s", (task_id, employee_id)):
        raise AppError("You can view comments only for tasks assigned to you.")
    print_table(rows("SELECT c.id,e.name AS employee_name,c.comment,c.created_at FROM comments c JOIN employees e ON e.id=c.employee_id WHERE c.task_id=%s ORDER BY c.created_at,c.id", (task_id,)), [("id", "ID"), ("employee_name", "Employee"), ("comment", "Comment"), ("created_at", "Created at")])


def profile(user):
    """View/update the signed-in employee profile and password."""
    current = rows("SELECT id,name,role,email FROM employees WHERE id=%s", (user["id"],))
    print_table(current, EMPLOYEE_FIELDS)
    if input("Update profile? (y/n): ").lower() == "y":
        old = current[0]
        name = input(f"Name [{old['name']}]: ").strip() or old["name"]
        role = input(f"Role [{old['role']}]: ").strip() or old["role"]
        email = input(f"Email [{old['email']}]: ").strip().lower() or old["email"]
        if not EMAIL_RE.fullmatch(email):
            raise AppError("Enter a valid email address.")
        if rows("SELECT id FROM employees WHERE LOWER(email)=%s AND id<>%s", (email, user["id"])):
            raise AppError("Another employee already uses that email.")
        execute("UPDATE employees SET name=%s,role=%s,email=%s WHERE id=%s", (name, role, email, user["id"]))
        user.update(name=name, role=role, email=email)
        print("Profile updated.")
    if input("Change password? (y/n): ").lower() == "y":
        password = getpass("New password (minimum 8 characters): ")
        if len(password) < 8 or password != getpass("Confirm password: "):
            raise AppError("Passwords must be at least 8 characters and match.")
        execute("UPDATE employees SET password_hash=%s WHERE id=%s", (PASSWORD_HASHER.hash(password), user["id"]))
        print("Password updated.")


def report():
    """Display task totals, statuses, overdue tasks, and employee performance."""
    totals = rows("SELECT COUNT(*) AS total FROM `task`")[0]["total"]
    employees = rows("SELECT COUNT(*) AS total FROM employees")[0]["total"]
    counts = {r["status"]: r["total"] for r in rows("SELECT status,COUNT(*) AS total FROM `task` GROUP BY status")}
    overdue = rows("SELECT COUNT(*) AS total FROM `task` WHERE due_date<CURDATE() AND status<>'Completed'")[0]["total"]
    upcoming = rows("SELECT COUNT(*) AS total FROM `task` WHERE due_date BETWEEN CURDATE() AND DATE_ADD(CURDATE(),INTERVAL 7 DAY) AND status<>'Completed'")[0]["total"]
    print("\n========== DASHBOARD / REPORTS ==========")
    print(f"Employees: {employees} | Tasks: {totals} | Completed: {counts.get('Completed', 0)} | Pending: {counts.get('Pending', 0)}")
    print(f"Overdue tasks: {overdue} | Due within 7 days: {upcoming}")
    print("\nStatus breakdown:")
    for status in STATUSES:
        print(f"  {status}: {counts.get(status, 0)}")
    print("\nEmployee performance:")
    print_table(rows("SELECT e.id,e.name,COUNT(DISTINCT a.task_id) AS assigned_tasks,COUNT(DISTINCT CASE WHEN t.status='Completed' THEN t.id END) AS completed_tasks FROM employees e LEFT JOIN assigned_tasks a ON a.employee_id=e.id LEFT JOIN `task` t ON t.id=a.task_id GROUP BY e.id ORDER BY e.name"), [("id", "ID"), ("name", "Employee"), ("assigned_tasks", "Assigned"), ("completed_tasks", "Completed")])


def authenticate():
    """Authenticate email/password; never display or store plain-text passwords."""
    email = required(input("Email: "), "Email").lower()
    password = getpass("Password: ")
    user_rows = rows("SELECT id,name,role,email,password_hash,account_role FROM employees WHERE LOWER(email)=%s", (email,))
    if not user_rows or not user_rows[0]["password_hash"]:
        raise AppError("Invalid email or password. Ask an admin to set your login password.")
    user = user_rows[0]
    try:
        PASSWORD_HASHER.verify(user["password_hash"], password)
    except (VerifyMismatchError, VerificationError, InvalidHashError) as exc:
        raise AppError("Invalid email or password.") from exc
    user.pop("password_hash", None)
    return user


def first_admin_setup():
    """Create the first admin, or promote a matching existing employee record."""
    if rows("SELECT id FROM employees WHERE account_role='admin' LIMIT 1"):
        return
    print("\nNo admin account exists. Create the first admin account.")
    name = required(input("Admin name: "), "Name", 150)
    role = input("Job role [Administrator]: ").strip() or "Administrator"
    email = required(input("Admin email: "), "Email", 200).lower()
    if not EMAIL_RE.fullmatch(email):
        raise AppError("Enter a valid email address.")
    password = getpass("Admin password (minimum 8 characters): ")
    if len(password) < 8 or password != getpass("Confirm password: "):
        raise AppError("Passwords must be at least 8 characters and match.")
    existing = rows("SELECT id FROM employees WHERE LOWER(email)=%s", (email,))
    hashed = PASSWORD_HASHER.hash(password)
    if existing:
        execute("UPDATE employees SET name=%s,role=%s,password_hash=%s,account_role='admin' WHERE id=%s", (name, role, hashed, existing[0]["id"]))
        print("Existing employee account promoted to admin. Existing tasks were preserved.")
    else:
        execute("INSERT INTO employees(name,role,email,password_hash,account_role,created_at) VALUES(%s,%s,%s,%s,'admin',NOW())", (name, role, email, hashed))
        print("First admin account created.")


def employee_menu(user):
    """Display only the employee features shown in the specification."""
    actions = {
        "1": ("Dashboard / my progress", lambda: report_employee(user)),
        "2": ("My tasks / filter", lambda: view_tasks(employee_id=user["id"])),
        "3": ("Task details and comments", lambda: view_comments(user["id"])),
        "4": ("Update task status", lambda: update_task_status(user["id"])),
        "5": ("Add comment", lambda: add_comment(user)),
        "6": ("View completed tasks", lambda: print_table(task_records(employee_id=user["id"], completed=True), TASK_FIELDS)),
        "7": ("Profile", lambda: profile(user)),
    }
    run_menu("EMPLOYEE SECTION", actions)


def report_employee(user):
    """Show the signed-in employee's task progress."""
    assigned = task_records(employee_id=user["id"])
    completed = sum(task["status"] == "Completed" for task in assigned)
    overdue = sum(task["due_date"] and task["due_date"] < date.today() and task["status"] != "Completed" for task in assigned)
    print(f"My tasks: {len(assigned)} | Completed: {completed} | Remaining: {len(assigned)-completed} | Overdue: {overdue}")
    print_table(assigned, TASK_FIELDS)


def admin_menu(user):
    """Display admin actions from the supplied project specification."""
    actions = {
        "1": ("Dashboard", report),
        "2": ("View employee list", employee_list),
        "3": ("Add employee", add_employee),
        "4": ("Update employee", update_employee),
        "5": ("Delete employee", lambda: delete_employee(user)),
        "6": ("Create task", create_task),
        "7": ("Assign task", assign_task),
        "8": ("View all tasks", lambda: print_table(task_records(), TASK_FIELDS)),
        "9": ("Search / filter tasks", view_tasks),
        "10": ("Update task details", update_task),
        "11": ("Delete task", delete_task),
        "12": ("Update task status", update_task_status),
        "13": ("Add comment", lambda: add_comment(user)),
        "14": ("View comments", view_comments),
        "15": ("Reports and analytics", report),
    }
    run_menu("ADMIN SECTION", actions)


def run_menu(title, actions):
    """Run a menu until the user logs out."""
    while True:
        print(f"\n========== {title} ==========")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        print("L. Logout")
        choice = input("Choose an option: ").strip().lower()
        if choice == "l":
            print("Logged out.")
            return
        if choice not in actions:
            print("Invalid option.")
            continue
        try:
            actions[choice][1]()
        except AppError as exc:
            print("Error:", exc)
        except mysql.connector.Error as exc:
            print("Database operation failed:", exc.msg)
        except (ValueError, EOFError, KeyboardInterrupt):
            print("Invalid input or operation cancelled.")


def main():
    """Set up MySQL and run first-admin setup, login, and role-specific menus."""
    print("=" * 48 + "\n       EMPLOYEE TASK TRACKING SYSTEM\n" + "=" * 48)
    try:
        setup_database()
        first_admin_setup()
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
                user = authenticate()
                print(f"Welcome, {user['name']} ({user['account_role']}).")
                if user["account_role"] == "admin":
                    admin_menu(user)
                else:
                    employee_menu(user)
            except AppError as exc:
                print("Login failed:", exc)
    except (AppError, mysql.connector.Error, ValueError, EOFError, KeyboardInterrupt) as exc:
        print("Could not start application:", exc)
        print("Check MySQL and the DB_* values in .env.")


if __name__ == "__main__":
    main()
