-- q14: Delete all students who have a tot_cred (total credits) value of less than 40.
--query:
-- we have first deleted dependent course registration first so that it satisfies the foreign key constraint.
DELETE FROM takes WHERE ID IN ( SELECT ID FROM student WHERE tot_cred < 40 );
DELETE FROM student WHERE tot_cred < 40;