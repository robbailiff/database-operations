"""
In this mini-project, I have downloaded the data from a web page in .tsv format, and saved it as a file object. 
Then I have parsed it using csv_reader, and trimmed and cleaned the data ready for use. 
Next I have set up an SQLite database and used string formating in SQL multiline string statements to set up the column names and inset the data. 
Finally, I have recalled data from the table to check that the database is working correctly.

Hope you like the code. Any tips, comments or general feedback are welcome.

Thanks, 
Rob

+++++++++++++++++++++++++++++++++++++++++
The official sqlite3 documentation: https://docs.python.org/3/library/sqlite3.html

CSV Module Documentation: https://docs.python.org/2/library/csv.html

List comprehension thread:
https://stackoverflow.com/questions/52462764/replacing-string-in-list-of-lists-python

"""

# Import libraries
import csv, sqlite3
from urllib.request import urlopen, Request


################
### Download ###
################


link = "https://www.dropbox.com/s/shsvqzbe5c6ncbr/livermore1a.txt?dl=1"

# Download the data from the link
req = Request(link)
res = urlopen(req)

# This dataset contains special characters not recognised by unicode so we need to decode to latin-1
data = res.read().decode('latin-1')
data = data[:1500]

print("Pre-parsed data: \n")
print(data[:200])
print("=" * 30 + "\n")

# Create a new file in write+ mode and write the data to it. Then return the file pointer to position zero ready to by read by the csv reader
tsvfile = open('data.tsv', 'w+')
tsvfile.write(data)
tsvfile.seek(0)


###############
### Parsing ###
###############


# Create empty list to append values to
data_list = []

# Parse the file object line by line to create a list of lists, with the main list representing a table, and each nested list representing a column in the table
for line in csv.reader(tsvfile, dialect="excel-tab"):
    if line:
        data_list.append(line)

# Remember to close the file
tsvfile.close()

# Save header to a list
header = data_list[0]
print("Parsed header: \n\n" + str(header) + "\n")
print("=" * 30 + "\n")

# Remove header and trim the main list
data_list = data_list[1:6]
print("Parsed data: \n\n" + str(data_list) + "\n")
print("=" * 30 + "\n")

# Replace all blank strings
for row in data_list:
    for index, column in enumerate(row):
        if not column:
            row[index] = column.replace('', 'No data')
                      

# I also found on stack overflow that you can use list comprensions. The following code also worked:

# new_list = [[col or 'No data' for col in row] for row in data_list]


# Remove unwanted columns
data_list = [row[2:] for row in data_list]

# Concatenate first 2 columns
new_list = []
for row in data_list:
    string = row[0] + ' ' + row[1]
    row = row[2:]
    row.insert(0, string)
    new_list.append(row)

data_list = new_list
print("Trimmed and formatted data: \n\n" + str(data_list) + "\n")
print("=" * 30 + "\n")


################
### Database ###
################


# Set up DB and cursor object
db = sqlite3.connect(':memory:')
cursor = db.cursor()

# Create the table we will add the data to and then add the name from headers list    
cursor.execute(f'''CREATE TABLE FungiData(
    {header[0]} INTEGER PRIMARY KEY,
    {header[1]} VARCHAR,
    {header[2]} DATE,
    {header[3]} DATE,
    {header[4]} VARCHAR,
    {header[5]} VARCHAR,
    {header[6]} VARCHAR,
    {header[7]} VARCHAR,
    {header[8]} INTEGER,
    {header[9]} VARCHAR,
    {header[10]} VARCHAR,
    {header[11]} VARCHAR,
    {header[12]} VARCHAR,
    {header[13]} VARCHAR,
    {header[14]} VARCHAR,
    {header[15]} VARCHAR
)''')

# Then we commit the change
db.commit()

# Check that the headers habe been entered correctly
cursor.execute('''SELECT * FROM FungiData''')
head_check = [col[0] for col in cursor.description]
print("Column headers in DB table: \n\n" + str(head_check) + "\n")
print("=" * 30 + "\n")


# Insert data into DB using iteration and string formatting for column names and inserted data
for row in data_list:
    cursor.execute(f'''INSERT INTO FungiData(
    {header[1]},
    {header[2]},
    {header[3]},
    {header[4]},
    {header[5]},
    {header[6]},
    {header[7]},
    {header[8]},
    {header[9]},
    {header[10]},
    {header[11]},
    {header[12]},
    {header[13]},
    {header[14]},
    {header[15]}
    ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14]))

db.commit()


##############
### Checks ###
##############


# Recall entries to check the results
cursor.execute('''SELECT * FROM FungiData''')

print("First row in the database: \n\n" + str(cursor.fetchone()) + "\n")
print("=" * 30 + "\n")

# Recall entries from a specific column
cursor.execute('''SELECT SpeciesAsRecorded FROM FungiData''')

print("All entries from Species column: \n\n" + str(cursor.fetchall()) + "\n")
print("=" * 30 + "\n")


cursor.execute('''SELECT Ecosystem FROM FungiData WHERE RecordKey = ?''', (2,))
print("Ecoystem for second record in the database: \n\n" + str(cursor.fetchall()) + "\n")

# Finally close the DB
db.close()
