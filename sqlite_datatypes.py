"""
Here is some practice code for using the sqlite3 module with Python. 
I was mostly playing around with datatypes and came across some useful methods. 
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
from datetime import date, datetime

# Pass ':memory:' as an argument to the connect() function to set up a database in RAM
# Sqlite returns a string by default for certain datatypes. By passing PARSE_DECLTYPES and PARSE_COLNAMES to the connect method it converts them to the correct datatype
# PARSE_DECLTYPES and PARSE_COLNAMES parse the declared type and column name respectively for each column returned. It works by searching the sqlite converters dictionary for a converter function for the declared datatype and thens returns a converted value
db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

# Create a cursor object and pass the instructions to it
cursor = db.cursor()

# Use the execute method of the cursor object to execute a command
cursor.execute('''CREATE TABLE login_info(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    login_time DATE)''')

# Then we use the db object to commit the change
db.commit()

thedate = date.today()
print(f"The date saved by the date.today() method is {thedate} and it's datatype is {type(thedate)}.\n")

# Insert some data into the table
cursor.execute('''INSERT INTO login_info(name, login_time) VALUES (?,?)''', ("Bob", thedate))
db.commit()

# Retrieve the inserted object
cursor.execute('''SELECT login_time FROM login_info''')

# The fetchone method returns a tuple so you need to refer to the first index to extract the info
# If we did not pass the PARSE_DECLTYPES and PARSE_COLNAMES to the connect method, this date would have been returned as a string datatype
result = cursor.fetchone()
print(f"The result from the query is {result} and it's datatype is {type(result)}.\n")
print(f"When extracted, the value is {result[0]} and it's datatype is {type(result[0])}.\n")

print("=" * 50 + "\n")

# To use a datetime object instead of a date object, we must declare the column in the table as a timestamp datatype
timestamp = datetime.now()
print(f"The timestamp saved by the datetime.now() method is {timestamp} and it's datatype is {type(timestamp)}.\n")

# Create a new table with a timestamp datatype
cursor.execute('''CREATE TABLE login_info_2(
    id INTEGER PRIMARY KEY,
    name VARCHAR,
    login_time TIMESTAMP)''')

# Insert timestamp into table
cursor.execute('''INSERT INTO login_info_2(name, login_time) VALUES(?,?)''', ("Dave", timestamp))
db.commit()
 
# Retrieve the inserted object
cursor.execute('''SELECT login_time [timestamp] FROM login_info_2''')

# Fetch the entry and extract from the tuple by indexing
# The datetime object data is parsed correctly when retreived because PARSE_DECLTYPES and PARSE_COLNAMES were passed to the connect method
entry = cursor.fetchone()
print(f"The result from the query is {entry} and it's datatype is {type(entry)}.\n")
print(f"When extracted, the value is {entry[0]} and it's datatype is {type(entry[0])}.\n")

# And finally close down the database
db.close()
