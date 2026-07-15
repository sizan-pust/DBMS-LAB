-- q5: Find the department names that have an average instructor salary greater than $70,000.
--query:
SELECT dept_name from instructor GROUP BY dept_name having avg(salary) > 70000;