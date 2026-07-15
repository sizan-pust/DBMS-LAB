-- q5: Find the ProductName and Price of products that have a Supplier ID of 1 and cost more than $18.00.
--query:
SELECT ProductName, Price FROM Product WHERE SupplierID = 1 and Price > 18.00;