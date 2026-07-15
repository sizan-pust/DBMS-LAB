-- q2: Find the CategoryID and CategoryName for the category with the description containing 'Soft drinks'.
--query:
SELECT CategoryID, CategoryName FROM Category WHERE description like '%Soft drinks%';