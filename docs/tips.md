### suppress scientific notation

```
x = 1.0
y = 100000000.0    
print (x/y)

print ('%f' % (1/10**8))
print ( '{0:f}'.format(x/y))
```

### suppress scientific notation in Numpy
Suppress Scientific Notation in Numpy When Creating Array From Nested List
```
import numpy as np
np.set_printoptions(suppress=True)
```

### suppress warnings
```
import warnings
warnings.filterwarnings('ignore')
```

### Understanding the underscore _ 

There are 5 cases for using the underscore in Python.

1. storing the value of last expression in interpreter.
```
>>> 10 
10 
>>> _ 
10
```

2. ignoring the specific values. (so-called “I don’t care”)
x, _, y = (1, 2, 3) # x = 1, y = 3

3. To give special meanings and functions to name of variables or functions.  The PEP8 which is Python convention guideline introduces the following 4 naming cases.

	3.1.   "_single_leading_underscore": 

	This convention is used for declaring private variables, functions, methods and classes in a module.
	Anything with this convention are ignored in from module import *. However, of course, Python does not supports truly private, 
	so we can not force somethings private ones and also can call it directly from other modules. So sometimes we say it “weak internal use indicator”.

	3.2. single_trailing_underscore_: 
	 This convention could be used for avoiding conflict with Python keywords or built-ins.
	 
	 ```python
		 Avoid conflict with 'class' keyword
		 func(master, class_='ClassName')
	 ``` 

	3.3. "__double_leading_underscore": 
	This is about syntax rather than a convention. double underscore will mangle the attribute names of a class to avoid conflicts of attribute names between classes. (so-called “mangling” that 		means that the compiler or interpreter modify the variables or function names with some rules, not use as it is) 
	The mangling rule of Python is adding the “_ClassName” to front of attribute names are declared with double underscore. 
	That is, if you write method named “__method” in a class, the name will be mangled in “_ClassName__method” form.
```
class A:
	def _single_method(self):
        	pass    
	def __double_method(self): # for mangling
        	print("my full name is: _A__double_method")
class B(A):
	def __double_method(self): # for mangling
        	pass


a=A()
a._A__double_method()
```
	3.4. __double_leading_and_trailing_underscore__: __file__, __eq__, __init__, __len__
	#This convention is used for special variables or methods (so-called “magic method”) such as__init__, __len__. These methods provides special syntactic features or does special things. For 		example, __file__ indicates the location of Python file, __eq__ is executed when a == b expression is excuted. 
	#A user of course can make custom special method, it is very rare case, but often might modify the some built-in special methods. (e.g. You should initialize the class with __init__ that will 	#be executed at first when a instance of class is created.)

4. To use as ‘Internationalization(i18n)’ or ‘Localization(l10n)’ functions.

5. To separate the digits of number literal value:

numbers using underscore for readability.

```
dec_base = 1_000_000
bin_base = 0b_1111_0000
hex_base = 0x_1234_abcd
print("1_000_000==", dec_base) # 1000000
print(bin_base) # 240
print(hex_base) # 305441741
```


#### Performance Measurement
```
from timeit import Timer
print("start time:", Timer().timeit())
[i*i for i in range(0,100000)] 
print("end time:",  Timer().timeit())
```

#### the `__file__` variable

When a module is loaded in Python, `__file__` is set to its name. You can then use that with other functions to find the directory that the file is located in.

```
import os

print("name of the running file: ",__file__)
print("the parent directory of the directory where program resides: ",os.path.join(os.path.dirname(__file__), '..'))
print("the canonicalised (?) directory where the program resides:",os.path.dirname(os.path.realpath(__file__)))
print("the absolute path of the directory where the program resides",os.path.abspath(os.path.dirname(__file__)))
```

#### What does the  `__name__ == “__main__”`: do

Before executing code, Python interpreter reads source file and define few special variables/global variables.
If the python interpreter is running that module (the source file) as the main program, it sets the special `__name__` variable to have a value “__main__”. 
If this file is being imported from another module, `__name__` will be set to the module’s name.


```
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import modules_packages.myscript 
#print(__name__)
```


####  python -m
```
python -m <module-name> args
Search sys.path for the named module and execute its contents as the __main__ module.
It will execute the content after:
if __name__ == "__main__"


python -m <pkg> args
python interpretor will looking for a __main__.py file in the package path to execute. It's equivalent to:
python path_to_package/__main__.py somearguments
```






### "with" keyword

In python the "with" keyword is used when working with unmanaged resources (like file streams). The with statement clarifies code that previously would use `try...finally` blocks to ensure that clean-up code is executed.

```
with expression [as variable]:
    with-block
```
#### file handling 
  
without using with statement 
```
file = open('file_path', 'w') 
file.write('hello world !') 
file.close() 
```
  
without using with statement 
```
file = open('file_path', 'w') 
try: 
    file.write('hello world') 
finally: 
    file.close() 
```
using with statement 
```
with open('file_path', 'w') as file: 
    file.write('hello world !')
```


```
import socket

host = "localhost"
port = 80

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(b'hello, world')


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.connect((host, port))
    s.sendall(b'hello, world')
finally:
    s.close()
```



### PEP 8 Style Guide for Python Code

