"""
Here is some practice code for using the sqlite3 module with Python. 
It is a good way to practice some of the skills learnt on SQL courses. 
I have included comments throughout explaining the code for my own benefit, but hopefully they'll help someone else too.

NB: I should have probably written a function to check the database entries instead of repeating the same code

Hope you like the code. Any tips, comments or general feedback are welcome.

Thanks, 
Rob

+++++++++++++++++++++++++++++++++++++++++
For anyone looking for a tutorial on the sqlite3 module, the tutorial I used is located here: https://www.pythoncentral.io/introduction-to-sqlite-in-python/

"""

# Import libraries
import sqlite3

# Pass ':memory:' as an argument to the connect() function to set up a database in RAM
db = sqlite3.connect(':memory:')

# To operate the database we need to create a cursor object and pass the instructions to it
cursor = db.cursor()

# Next we create an example table using the excute() method of the cursor object
cursor.execute('''CREATE TABLE Employees(
    UserID INTEGER PRIMARY KEY,
    Name VARCHAR,
    Age INTEGER,
    StartDate DATE
)''')

# Then we use the db object to commit the change
db.commit()

# Next we add information to the database by writing an SQL statement with "?" acting as a placeholder for the data to be input. Then pass a second argument as a tuple for the actual values you want to add for each column
cursor.execute('''INSERT INTO Employees(Name, Age, StartDate) VALUES (?,?,?)''', ("Bob", 33, '2010-08-22'))
db.commit()

# You can also pass the second argument as a dictionary. 
cursor.execute('''INSERT INTO Employees(Name, Age, StartDate) VALUES(:Name,:Age,:StartDate)''', {'Name': "David", 'Age': 24, 'StartDate': "2017-07-10"})
db.commit()

# Or you can pass the second argument as variables
name = "Heather"
age = 29
start = "2011-09-14"
cursor.execute('''INSERT INTO Employees(Name, Age, StartDate) VALUES(?,?,?)''', (name, age, start))
db.commit()

# You can also create a list of tuples containing the data entries and use the executemany() method
entries = [("Gregory", 44, "2004-11-12"),
("Susan", 50, "1998-04-11"),
("Tyler", 22, "2018-06-18")]

cursor.executemany('''INSERT INTO Employees(Name, Age, StartDate) VALUES(?,?,?)''', entries)
db.commit()

# To see the data we've entered we need to select it with an SQL statement and the return it with the fetchone() or fetchall() methods
cursor.execute('''SELECT UserID, Name, Age, StartDate FROM Employees''')

# We can can see the row number of the last data entry with lastrowid()
print("Last row id: " + str(cursor.lastrowid) + "\n")

# The fetchone() method retrieves the first column
print("First record in the database: \n" + str(cursor.fetchone()) + "\n")

# The cursor object acts as an iterator which moves over entries after a SELECT statement. Hence why it only prints entries 2-6 for the fetchall() statement after it previously returned the first row following the use fetchone() method
print("All records after the first: \n" + str(cursor.fetchall()) + "\n")

# If we select all columns again and use fetchall() before any other methods, it returns the full selection
cursor.execute('''SELECT UserID, Name, Age, StartDate FROM Employees''')
# We can save the returned data to a variable
all = cursor.fetchall()
print("All records saved to a variable: \n" + str(all) + "\n")

# We can iterate over the records like a regular python iterable
for row in all:
    print(f"User {row[0]} Name: {row[1]}")
print("")
    
# We can update records with the UPDATE statement
cursor.execute('''UPDATE Employees SET Name = ? WHERE UserID = ?''', ("Stefano", 6))

# Now check the entry with a query. The second argument must be a tuple
cursor.execute('''SELECT Name FROM Employees WHERE UserID = ?''', (6,))
print("Updated Entry: " + str(cursor.fetchall()) + "\n")
    
# If we made a mistake we can change it back with db.rollback() to return database to the last time db.commit() was used
db.rollback()

# Now check the whether the database has gone back to the previous entry (which was Tyler)
cursor.execute('''SELECT Name FROM Employees WHERE UserID = ?''', (6,))
print("Rollback Entry: " + str(cursor.fetchall()) + "\n")

# We can also remove entries from the database with the DELETE statement
cursor.execute('''DELETE FROM Employees WHERE UserID = ? ''', (6,))
db.commit()

# Do a final check of the entries. We can use '*' as a wildcard in the statement instead of listing all the column names
cursor.execute('''SELECT * FROM Employees''')
print("Database after deleted entry: \n" + str(cursor.fetchall()) + "\n")

# Finish by closing the database
db.close()
