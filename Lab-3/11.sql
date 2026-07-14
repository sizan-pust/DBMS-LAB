--Q11: Find the title of a course and the title of its prerequisite.
--Query:
SELECT c.title AS course_title, p.title AS prereq_title
FROM prereq AS pr, course AS c, course AS p
WHERE pr.course_id = c.course_id AND pr.prereq_id = p.course_id;