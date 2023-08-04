# 



- list()
- tuple()
- set()
- dict()
- all()
- any()
- abs()
- round()
- min() max()
- sorted()
- sum()
- type()
- staticmethod()
- classmethod()

## string
```
upper(), lower(), strip(), replace('old', 'new'), split('delimiter'),  join( )
```
## list
```
 append(arg), remove(arg), count(arg) clear()  sort()
```
## dictionaries: 
```
keys() values()
```
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

## dir()
 Without arguments, return the list of names in the current local scope. With an argument, attempt to return a list of valid attributes for that object.
```
print(dir())
print(dir(numpy))
```

## iter() next()
```
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

```
## vars() 

the built-in `vars()` function returns the `__dict__` attribute of an object. The `__dict__` attribute is a dictionary that contains the object's namespace (its variables, in simpler terms). If the object has no `__dict__` attribute, `vars()` raises a `TypeError`.

When `vars()` is called without an argument, it behaves like `locals()` and returns a dictionary of the local namespace.

Let's delve into a few examples:

### 1. Using `vars()` without an argument:

This will give us the local namespace. If used at the module level, it will give the global namespace.

```python
x = 10
y = 20

print(vars())
```

You will see something like this:

```
{
    '__name__': '__main__',
    '__doc__': None,
    ... (other module level attributes) ...,
    'x': 10,
    'y': 20
}
```

### 2. Using `vars()` with a custom object:

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

alice = Person('Alice', 30)

print(vars(alice))
```

Output:

```
{
    'name': 'Alice',
    'age': 30
}
```

This gives the dictionary representation of the attributes set in the `alice` object.

### 3. Objects without `__dict__`:

Some built-in objects don't have a `__dict__` attribute. If you call `vars()` on them, you'll get a `TypeError`.

```python
x = 10
print(vars(x))  # Raises TypeError: vars() argument must have __dict__ attribute
```

### Note:

It's essential to use `vars()` judiciously. For instance, modifying the dictionary returned by `vars()` for an object might have unintended side effects, as you would be directly altering the object's attributes.

## eval()
apply an string operation on the variable:

```
x = 1
x=eval('x+1')
```


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

## zip

x = [1, 2, 3]
y = [4, 5, 6]
print(list(zip(x, y)))

### zip() in conjunction with the * operator can be used to unzip a list:
x2, y2 = zip(*zip(x, y))
print(list(x2))

## map

The built-in `map()` function in Python is used to apply a function to all the items in an input list (or any other iterable). It's a way to transform a series of data in a concise manner.

### Syntax:

```python
map(function, iterable, ...)
```

Here, `function` is the function to which the map applies for each item of the iterable.

### Example:

Let's look at some examples to better understand the `map()` function.

**Example 1: Square all items in a list**

```python
def square(n):
    return n * n

numbers = [1, 2, 3, 4, 5]
squared_numbers = map(square, numbers)

print(list(squared_numbers))  # Output: [1, 4, 9, 16, 25]
```

Note that the result of `map()` is a map object, which is an iterator. To get the result as a list, we need to convert it using the `list()` function.

**Example 2: Convert all strings in a list to uppercase**

```python
names = ["alice", "bob", "charlie"]
uppercase_names = map(str.upper, names)

print(list(uppercase_names))  # Output: ['ALICE', 'BOB', 'CHARLIE']
```

**Example 3: Using lambda functions with `map()`**

Often, `map()` is used with lambda functions for quick, one-off transformations:

```python
numbers = [1, 2, 3, 4, 5]
squared_numbers = map(lambda x: x*x, numbers)

print(list(squared_numbers))  # Output: [1, 4, 9, 16, 25]
```

**Example 4: Using multiple iterables with `map()`**

`map()` can also accept multiple iterables, and the function you provide should accept as many arguments as there are iterables. For instance:

```python
a = [1, 2, 3]
b = [4, 5, 6]

result = map(lambda x, y: x + y, a, b)

print(list(result))  # Output: [5, 7, 9]
```

This example adds corresponding elements of two lists together.

These are just a few examples to showcase the versatility and utility of the `map()` function in Python.

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


### string 

a = ["Create" "a" "single" "string" "from" "all" "the" "elements"] 
print(" ".join(a)) 

print('*' * 80)

multiStr = "select * from multi_row \
where row_id < 5"

#startswith, endswith

## id, type() and "is"

#The built-in function id() returns the identity of an object as an integer. This integer usually corresponds to the object’s location in memory, although this is specific to the Python implementation and the platform being used. The is operator compares the identity of two objects.

#The built-in function type() returns the type of an object. 

#The is operator compares the identity of two objects.

a = "Holberton"
b = "Holberton"
print("id(a): ",id(a))
print("id(b): ",id(b))

print("a is b",a is b)# '''comparing the types'''

x=10
y=10
print("id(x) == id(y)",id(x) == id(y))
x = y


print("id(y) == id(10)",id(y) == id(10))

x = x + 1

print("id(x) == id(y)",id(x) == id(y))
print("id(y) == id(10)",id(y) == id(10))


m = list([1, 2, 3])
n = m

print("id(m) == id(n)",id(m) == id(n))
m.pop()
print(m)
print(n)
print("id(m) == id(n)",id(m) == id(n))


Refs [1](https://docs.python.org/3/library/functions.html), [2](https://docs.python.org/3/library/stdtypes.html)

