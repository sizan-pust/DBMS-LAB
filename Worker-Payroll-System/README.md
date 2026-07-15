# Worker Payroll Management System

A simple Python Tkinter desktop application connected to MySQL. It demonstrates
worker CRUD operations and basic monthly payroll processing.

## Project Structure

```text
Worker-Payroll-System/
├── main.py
├── db.py
├── ui.py
├── database.sql
├── requirements.txt
└── README.md
```

## Features

- MySQL database connection
- Add new worker
- View and search worker records
- Update worker information
- Delete worker
- Calculate salary using absent days, overtime or bonus, and deductions
- Save payroll records
- View worker payroll history
- Primary key, foreign key, unique constraint, and JOIN demonstration

## Payroll Formula

```text
Absence Deduction = (Base Salary / 30) × Absent Days

Net Salary =
Base Salary
+ Overtime or Bonus
- Absence Deduction
- Other Deduction
```

## Database Tables

### workers

Stores worker name, work section, job role, contact information, and base salary.

### payroll

Stores monthly payroll information. `payroll.worker_id` references
`workers.worker_id`.

## Setup

### 1. Run the SQL file

Open MySQL Workbench and run the complete `database.sql` file.

### 2. Set your MySQL password

Open `db.py` and replace:

```python
"password": "YOUR_MYSQL_PASSWORD",
```

with your local MySQL root password.

When MySQL has no password:

```python
"password": "",
```

Before uploading to GitHub, change the password back to
`YOUR_MYSQL_PASSWORD`.

### 3. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

When PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Install the dependency

```powershell
python -m pip install -r requirements.txt
```

### 5. Run the application

```powershell
python main.py
```

## CRUD Demonstration

- **Create:** Enter worker information and click Add.
- **Read:** View or search workers in the table.
- **Update:** Select a worker, change information, and click Update.
- **Delete:** Select a worker and click Delete.
- **Payroll:** Select a worker, calculate salary, and save the payroll record.

## Suggested Demonstration to the Professor

1. Show the `workers` and `payroll` tables in MySQL Workbench.
2. Show the MySQL connection in `db.py`.
3. Run `python main.py`.
4. Add a worker to demonstrate CREATE.
5. Search the worker to demonstrate READ.
6. Change the worker's section or salary to demonstrate UPDATE.
7. Calculate and save a monthly payroll.
8. Delete a test worker to demonstrate DELETE.
9. Refresh MySQL Workbench and show the database changes.
