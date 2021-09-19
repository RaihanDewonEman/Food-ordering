import sys
import psycopg2
import databaseConnection as dbc
from datetime import datetime, timezone


### -------------------  Menu List	------------------------------
def menu():
	print("1. Add customer")
	print("2. Remove customer")
	print("3. Add product")
	print("4. Remove product")
	print("5. Update product")
	print("6. Show list of products")
	print("7. Show list of customers")
	print("8. Show list of orders")
	print("9. Top selling product")
	print("10. Customer list who ordered most in total")
	print("11. Order a product")
	print("12. List of products according to lastest addition")
	print("13. Show list of product which price is greater that average product price")
	print("14. Show total customer, product and order")
	print("15. Show a customer details with his contact info")
	print("16. Max priced product")
	print("17. List of customer who doesn't order yet")
	print("18. List of product which doesn't sell yet")
	print("19. Exit")
	print()


###---------------------------	Creation of database	-----------------------------
def create_database(connection):
	dbname = input("Please enter database name: ")
	#print(connection)
	connection.autocommit = True
	cur = connection.cursor()
	cur.execute("SELECT datname FROM pg_database;")
	list_database = cur.fetchall()
	#print(list_database)
	if (dbname,) in list_database:
		print("Database already exist.")
	else:
		sql = "CREATE DATABASE "+ dbname + ";"
		cur.execute(sql)
		print('Database is created successfully!!!')
	connection.close()
	#print(connection)
	return dbname


###--------------------------   create table 	----------------------------
def create_table(dbname):
	connection = dbc.database_connection2(dbname)
	#print(connection)
	connection.autocommit = True
	cur = connection.cursor()
	
	sql = "CREATE TABLE IF NOT EXISTS customers(customerid SERIAL, customername varchar(255) NOT NULL, PRIMARY KEY(customerid));"
	cur.execute(sql)
	
	sql = "CREATE TABLE IF NOT EXISTS customercontact(customerid int, customeraddress varchar(255), phonenumber varchar(255), CONSTRAINT PK_customercontact PRIMARY KEY(customeraddress, phonenumber), FOREIGN KEY(customerid) REFERENCES customers(customerid));"
	cur.execute(sql)
	
	sql = "CREATE TABLE IF NOT EXISTS products(productid SERIAL, productname varchar(255), price decimal(10,2), PRIMARY KEY(productid));"
	cur.execute(sql)
	
	sql = "CREATE TABLE IF NOT EXISTS orders(orderid SERIAL, customerid int REFERENCES customers(customerid), productid int REFERENCES products(productid), unit int, totalcost int, orderdate timestamp, PRIMARY KEY(orderid));"
	cur.execute(sql)
	print("All the tables are created!!!")
	return cur


###-------------------------	Choice 1	-----------------------------
def add_customer(cur):
	customer_name = input("Enter your name: ")
	customer_phone = input("Enter your phone number: ")
	customer_address = input("Enter you address : ")
	sql = "INSERT INTO customers(customername) values('"+customer_name+"') RETURNING customerid;"
	cur.execute(sql)
	customer_id = cur.fetchone()[0]
	sql = f"INSERT INTO customercontact(customerid, customeraddress, phonenumber) values({customer_id},'{customer_address}','{customer_phone}');"
	cur.execute(sql)
	print("A new customer is added successfully!")
	

### ----------------------- Remove a customer	-------------------------
def remove_customer(cur):
	list_of_customer(cur)
	customer_id = int(input("Please enter a customer id that you want to remove: "))
	sql = f"DELETE FROM customers where customerid = {customer_id};"
	cur.execute(sql)
	sql = f"DELETE FROM customercontact where customerid = {customer_id};"
	cur.execute(sql)
	print("Customer is removed successfully!")
	
### ---------------------- add a product item	----------------------------
def add_product(cur):
	product_name = input("Enter product name: ")
	product_price = float(input("Enter product price: "))
	sql = f"INSERT INTO products(productname, price) values('{product_name}', {product_price});"
	cur.execute(sql)
	print("A new product is added successfully!")
	
	
###----------------------------- Remove a product 	-------------------
def remove_product(cur):
	list_of_product(cur)
	product_id = int(input("Please enter a product id that you want to remove: "))
	sql = f"DELETE FROM products where productid = {product_id}"
	cur.execute(sql)
	print("A product is removed successfully!")


###------------------------- Update price	----------------------------------	
def update_product(cur):
	list_of_product(cur)
	product_id = int(input("Please enter a product id that you want to update its price: "))
	product_price = float(input("Enter new price: "))
	sql = f"Update products set price={product_price} where productid = {product_id};"
	cur.execute(sql)
	print("A product price is updated successfully!")
	
	
###------------------------------- Show Product	-------------------------------
def list_of_product(cur):
	sql = "SELECT * from products;"
	cur.execute(sql)
	records = cur.fetchall()
	print("Id	Name	Price")
	for row in records:
		print(f"{row[0]}	{row[1]}	{row[2]}")
	print()

	
###----------------------------	Show customers	---------------------
def list_of_customer(cur):
	sql = "SELECT * from customers;"
	cur.execute(sql)
	records = cur.fetchall()
	print("Id	Name")
	for row in records:
		print(f"{row[0]}	{row[1]}")
	print()

	
