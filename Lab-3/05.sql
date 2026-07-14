--Q5: Find the names and salaries of all instructors who are in the 'Finance' department and have a salary greater than $80,000.
--Query:
SELECT name, salary FROM instructor WHERE dept_name = 'Finance' AND salary>80000;