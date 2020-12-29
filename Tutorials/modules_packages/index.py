#Modules: Python modules are .py files that consist of Python code. Any Python file can be referenced as a module.
#Packages: is a collection of Modules, the packages name is the directory name,you just need to add a __init__.py file
# importing a package essentially imports the package’s __init__.py file as a module.

#How to use:
#First method:
#   from <package_name> import <Module_name>
#   object=<Module_name>.<Class_name>()

#second method:
#   from <package_name>.<Module_name> import <Class_name>
#   object=<Class_name>()


#The first thing Python will do is look up the name abc in sys.modules. This is a cache of all modules that have been previously imported. If the name isn’t found in the module cache, Python will proceed to search through a list of built-in modules. These are modules that come pre-installed with Python and can be found in the Python Standard Library. If the name still isn’t found in the built-in modules, Python then searches for it in a list of directories defined by sys.path. This list usually includes the current directory, which is searched first.


import sys
sys.path.append('/path/to/module_file.py')
print("sys.path:\n", sys.path)


#or 
# Linux & OSX
#export PYTHONPATH=$HOME/dirWithScripts/:$PYTHONPATH




#################################### Absolute Imports #################################### 

#Let’s say you have the following directory structure:
#└── project
#    ├── package1
#    │   ├── module1.py
#    │   └── module2.py
#    └── package2
#        ├── __init__.py
#        ├── module3.py
#        ├── module4.py
#        └── subpackage1
#            └── module5.py


#Let’s assume the following:

#package1/module2.py contains a function, function1.
#package2/__init__.py contains a class, class1.
#package2/subpackage1/module5.py contains a function, function2.

#This is somewhat similar to its file path, but we use a dot (.) instead of a slash (/).

#from package1 import module1
#from package1.module2 import function1
#from package2 import class1
#from package2.subpackage1.module5 import function2


################################# Relative Imports #################################
#You can only use relative imports inside the same package that you are currently in. If you're not inside a package then relative imports just won't work. 

#1)let's say we are here:
# package1/module1.py

# We can import like followings:
# from .module2 import function1

#2)let's say we are here:
# package2/module3.py

# We can import like followings:
#from . import class1
#from .subpackage1.module5 import function2


from space_package import Planet #from .space_package import Planet doesn't work because we are not inside space_package
my_planet=Planet.planet()
print(my_planet.shape)
my_planet.printInfo(20)
my_planet.comment()
print(Planet.planet.spin())

from space_package.Planet import planet
my_planet=planet()
my_planet.printInfo(20)

from space_package import Calc
from space_package.Calc import plannet_mass

print(f'math of planet {my_planet.name} is:',plannet_mass(my_planet.gravity,my_planet.radius))


import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
#now we can import <package_name>.<Module_name>



