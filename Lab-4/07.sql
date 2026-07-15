-- q7: Find the CompanyName and Country of all customers who are not located in the 'UK'.
--query:
select CompanyName, Country from Customer where Country <> 'UK';