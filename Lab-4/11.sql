-- q11: Find the OrderID and the LastName of the employee who handled that order by linking Orders and Employee.
--query:
SELECT Orders.OrderID, Employee.LastName
FROM Orders, Employee WHERE Orders.EmployeeID = Employee.EmployeeID;