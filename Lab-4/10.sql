-- q10: Find the ProductName and the City of the supplier who provides it by linking Product and Supplier using SupplierID.
--query:
SELECT Product.ProductName, Supplier.City FROM Product, Supplier  WHERE Product.SupplierID = Supplier.SupplierID;