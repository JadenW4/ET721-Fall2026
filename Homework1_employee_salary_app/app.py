import os
from decimal import Decimal
from pathlib import Path

import mysql.connector
from flask import Flask, render_template, request

app = Flask(__name__)

# Set these environment variables in the terminal before running the app.
# Never put your real database password in a file that you upload to GitHub.
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "user": os.getenv("MYSQL_USER", "flaskuser"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "employee_data"),
    "connection_timeout": 5,
}

# Change this filename if you rename your HTML template.
TEMPLATE_NAME = "index_jadenwiltshire.html"


def get_connection():
    """Connect to MySQL. Called only when a form is submitted."""
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    result = None
    form_data = {
        "employee_name": "",
        "employee_id": "",
        "salary": "",
    }

    if request.method == "POST":
        form_data["employee_name"] = request.form.get("employee_name", "").strip()
        form_data["employee_id"] = request.form.get("employee_id", "").strip()
        form_data["salary"] = request.form.get("salary", "").strip()

        name = form_data["employee_name"]
        employee_id_text = form_data["employee_id"]
        salary_text = form_data["salary"]

        # Validate on the server; browser limits alone are not enough.
        if not name:
            error = "Please enter the employee name."
        elif len(name) > 50:
            error = "Employee name must be 50 characters or fewer."
        elif not employee_id_text.isdigit() or len(employee_id_text) > 2:
            error = "Employee ID must be a whole number with no more than two digits."
        elif not salary_text.isdigit() or len(salary_text) > 6:
            error = "Employee salary must be a whole number with no more than six digits."
        else:
            employee_id = int(employee_id_text)
            salary = int(salary_text)
            increased_salary = Decimal(salary) * Decimal("1.05")

            connection = None
            cursor = None
            try:
                connection = get_connection()
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO employee_salary (employee_name, employee_id, salary)
                    VALUES (%s, %s, %s)
                    """,
                    (name, employee_id, salary),
                )
                connection.commit()

                result = {
                    "employee_name": name,
                    "employee_id": employee_id,
                    "salary": salary,
                    "increased_salary": f"{increased_salary:.2f}",
                }
            except mysql.connector.Error as exc:
                if connection is not None:
                    try:
                        connection.rollback()
                    except mysql.connector.Error:
                        pass
                app.logger.exception("Database operation failed")
                error = (
                    "The form worked, but the employee could not be saved to MySQL. "
                    "Check that MySQL is running, the database/table exist, and the "
                    "MYSQL_* settings in your terminal are correct. "
                    f"Database message: {exc}"
                )
            finally:
                if cursor is not None:
                    cursor.close()
                if connection is not None and connection.is_connected():
                    connection.close()

    return render_template(
        TEMPLATE_NAME,
        form_data=form_data,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    # Use 0.0.0.0 so the app can be opened through a Codespaces forwarded port.
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
