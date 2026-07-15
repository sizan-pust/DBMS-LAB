-- q8: Find the OrderID and CustomerID for orders placed on or after '2025-07-05'.
--query:
select OrderID, CustomerID from Orders where OrderDate >= '2025-07-05';