CREATE DATABASE IF NOT EXISTS worker_payroll_db;
USE worker_payroll_db;
DROP TABLE IF EXISTS payroll;
DROP TABLE IF EXISTS workers;
CREATE TABLE workers (
    worker_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    work_section VARCHAR(50) NOT NULL,
    job_role VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    base_salary DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    worker_id INT NOT NULL,
    salary_month CHAR(7) NOT NULL,
    absent_days INT NOT NULL DEFAULT 0,
    overtime_bonus DECIMAL(10,2) NOT NULL DEFAULT 0,
    absence_deduction DECIMAL(10,2) NOT NULL DEFAULT 0,
    other_deduction DECIMAL(10,2) NOT NULL DEFAULT 0,
    net_salary DECIMAL(10,2) NOT NULL,
    payment_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_payroll_worker
        FOREIGN KEY (worker_id)
        REFERENCES workers(worker_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_worker_salary_month
        UNIQUE (worker_id, salary_month),

    CONSTRAINT chk_absent_days
        CHECK (absent_days BETWEEN 0 AND 30)
);
INSERT INTO workers(full_name, work_section, job_role, phone, email, base_salary)
VALUES('Rahim Uddin', 'Production', 'Machine Operator', '01710000001', 'rahim@example.com', 28000.00),('Karim Mia', 'Packaging', 'Packing Worker',
'01710000002', 'karim@example.com', 24000.00),

('Salma Akter', 'Maintenance', 'Maintenance Technician',
     '01710000003', 'salma@example.com', 32000.00);
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
VALUES
    (1, '2026-06', 1, 2000.00, 933.33, 300.00, 28766.67, '2026-06-30'),
    (2, '2026-06', 0, 1500.00, 0.00, 200.00, 25300.00, '2026-06-30');
SELECT * FROM workers;
SELECT
    p.payroll_id,
    w.full_name AS worker_name,
    w.work_section,
    w.job_role,
    p.salary_month,
    w.base_salary,
    p.overtime_bonus,
    p.absence_deduction,
    p.other_deduction,
    p.net_salary,
    p.payment_date
FROM payroll AS p
JOIN workers AS w
  ON p.worker_id = w.worker_id
ORDER BY p.salary_month DESC, w.full_name;
