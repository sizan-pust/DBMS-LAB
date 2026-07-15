-- q2: Find the ID and Course ID of all student course registrations where the grade has not yet been assigned.
--query:
select id, course_id from takes where grade is null;