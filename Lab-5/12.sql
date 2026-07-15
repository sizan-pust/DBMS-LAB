-- q12: Insert a new instructor named 'Mozart' into the 'Music' department with ID '99999' and a salary of $50,000.
--query:
insert into department (dept_name, building, budget)
values ('Music', 'Packard', 60000);
INSERT INTO instructor (ID, name, dept_name, salary)
VALUES ('99999', 'Mozart', 'Music', 50000);