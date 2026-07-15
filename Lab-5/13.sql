-- q13: Give a 5 percent salary increase to all instructors in the 'Comp. Sci.' department.
--query:
UPDATE instructor SET salary = salary * 1.05 WHERE dept_name = 'Comp. Sci.';