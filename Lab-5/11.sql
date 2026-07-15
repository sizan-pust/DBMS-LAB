-- q11: Find the names of all students who have taken the course 'CS-101'.
--query:
SELECT name from student where ID IN (SELECT ID FROM takes where course_id = 'CS-101' );