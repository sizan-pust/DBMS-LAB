--Q7: Find the instructor's name, department name, and that department's budget.
--Query:
SELECT instructor.name, instructor.dept_name, department.budget FROM instructor, department
WHERE instructor.dept_name = department.dept_name;