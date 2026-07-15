-- q6: Find the CompanyName of all customers who are located in either 'Germany' or 'Mexico'.
--query:
SELECT CompanyName FROM Customer WHERE Country = 'Germany' OR Country = 'Mexico';