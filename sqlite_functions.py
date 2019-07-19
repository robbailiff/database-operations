"""
Here is some practice code for using the sqlite3 module with Python. 
Here I was experimenting with applying functions in SQLite statements. 
I have included comments throughout explaining the code for my own benefit, but hopefully they'll help someone else too.

Hope you like the code. Any tips, comments or general feedback are welcome.

Thanks, 
Rob

+++++++++++++++++++++++++++++++++++++++++
For anyone looking for a tutorial on the sqlite3 module, the tutorial I used is located here: https://www.pythoncentral.io/advanced-sqlite-usage-in-python/

Also the official documentation: https://docs.python.org/3/library/sqlite3.html

"""

# Import libraries
import sqlite3

# Define function
def temp_converter(temp):
    result = round((temp - 32) / 1.8, 1)
    return result

# Connect to the database
db = sqlite3.connect(':memory:')

# Register the function using the create_function method of connection object, which takes 3 arguments
# First is the name which will be used to call the function in an SQL statement
# Second is the number of arguments in the function to be called
# Third is the function object (i.e. the defined function itself)
db.create_function('F_to_C', 1, temp_converter)

# Create cursor object
cursor = db.cursor()

# Create a table in the database
cursor.execute('''CREATE TABLE weather(
    id INTEGER PRIMARY KEY, 
    city TEXT, 
    temp REAL)''')

# Insert data into the table but call the function to convert the temperature from Farenheit to Celcius
cursor.execute('''INSERT INTO weather(city, temp) VALUES (?,F_to_C(?))''', ("London", 68.3))

# Commit the changes
db.commit()

# Retrieve all the data in the table
cursor.execute('''SELECT * FROM weather''')

# Fetch first entry of cursor selection and notice that the temperature has been converted
result = cursor.fetchone()
print(f"Result returned from query: \n{result}")

# And finally close down the database
db.close()
