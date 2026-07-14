--Q12: Find the names of all instructors who earn a higher salary than the instructor named 'Einstein'.
--Query:
SELECT name FROM instructor
WHERE salary > (SELECT salary FROM instructor WHERE name = 'Einstein');