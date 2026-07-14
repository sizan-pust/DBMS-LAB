--Q6: Find the names of all instructors who do not belong to the 'Comp. Sci.' department.
--Query:
SELECT name FROM instructor WHERE dept_name<>'Comp. Sci.';