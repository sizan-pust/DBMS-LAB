-- q9: Find the ProductName and its CategoryName by linking Product and Category using CategoryID.
--query:
SELECT Product.ProductName, Category.CategoryName FROM Product, Category WHERE Product.CategoryID = Category.CategoryID;