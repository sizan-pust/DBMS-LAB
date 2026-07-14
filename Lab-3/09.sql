--Q9: Find the names of students and the course IDs of the courses they have taken.
--Query:
SELECT student.name, takes.course_id FROM student, takes WHERE student.ID = takes.ID;