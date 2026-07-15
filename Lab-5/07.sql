-- q7: Find the course_id of courses offered in Fall 2024 but not offered in Spring 2025.
--query:
select course_id FROM section where semester = 'Fall' AND year = 2024
EXCEPT
SELECT course_id from section where semester = 'Spring' and year = 2025;