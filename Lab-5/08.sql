-- q8: Find all names present in the instructor table combined with all names present in the student table.
--query:
select name from instructor union select name from student;