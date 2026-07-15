-- q9: Find the names of all instructors who earn more than the average salary of all instructors.
--query: 
SELECT name FROM instructor WHERE salary > (SELECT AVG(salary)FROM instructor);