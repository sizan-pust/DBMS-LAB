from decimal import Decimal, ROUND_HALF_UP
from typing import Any
import mysql.connector
from mysql.connector import Error, IntegrityError
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "",
    "database": "worker_payroll_db",
}
def get_connection():
    """Create and return a MySQL database connection."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as error:
        raise ConnectionError(f"Could not connect to MySQL: {error}") from error
def test_connection() -> bool:
    """Test the MySQL connection."""
    connection = get_connection()
    try:
        return connection.is_connected()
    finally:
        connection.close()
def _fetch_all(query: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()
        connection.close()
def _fetch_one(query: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()
def _execute(query: str, params: tuple[Any, ...] = ()) -> int:
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(query, params)
        connection.commit()
        return cursor.lastrowid
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
def add_worker(
    full_name: str,
    work_section: str,
    job_role: str,
    phone: str,
    email: str | None,
    base_salary: float,
) -> int:
    query = """
        INSERT INTO workers
            (full_name, work_section, job_role, phone, email, base_salary)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        return _execute(
            query,
            (full_name, work_section, job_role, phone, email, base_salary),
        )
    except IntegrityError as error:
        if error.errno == 1062:
            raise ValueError("This email address is already used.") from error
        raise
def get_workers(keyword: str = "") -> list[dict[str, Any]]:
    if keyword.strip():
        search = f"%{keyword.strip()}%"
        return _fetch_all(
            """
            SELECT worker_id, full_name, work_section, job_role,
                   phone, email, base_salary
            FROM workers
            WHERE full_name LIKE %s
               OR work_section LIKE %s
               OR job_role LIKE %s
            ORDER BY worker_id DESC
            """,
            (search, search, search),
        )

    return _fetch_all(
        """
        SELECT worker_id, full_name, work_section, job_role,
               phone, email, base_salary
        FROM workers
        ORDER BY worker_id DESC
        """
    )
def get_worker(worker_id: int) -> dict[str, Any] | None:
    return _fetch_one(
        """
        SELECT worker_id, full_name, work_section, job_role,
               phone, email, base_salary
        FROM workers
        WHERE worker_id = %s
        """,
        (worker_id,),
    )
def update_worker(
    worker_id: int,
    full_name: str,
    work_section: str,
    job_role: str,
    phone: str,
    email: str | None,
    base_salary: float,
) -> None:
    query = """
        UPDATE workers
        SET full_name = %s,
            work_section = %s,
            job_role = %s,
            phone = %s,
            email = %s,
            base_salary = %s
        WHERE worker_id = %s
    """
    try:
        _execute(
            query,
            (
                full_name,
                work_section,
                job_role,
                phone,
                email,
                base_salary,
                worker_id,
            ),
        )
    except IntegrityError as error:
        if error.errno == 1062:
            raise ValueError("This email address is already used.") from error
        raise
def delete_worker(worker_id: int) -> None:
    _execute("DELETE FROM workers WHERE worker_id = %s", (worker_id,))
def calculate_payroll(
    worker_id: int,
    absent_days: int,
    overtime_bonus: float,
    other_deduction: float,
) -> dict[str, Any]:
    worker = get_worker(worker_id)
    if not worker:
        raise ValueError("Worker was not found.")

    if absent_days < 0 or absent_days > 30:
        raise ValueError("Absent days must be between 0 and 30.")

    if overtime_bonus < 0 or other_deduction < 0:
        raise ValueError("Bonus and deduction cannot be negative.")

    money = Decimal("0.01")
    base_salary = Decimal(str(worker["base_salary"]))
    bonus = Decimal(str(overtime_bonus))
    deduction = Decimal(str(other_deduction))

    absence_deduction = (
        (base_salary / Decimal("30")) * Decimal(absent_days)
    ).quantize(money, rounding=ROUND_HALF_UP)

    net_salary = (
        base_salary + bonus - absence_deduction - deduction
    ).quantize(money, rounding=ROUND_HALF_UP)

    if net_salary < 0:
        raise ValueError("Net salary cannot be negative.")

    return {
        "worker_id": worker_id,
        "worker_name": worker["full_name"],
        "base_salary": base_salary.quantize(money),
        "absent_days": absent_days,
        "overtime_bonus": bonus.quantize(money),
        "absence_deduction": absence_deduction,
        "other_deduction": deduction.quantize(money),
        "net_salary": net_salary,
    }
def save_payroll(
    worker_id: int,
    salary_month: str,
    absent_days: int,
    overtime_bonus: float,
    other_deduction: float,
) -> dict[str, Any]:
    result = calculate_payroll(
        worker_id,
        absent_days,
        overtime_bonus,
        other_deduction,
    )
    query = """
        INSERT INTO payroll
            (
                worker_id,
                salary_month,
                absent_days,
                overtime_bonus,
                absence_deduction,
                other_deduction,
                net_salary,
                payment_date
            )
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURDATE())
    """
    try:
        payroll_id = _execute(
            query,
            (
                worker_id,
                salary_month,
                absent_days,
                result["overtime_bonus"],
                result["absence_deduction"],
                result["other_deduction"],
                result["net_salary"],
            ),
        )
    except IntegrityError as error:
        if error.errno == 1062:
            raise ValueError(
                "Payroll for this worker and month already exists."
            ) from error
        raise

    result["payroll_id"] = payroll_id
    result["salary_month"] = salary_month
    return result
def get_payroll_history() -> list[dict[str, Any]]:
    return _fetch_all(
        """
        SELECT
            p.payroll_id,
            w.full_name,
            p.salary_month,
            w.base_salary,
            p.absent_days,
            p.overtime_bonus,
            p.absence_deduction,
            p.other_deduction,
            p.net_salary,
            p.payment_date
        FROM payroll AS p
        JOIN workers AS w
          ON p.worker_id = w.worker_id
        ORDER BY p.salary_month DESC, p.payroll_id DESC
        """
    )