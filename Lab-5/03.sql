-- q3: Find the count of instructors in each department.
--query:
select dept_name, count(*) as instructor_count from instructor group by dept_name;