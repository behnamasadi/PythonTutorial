##################################### Reading Keyboard Input #####################################
# input() functions read data from keyboard as string

# user_value=input("please insert a value")
# print(user_value)


print("##################################### Reading/Writing File #####################################")

# Opening and Closing Files
# file object = open(file_name ,access_mode)
# access_mode=r,rb,r+,rb+,w,wb,w+,wb+,a,ab,a+,ab+
file_name = 'data/bob.txt'
access_mode = 'r'
file_object = open(file_name, access_mode)
print("Reading a file:")
for line in file_object:
    print(line)

f2 = open(file_name, 'r')
# read the whole file into a single variable, which is a list of every row of the file.
lines = f2.readlines()

# The with statement clarifies code that previously would use try...finally blocks to ensure that clean-up code is executed.

with open('file_path', 'w') as file:
    file.write('hello world !')

print("##################### Checking/ Creating/ Traversing Files, Directories #######################")

import os.path

# os.path - The key to File I/O
os.path.exists("data/bob.txt")
os.path.isfile("data/bob.txt")  # Does bob.txt exist?  Is it a file, or a directory?
os.path.isdir("data")
os.path.isabs("/home/me/bob.txt")  # Is it an absolute path to this file?

print("##################################### Reading/Writing CSV #####################################")

path = "data/data.csv"
lines = [line for line in open(path)]
print(lines[0])

print(lines[0].strip().split(','))
print(lines[1].strip().split(','))

import csv
import datetime

file = open(path, newline='')
reader = csv.reader(file)

header = next(reader)

data = []
for row in reader:
    # Date,Open,High,Low,Close,Volume,Adj Close
    date = datetime.datetime.strptime(row[0], '%m/%d/%Y')
    open_price = float(row[1])
    high = float(row[2])
    low = float(row[3])
    close = float(row[4])
    volume = int(row[5])
    adj_close = float(row[6])
    data.append([date, open_price, high, low, close, volume, adj_close])

path_processed = "data/processed_data.csv"
file = open(path_processed, 'w')
writer = csv.writer(file)
writer.writerow(["Date", "Return"])



print("##################################### Serializing/de-serializing #####################################")

# Pickling: It is a process where a Python object hierarchy is converted into a byte stream.
# Unpickling: It is the inverse of Pickling process where a byte stream is converted into an object hierarchy.
import pickle


# import io

class MyData:
    def __init__(self, name):
        self.name = name
        self.value = 10


# out=io.StringIO()
data_to_be_stored = [MyData("Behnam"), MyData("Asadi")]
dbfile = open('data/pickle_data', 'wb')  # append binary

pickle.dump(12, dbfile)
pickle.dump("my string", dbfile)
pickle.dump({"water": 1, "beer": 2}, dbfile)
pickle.dump(MyData("Behnam"), dbfile)
dbfile.close()

# pickle.dump(data_to_be_stored, dbfile)
# dbfile.close()

print("Serializing/de-serializing using pickle")

dbfile = open('data/pickle_data', 'rb')  # append binary
my_int = pickle.load(dbfile)
print(my_int)

my_string = pickle.load(dbfile)
print(my_string)

my_dict = pickle.load(dbfile)
print(my_dict)

my_objct = pickle.load(dbfile)
print("object name is: {} and value is{}:".format(my_objct.name, my_objct.value))

# The dumps() works exactly like dump() but instead of sending the output to a file, it returns the pickled data as a string.
str_object = pickle.dumps(MyData("Asadi"))
print(pickle.loads(str_object).name)





print("#################################### glob ####################################")
import glob

#Escape all special characters ('?', '*' and '['). This is useful if you want to match an arbitrary literal string that may have special characters in it

directory_path="./*"
print("directory path= {}".format(directory_path) )

for name in glob.glob(directory_path):
	print(name)


directory_path_and_sub_directories="./*/*"
print("directory path= {}".format(directory_path_and_sub_directories) )
for name in glob.glob(directory_path_and_sub_directories):
	print(name)


print("#################################### pathlib,rglob ####################################")
from pathlib import Path

for filename in Path('./').rglob('*.py'):
    print(filename)