###------------------------- Show orders	-------------------------
def list_of_order(cur):
	sql = "SELECT * from orders;"
	cur.execute(sql)
	records = cur.fetchall()
	print("Id	Customer Id	Product Id	Unit	Total	Date")
	for row in records:
		print(f"{row[0]}	{row[1]}		{row[2]}		{row[3]}	{row[4]}	{row[5]}")
	print()
	
###-------------------------- Top selling product	-----------------------------
def top_selling_product(cur):
	sql = "SELECT p.productname, count(p.productname) as ordernumber from orders as o inner join products as p on o.productid = p.productid GROUP BY p.productid ORDER BY ordernumber DESC LIMIT 1;"
	cur.execute(sql)
	record = cur.fetchone()
	print("Top selling product: ")
	print(f"{record[0]}	{record[1]}")
	
###--------------------------	choice 12	------------------------------
def most_ordered_customer(cur):
	sql = "SELECT c.customername, sum(o.totalcost) as total from orders as o inner join customers as c on o.customerid = c.customerid GROUP BY c.customerid ORDER BY total DESC;"
	cur.execute(sql)
	records = cur.fetchall()
	print("Name	Total")
	for row in records:
		print(f"{row[0]}	{row[1]}")
	print()
	
###---------------------	Take a order	----------------------------
def taking_order(cur):
	list_of_customer(cur)
	customer_id = int(input("Please select a customer id: "))
	list_of_product(cur)
	product_id = int(input("Please select a product id: "))
	product_unit = int(input("Please enter the quantity of the product: "))
	sql = f"SELECT price from products where productid = {product_id};"
	cur.execute(sql)
	price = cur.fetchone()
	total_cost = product_unit*price[0];
	#print(total_cost)
	today = datetime.now(timezone.utc)
	sql = f"INSERT INTO orders(customerid, productid, unit, totalcost, orderdate) values({customer_id}, {product_id}, {product_unit}, {total_cost}, '{today}');"
	cur.execute(sql)
	print("Order is taken successfully!")
	
###---------------------------	choice 12	------------------------
def list_newly_added_product(cur):
	sql = "SELECT * from products ORDER BY productid DESC;"
	cur.execute(sql)
	records = cur.fetchall()
	print("Id	Name	Price")
	for row in records:
		print(f"{row[0]}	{row[1]}	{row[2]}")
	print()

	
### ----------------------	Customer Info	--------------------------
def customer_info(cur):
	list_of_customer(cur)
	customer_id = int(input("Enter a customer id: "))
	sql = f"SELECT * from customers inner join customercontact on customers.customerid = customercontact.customerid where customers.customerid = {customer_id};"
	cur.execute(sql)
	records = cur.fetchall()
	#print(records)
	for row in records:
		print(f"Customer id: {row[0]}, Customer Name: {row[1]}, Customer address: {row[3]}, Customer Contact number: {row[4]}")
	print()


if __name__ == '__main__':
	connection = dbc.database_connection()
	if connection is None:
		sys.exit()
	dbname = create_database(connection)
	cur = create_table(dbname)
	while True:
		menu()
		choice = int(input("Enter your choice: "))
		if choice == 1:
			add_customer(cur)
		elif choice == 2:
			remove_customer(cur)
		elif choice == 3:
			add_product(cur)
		elif choice == 4:
			remove_product(cur)
		elif choice == 5:
			update_product(cur)
		elif choice == 6:
			list_of_product(cur)
		elif choice == 7:
			list_of_customer(cur)
		elif choice == 8:
			list_of_order(cur)
		elif choice == 9:
			top_selling_product(cur)
		elif choice == 10:
			most_ordered_customer(cur)
		elif choice == 11:
			taking_order(cur)
		elif choice == 12:
			list_newly_added_product(cur)
		elif choice == 13:
			sql = "SELECT productname from products where price > (SELECT avg(price) from products);"
			cur.execute(sql)
			records = cur.fetchall()
			print("Product Name")
			for row in records:
				print(f"{row[0]}")
		elif choice == 14:
			sql = "SELECT count(customerid) from customers;"
			cur.execute(sql)
			total_customer = cur.fetchone()[0]
			sql = "SELECT count(productid) from products;"
			cur.execute(sql)
			total_product = cur.fetchone()[0]
			sql = "SELECT count(orderid) from orders;"
			cur.execute(sql)
			total_order = cur.fetchone()[0]
			print(f"Total customers : {total_customer}, Total products : {total_product}, Total orders: {total_order}.")
		elif choice == 15:
			customer_info(cur)
		elif choice == 16:
			sql = "SELECT productname, price from products ORDER BY price DESC LIMIT 1;"
			cur.execute(sql)
			result = cur.fetchone()
			#print(result)
			print(f"Product Name: {result[0]}, Price: {result[1]}")
		elif choice == 17:
			sql = "SELECT c.customername from orders as o right join customers as c on o.customerid = c.customerid where o.orderid is NULL;"
			cur.execute(sql)
			records = cur.fetchall()
			for row in records:
				print(f"Customer Name : {row[0]}")
			print()
		elif choice == 18:
			sql = "SELECT p.productname from orders as o right join products as p on o.productid = p.productid where o.orderid is NULL;"
			cur.execute(sql)
			records = cur.fetchall()
			print("Product Name")
			for row in records:
				print(f"{row[0]}")
			print()
		else:
			connection.close()
			break

