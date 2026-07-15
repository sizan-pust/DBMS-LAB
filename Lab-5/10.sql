-- q10: Find the names of all instructors whose salary is greater than at least one instructor in the 'Biology' department.
--query:
SELECT name FROM instructor WHERE salary >ANY(
SELECT salary FROM instructor WHERE dept_name = 'Biology');