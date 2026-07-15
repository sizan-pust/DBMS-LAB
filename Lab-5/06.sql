-- q6: Find the course_id of courses that were offered in Fall 2024 and in Spring 2025.
--query:
SELECT course_id FROM section WHERE semester = 'Fall' and year = 2024
INTERSECT
SELECT course_id from section where semester = 'Spring' and year = 2025;