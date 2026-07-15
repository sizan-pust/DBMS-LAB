-- Question 12: Find the ProductName and CategoryName for all products that are not in the 'Seafood' category.
---query:
SELECT p.ProductName, c.CategoryName
FROM Product as p, Category as c
WHERE p.CategoryID = c.CategoryID and c.CategoryName <> 'Seafood';