Refs [1](https://www.python.org/dev/peps/pep-0008/)






### Most Frequent Value In A List
```
test = [1, 2, 3, 4, 2, 2, 3, 1, 4, 4, 4] 
print(max(set(test), key = test.count))


from  collections import Counter
list_of_words=['a','a','b' ,'c' , 'b', 'a' ,'a','b']
c=Counter(list_of_words)
print("Top two most common elements are:",c.most_common(2))
```
 

### Check The Memory Usage Of An Object

```
import sys
l=[2,3,4]
print(sys.getsizeof(l))
```

import itertools
a = [[1, 2], [3, 4], [5, 6]]
print(list(itertools.chain.from_iterable(a)))


### Setup File Sharing

```
python3 -m http.server
```

### Difference between zip(list) and zip(*list)

zip wants a bunch of arguments to zip together, The * in a function call "unpacks" a list (or other iterable), 
making each of its elements a separate argument. So without the *, you're doing zip( [[1,2,3],[4,5,6]] ).
With the *, you're doing zip([1,2,3], [4,5,6]).

```
p = [[1,2,3],[4,5,6]]
d=zip(*p)
```


[(1, 4), (2, 5), (3, 6)]



### Arguments default
arguments default are defined when function is defined not when it's run 

```
def append(n, l=[]):
    l.append(n)
    return l


print(append(0))
print(append(1))
```
This will give you:

```
[0]
[0, 1]
```
The correction:

```
def append(n, l=None):
    if l is None:
        l = []
    l.append(n)
    return l
```


## is None
In Python, `None` is a special constant that represents the absence of a value. It is used to indicate that a variable or expression does not have a valid value or points to nothing. You can use the `is` keyword to check if a variable is referring to the `None` object. Here's an example of how to use `is None`:

```python
def check_if_none(value):
    if value is None:
        print("The value is None.")
    else:
        print(f"The value is: {value}")

# Example usage:
value1 = None
value2 = 42

check_if_none(value1)  # Output: The value is None.
check_if_none(value2)  # Output: The value is: 42
```

Here are some scenarios where you might want to use `is None`:

1. **Default parameter values**: If you have a function that accepts optional arguments and wants to check if a parameter was provided by the caller or if it's missing (None is often used as the default value).

2. **Testing for existence or validity**: You can use `is None` to check if a variable has been initialized or set to a value. For example, in file handling, you might check if a file object is valid before performing operations on it.

3. **Returning values from functions**: Sometimes, functions return None to indicate failure or no useful result. Checking the return value with `is None` can help you handle such cases appropriately.

4. **Clearing references**: When you want to explicitly release the reference to an object, you can set it to None. This can be helpful in managing memory usage in certain situations.

It's important to note that `is None` is different from `== None`. The former checks for identity (whether two objects are the same), while the latter checks for equality (whether two objects have the same value). For None, these two checks will typically give the same result, but it's generally recommended to use `is None` for clarity and to avoid potential pitfalls when dealing with custom classes that might override the equality comparison. 

Sure! Let's create an example for each case:

1. **Default parameter values**:

```python
def greet(name=None):
    if name is None:
        print("Hello, stranger!")
    else:
        print(f"Hello, {name}!")

# Example usage:
greet()          # Output: Hello, stranger!
greet("Alice")   # Output: Hello, Alice!
```

2. **Testing for existence or validity**:

```python
def process_file(file_path):
    try:
        with open(file_path, 'r') as file:
            # Process the file here
            print(f"File '{file_path}' processed successfully.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found or unable to read.")

# Example usage:
file_path1 = "data.txt"
file_path2 = "non_existent_file.txt"

process_file(file_path1)   # Output: File 'data.txt' processed successfully.
process_file(file_path2)   # Output: File 'non_existent_file.txt' not found or unable to read.
```

3. **Returning values from functions**:

```python
def divide(a, b):
    if b == 0:
        return None
    else:
        return a / b

# Example usage:
result1 = divide(10, 2)
result2 = divide(10, 0)

if result1 is not None:
    print(f"Result1: {result1}")  # Output: Result1: 5.0
else:
    print("Error: Division by zero.")

if result2 is not None:
    print(f"Result2: {result2}")
else:
    print("Error: Division by zero.")  # Output: Error: Division by zero.
```

4. **Clearing references**:

```python
def heavy_computation():
    # Some time-consuming computation
    result = 42
    return result

# Example usage:
result1 = heavy_computation()
print(f"Result1: {result1}")  # Output: Result1: 42

result1 = None  # Clearing the reference to the result
# At this point, the result of heavy_computation() is no longer accessible

result2 = heavy_computation()
print(f"Result2: {result2}")  # Output: Result2: 42
```

In the last example, by setting `result1` to `None`, we release the reference to the previous result of `heavy_computation()`, allowing the garbage collector to free up the memory if there are no other references to the same object. When we call `heavy_computation()` again and store the result in `result2`, it creates a new object in memory.


### timing with time.perf_counter()

```
import time
start = time.perf_counter()
time.sleep(3)
end = time.perf_counter()
print(end-start)
```

### tips

`~x` is equivalent to `-(x+1)`.

```
x = 10
print(~x)
print(-(x+1))
```

This
```
list1 = [1, 2, 3]
print(list1*3)
```
will give you this:
```
[1, 2, 3, 1, 2, 3, 1, 2, 3]
```
This will give you `False`:
```
print(0.1+0.2 == 0.3)
```


instead of iterating with keys:
```
dictionary1 = {'GFG': 1, 'Google': 2, 'GFG': 3}
print(dictionary1['GFG'])
```

iterate over `items()`:

```
temp = {'GFG': 1, 'Facebook': 2, 'Google': 3}
for (key, values) in temp.items():
    print(key, values, end=" ")
```


**There is no operator ++ in Python**



## Google style guide

### importing

```
from package import module

module.function()
```

### main

```
def main():
    ...

if __name__ == '__main__':
    main()
```


Refs: [1](https://google.github.io/styleguide/pyguide.html)
