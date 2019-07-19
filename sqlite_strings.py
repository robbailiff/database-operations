"""
Here is some practice code for using the sqlite3 module with Python. 
In this code I was playing around with string formating in SQL multiline string statements with the aim of taking lists of strings and inserting them into a DB. 
I have included comments throughout explaining the code for my own benefit, but hopefully they'll help someone else too.

Hope you like the code. Any tips, comments or general feedback are welcome.

Thanks, 
Rob

+++++++++++++++++++++++++++++++++++++++++
The official sqlite3 documentation: https://docs.python.org/3/library/sqlite3.html

"""

# Import libraries
import sqlite3

# Pass ':memory:' as an argument to the connect() function to set up a database in RAM
db = sqlite3.connect(':memory:')

# Create a cursor object and pass the instructions to it
cursor = db.cursor()

row = ['ID', 'Item_name', 'Place']

# Use the execute method of the cursor object to execute a command
cursor.execute(f'''CREATE TABLE Stuff(
    {row[0]} INTEGER PRIMARY KEY,
    {row[1]} VARCHAR,
    {row[2]} VARCHAR)''')

# Then we use the db object to commit the change
db.commit()

data = ['TV', 'Living Room']

# Insert data from a list into table
cursor.execute('''INSERT INTO Stuff(Item_name, Place) VALUES(?,?)''',(data[0], data[1]))
db.commit()

# Retrieve the inserted object
cursor.execute('''SELECT * FROM Stuff''')

# The description method of the cursor object provides the column names for the last query in a 7-tuple (for compatibility reasons) 
print("Description method result: \n" +  str(cursor.description) + "\n")
names = [name[0] for name in cursor.description]
print("First item in each tuple: \n" + str(names) + "\n")

# Fetch first entry of cursor selection
result = cursor.fetchone()
print(f"Result returned from query: \n{result}")

# And finally close down the database
db.close()
