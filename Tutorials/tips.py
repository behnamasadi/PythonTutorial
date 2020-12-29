##########################no_ascii character error ##########################

#
# -*- coding: utf-8 -*-

# τ

########################## suppress scientific notation ##########################

x = 1.0
y = 100000000.0    
print (x/y)

print ('%f' % (1/10**8))
print ( '{0:f}'.format(x/y))

########################## suppress warnings ##########################
import warnings
warnings.filterwarnings('ignore')

########################## Understanding the underscore( _ )  ##########################
print("########################## Understanding the underscore( _ )  ##########################")
#There are 5 cases for using the underscore in Python.




 

#1) storing the value of last expression in interpreter.
#>>> 10 
#10 
#>>> _ 
#10

#2)ignoring the specific values. (so-called “I don’t care”)
x, _, y = (1, 2, 3) # x = 1, y = 3

#3) To give special meanings and functions to name of vartiables or functions.  The PEP8 which is Python convention guideline introduces the following 4 naming cases.
	#3-1)_single_leading_underscore: 
	#This convention is used for declaring private variables, functions, methods and classes in a module.
	#Anything with this convention are ignored in from module import *. #However, of course, Python does not supports truly private, 
	#so we can not force somethings private ones and also can call it directly from other modules. So sometimes we say it “weak internal use indicator”.

	#3-2)single_trailing_underscore_: 
	# This convention could be used for avoiding conflict with Python keywords or built-ins.
	# func(master, class_='ClassName') # Avoid conflict with 'class' keyword

	#3-3) __double_leading_underscore: 
	#This is about syntax rather than a convention. double underscore will mangle the attribute names of a class to avoid conflicts of attribute names between classes. (so-called “mangling” that 		means that the compiler or interpreter modify the variables or function names with some rules, not use as it is) 
	#The mangling rule of Python is adding the “_ClassName” to front of attribute names are declared with double underscore. 
	#That is, if you write method named “__method” in a class, the name will be mangled in “_ClassName__method” form.

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

	#3-4)__double_leading_and_trailing_underscore__: __file__, __eq__, __init__, __len__
	#This convention is used for special variables or methods (so-called “magic method”) such as__init__, __len__. These methods provides special syntactic features or does special things. For 		example, __file__ indicates the location of Python file, __eq__ is executed when a == b expression is excuted. 
	#A user of course can make custom special method, it is very rare case, but often might modify the some built-in special methods. (e.g. You should initialize the class with __init__ that will 	#be executed at first when a instance of class is created.)

#4)To use as ‘Internationalization(i18n)’ or ‘Localization(l10n)’ functions.

#5) To separate the digits of number literal value:
#numbers using underscore for readability.

dec_base = 1_000_000
bin_base = 0b_1111_0000
hex_base = 0x_1234_abcd
print("1_000_000==", dec_base) # 1000000
print(bin_base) # 240
print(hex_base) # 305441741




########################## Performance Measurement ##########################
print("########################## Performance Measurement ##########################")
from timeit import Timer
print("start time:", Timer().timeit())
[i*i for i in range(0,100000)] 
print("end time:",  Timer().timeit())


##########################  the __file__ variable  ##########################

#When a module is loaded in Python, __file__ is set to its name. You can then use that with other functions to find the directory that the file is located in.

import os
print("##########################  the __file__ variable  ##########################")
print("name of the running file: ",__file__)
print("the parent directory of the directory where program resides: ",os.path.join(os.path.dirname(__file__), '..'))
print("the canonicalised (?) directory where the program resides:",os.path.dirname(os.path.realpath(__file__)))
print("the absolute path of the directory where the program resides",os.path.abspath(os.path.dirname(__file__)))


########################## What does the if __name__ == “__main__”: do ##########################
# Before executing code, Python interpreter reads source file and define few special variables/global variables.
# If the python interpreter is running that module (the source file) as the main program, it sets the special __name__ variable to have a value “__main__”. 
# If this file is being imported from another module, __name__ will be set to the module’s name.



import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import modules_packages.myscript 
#print(__name__)




########################## How do I make a python script executable? ##########################
# to run a python script with my own command line name like 'myscript' without having to do 'python myscript.py' in the terminal
#1) Add a shebang line to the top of the script:
#!/usr/bin/env python

#2) Mark the script as executable:
#chmod +x myscript.py

#3)Add the dir containing it to your PATH variable. (If you want it to stick, you'll have to do this in .bashrc or .bash_profile in your home dir.)

#export PATH=/path/to/script:$PATH


########################## python -m ##########################

#python -m <module-name> args
#Search sys.path for the named module and execute its contents as the __main__ module.
#It will execute the content after:
#if __name__ == "__main__"


#python -m <pkg> args
#python interpretor will looking for a __main__.py file in the package path to execute. It's equivalent to:
#python path_to_package/__main__.py somearguments







########################## "with" keyword  ##########################

#In python the "with" keyword is used when working with unmanaged resources (like file streams). The with statement clarifies code that previously would use try...finally blocks to ensure that clean-up code is executed.

#with expression [as variable]:
#    with-block

# file handling 
  
# 1) without using with statement 
file = open('file_path', 'w') 
file.write('hello world !') 
file.close() 
  
# 2) without using with statement 
file = open('file_path', 'w') 
try: 
    file.write('hello world') 
finally: 
    file.close() 

# using with statement 
with open('file_path', 'w') as file: 
    file.write('hello world !')



#PEP 8 Style Guide for Python Code
#https://www.python.org/dev/peps/pep-0008/



#~x is equivalent to -(x+1).

#list1=[1,2,3] 
#print(list1*3)

#print(0.1+0.2==0.3)

#class Geeks: 
#    def __init__(self, id): 
#        self.id = id
  
#manager = Geeks(100) 
#manager.__dict__['life'] = 49
#print ( manager.life + len(manager.__dict__))


#list1 = range(100, 110) #statement 1 
#print ("index of element 105 is : ", list1.index(105))  #statement 2 



#data = 50
#try: 
#    data = data/10
#except ZeroDivisionError: 
#    print('Cannot divide by 0 ', end = '') 
#finally: 
#    print('GeeksforGeeks ', end = '') 
#else: 
#    print('Division successful ', end = '')



#dictionary1 = {'GFG' : 1, 'Google' : 2, 'GFG' : 3 } 
#print(dictionary1['GFG'])



#temp = {'GFG' : 1, 'Facebook' : 2, 'Google' : 3 } 
#for (key, values) in temp.items(): 
#    print(key, values, end = " ") 



################################## There is no operator ++ in Python #########################


################################## Most Frequent Value In A List #########################
test = [1, 2, 3, 4, 2, 2, 3, 1, 4, 4, 4] 
print(max(set(test), key = test.count))


from  collections import Counter
list_of_words=['a','a','b' ,'c' , 'b', 'a' ,'a','b']
c=Counter(list_of_words)
print("Top two most common elements are:",c.most_common(2))
 

################################## Check The Memory Usage Of An Object. #########################
import sys
l=[2,3,4]
print(sys.getsizeof(l))


import itertools
a = [[1, 2], [3, 4], [5, 6]]
print(list(itertools.chain.from_iterable(a)))


################################## Setup File Sharing ##################################

#python3 -m http.server



