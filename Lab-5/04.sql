-- q4: Find the average salary of instructors in each department and rename the result column to avg_salary.
--query:
select dept_name, avg(salary) as avg_salary from instructor group by dept_name;