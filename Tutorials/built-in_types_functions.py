# https://docs.python.org/3/library/functions.html
# https://docs.python.org/3/library/stdtypes.html
# list()
# tuple()
# set()
# dict()
# all()
# any()
# abs()
# round()
# min() max()
# sorted()
# sum()
# type()
# staticmethod()
# classmethod()

# string: upper(), lower(), strip(), replace('old', 'new'), split('delimiter'),  join( )
# Lists: append(arg), remove(arg), count(arg) clear()  sort()
# Dictionaries: keys() values()

my_list = [2, 4, 1, 0, 8]
print(sorted(my_list))

my_list.sort(reverse=True)
print(my_list)

# Both list.sort() and sorted() have a key parameter to specify a function to be called on each list element prior to
# making comparisons. The value of the key parameter should be a function that takes a single argument and returns a
# key to use for sorting purposes.

student_tuples = [
    ('john', 'A', 15),
    ('jane', 'B', 12),
    ('dave', 'B', 10),
]
sorted(student_tuples, key=lambda student: student[2])  # sort by age
print(student_tuples)

########################################### dir()###########################################
# Without arguments, return the list of names in the current local scope. With an argument, attempt to return a list of valid attributes for that object.
print(dir())

# print(dir(numpy))


########################################### iter() next() ###########################################
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


class MyNumbers:
    def __iter__(self):
        self.a = 1
        return self

    def __next__(self):
        if self.a <= 5:
            x = self.a
            self.a += 1
            return x
        else:
            raise StopIteration


myclass = MyNumbers()
myiter = iter(myclass)

print("next(myiter):",next(myiter))
print("myiter.__next__():",myiter.__next__())


for x in myiter:
    print(x)


########################################### vars() eval() ###########################################

# Class attributes belong to the class itself they will be shared by all the instances. 
class emp:
    count = 0  # class attribute
    count_ = 0

    def increase(self):
        emp.count += 1
        self.count_ += 1

    def __init__(self):
        self.name = 'xyz'
        self.salary = 4000

    def show(self):
        print(self.name)
        print(self.salary)


e1 = emp()

print("vars of my_number_object: ", vars(e1))
print(dir(e1))

e1.increase()
e2 = emp()
print(e2.count)
print(e2.count_)

#################################### zip ####################################
# https://www.geeksforgeeks.org/python-unzip-a-list-of-tuples/
x = [1, 2, 3]
y = [4, 5, 6]
print(list(zip(x, y)))

# zip() in conjunction with the * operator can be used to unzip a list:
x2, y2 = zip(*zip(x, y))
print(list(x2))

print('#################################### map ####################################')

# map functions expect a function object and any number of iterables, such as list, dictionary, etc. It executes the function_object for each element in the sequence and returns a list of the elements modified by the function object.

x = [3, 5, 1, -2, 0]

my_lambda = lambda a: True if a > 2 else False

for i in map(my_lambda, x):
    print(i)

print(list(map(my_lambda, x)))

list_a = [1, 2, 3]
list_b = [10, 20, 30]

map(lambda x, y: x + y, list_a, list_b)

print('#################################### all ####################################')

print("all() output is:", all(map(my_lambda, x)))

print('#################################### any ####################################')

print("any() output is:", any(map(my_lambda, x)))

######################### Iterating Over a Dictionary Using Map and Lambda #########################

dict_a = [{'name': 'python', 'points': 10}, {'name': 'java', 'points': 8}]

map(lambda x: x['name'], dict_a)  # Output: ['python', 'java']

map(lambda x: x['points'] * 10, dict_a)  # Output: [100, 80]

map(lambda x: x['name'] == "python", dict_a)  # Output: [True, False]

print('#################################### filter ####################################')
# The filter function expects two arguments: function_object and an iterable. function_object returns a boolean value and is called for each element of the iterable. Filter returns only those elements for which the function_object returns true.
print("filter output is:", list(filter(my_lambda, x)))

print('#################################### slice() ####################################')
# https://www.programiz.com/python-programming/methods/built-in/slice
pyString = 'Python'
stop = 4
slice_object = slice(stop)
print(pyString[slice_object])

start = 2
stop = 5
step = 2
slice_object = slice(start, stop, step)
print(pyString[slice_object])

#################################### char(),ord() ####################################
chr(97)  # returns the string 'a'
chr(8364)  # returns the string '€'

ord('a')  # returns 97

#################################### filter() ####################################

# filter() takes in a function and a list as arguments. It filters out all the elements of a sequence “sequence”, for which the function returns True.

# Python Program to find numbers divisible  
# by thirteen from a list using anonymous  
# function 

# Take a list of numbers.  
my_list = [12, 65, 54, 39, 102, 339, 221, 50, 70, ]

# use anonymous function to filter and comparing  
# if divisible or not 
result = list(filter(lambda x: (x % 13 == 0), my_list))

# printing the result 
print(result)


#################################### time ####################################
#import time

#Unix system, January 1, 1970, 00:00:00
#print(time.time())
#print(time.time()/ (24*365*3600))
#print(time.ctime())
#print(time.localtime(24*3600*365))
#print(time.gmtime(24*3600*365))

#t = (2018, 12, 28, 8, 44, 4, 4, 362, 0)
#print(time.mktime(t))
#named_tuple = time.localtime() # get struct_time
#time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
#print(time_string)
#i=0
#while True:
#	time.sleep(1)
#	i+=1
#	print(i)



####################################locals(), globals() ####################################
#https://www.geeksforgeeks.org/python-locals-function/


#################################### string ####################################

a = ["Create" "a" "single" "string" "from" "all" "the" "elements"] 
print(" ".join(a)) 

print('*' * 80)

multiStr = "select * from multi_row \
where row_id < 5"

#startswith, endswith



