# Packages
In Python, while modules are individual `.py` files, packages are a way of organizing related modules into a single directory hierarchy. Essentially, a package is a directory that contains multiple module files and a special `__init__.py` file.

### Key Concepts:

1. **Package Creation**:

   A package is simply a directory containing an `__init__.py` file. This file can be empty, or it can contain valid Python code. Its presence indicates that the directory should be treated as a package.

   For instance, consider you have a directory structure as follows:
   ```
   my_package/
   ├── __init__.py
   ├── module1.py
   └── module2.py
   ```

   Here, `my_package` is a package that contains two modules: `module1` and `module2`.

2. **Importing from Packages**:

   To import a module from a package, you use the package name and the module name separated by a dot. 

   ```python
   from my_package import module1
   ```

   Or to import a specific function or class from a module within a package:

   ```python
   from my_package.module1 import my_function
   ```

3. **Subpackages**:

   Packages can also contain subpackages. A subpackage is just a subdirectory containing its own `__init__.py` file.

   For example:
   ```
   my_package/
   ├── __init__.py
   ├── module1.py
   ├── module2.py
   └── subpackage/
       ├── __init__.py
       └── submodule1.py
   ```

   To import from the subpackage:

   ```python
   from my_package.subpackage import submodule1
   ```

4. **`__init__.py` Role**:

   While this file can be empty, it's also the place where package-level variables and functions can be defined. It runs when the package is imported, allowing for package initialization code. For instance, if you want to initialize some package-level data or import submodules by default, you'd do that in `__init__.py`.

5. **`__all__` List in `__init__.py`**:

   You can provide a list named `__all__` in your `__init__.py` file to specify which modules should be imported when `from package import *` is used.

   ```python
   __all__ = ["module1", "module2"]
   ```

### Benefits of Packages:

- **Structured Namespace**: Packages allow you to structure your modules in a hierarchical manner. This avoids module name collisions by providing a qualified namespace.

- **Code Organization**: Just as modules help in organizing related functions and classes, packages help in organizing related modules.

- **Distributed Development**: By splitting a large application into packages (and subpackages), different teams can work on different packages. This makes it easier to develop and maintain large codebases.

- **Reusability**: Like modules, packages can also be reused across different projects. Many third-party tools and libraries are distributed as packages.

In essence, Python packages are a way to distribute and organize larger codebases. They enable the creation of module hierarchies and provide a clean and structured way to represent module dependencies.


In Python, when you import a module or package, the Python interpreter searches for the module or package in a list of directories defined in a system variable named `sys.path`. This variable determines the import search path.

The `sys.path` variable contains the following locations:

1. **The directory of the script being run or the current directory if the interactive shell is used.** This is why scripts can always import other scripts located in the same directory.

2. **The site-packages directory** - where third-party packages are usually installed.

3. **PYTHONPATH directories** - if you set the PYTHONPATH environment variable, its content will be added to the Python import path.

4. **Standard library directories** - where Python’s built-in modules are stored.

5. **.pth files (Path Configuration Files)** - if you have .pth files in your Python's site-packages directory, the paths inside those files will be added to `sys.path`.

6. **Installation-dependent default paths** - defined when Python is installed or compiled.

To view the current `sys.path`, you can do the following:

```python
import sys
print(sys.path)
```

If you want to add a directory to the import path, you can append or prepend the directory to the `sys.path` list. For instance:

```python
sys.path.append("/path/to/my/package_or_module")
```

However, remember that such changes to `sys.path` are temporary and only affect the current Python session. If you want a permanent addition, consider updating the `PYTHONPATH` environment variable or using `.pth` files.





Certainly! A Python package is a way of organizing related modules into a single directory hierarchy. In simpler terms, it's like a folder that contains multiple Python scripts and possibly other nested folders, with the purpose of organizing and grouping related functionalities.

## Anatomy of a Python Package:
1. **Directory/Folder**: The main folder which contains all your Python scripts (or modules). This folder's name will be the name of your package.
2. **`__init__.py` file**: Every directory that wants to be considered a package must contain this file. In older versions of Python, this file used to be mandatory, but since Python 3.3, it's become optional for identifying a directory as a package. However, it's still widely used and can contain initialization code that runs when the package is imported.
3. **Modules**: These are the `.py` scripts that contain your functions, classes, etc.
4. **Subpackages**: These are subdirectories within the main directory, which can also contain their own modules and even further nested subpackages.

## Example:

Imagine you're building a package for mathematical operations. Here's a simple directory structure:

```
math_operations/
|-- __init__.py
|-- arithmetic.py
|-- geometry/
    |-- __init__.py
    |-- area.py
    |-- volume.py
```

1. **`math_operations`** is the main package.
2. **`arithmetic.py`** is a module within the main package that contains basic arithmetic functions.
3. **`geometry`** is a subpackage inside the main package.
4. **`area.py`** and **`volume.py`** are modules inside the `geometry` subpackage.

### Sample code:

`arithmetic.py`
```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

`area.py`
```python
def rectangle(l, w):
    return l * w

def circle(r):
    return 3.14159 * r * r
```

`volume.py`
```python
def cube(s):
    return s ** 3
```

To use the functions from these modules, you'd import them in another script:

```python
from math_operations.arithmetic import add, subtract
from math_operations.geometry.area import rectangle, circle
from math_operations.geometry.volume import cube

print(add(5, 3))  # 8
print(rectangle(5, 4))  # 20
print(circle(3))  # ~28.27431
print(cube(3))  # 27
```

This is a simple example, but in practice, packages can contain many more modules and subpackages, helping you organize large projects in a more maintainable and readable way.



# python import package path 
In Python, when you import a module or package, the Python interpreter searches for the module or package in a list of directories defined in a system variable named `sys.path`. This variable determines the import search path.

The `sys.path` variable contains the following locations:

1. **The directory of the script being run or the current directory if the interactive shell is used.** This is why scripts can always import other scripts located in the same directory.

2. **The site-packages directory** - where third-party packages are usually installed.

3. **PYTHONPATH directories** - if you set the PYTHONPATH environment variable, its content will be added to the Python import path.

4. **Standard library directories** - where Python’s built-in modules are stored.

5. **.pth files (Path Configuration Files)** - if you have .pth files in your Python's site-packages directory, the paths inside those files will be added to `sys.path`.

6. **Installation-dependent default paths** - defined when Python is installed or compiled.

To view the current `sys.path`, you can do the following:

```python
import sys
print(sys.path)
```

If you want to add a directory to the import path, you can append or prepend the directory to the `sys.path` list. For instance:

```python
sys.path.append("/path/to/my/package_or_module")
```

However, remember that such changes to `sys.path` are temporary and only affect the current Python session. If you want a permanent addition, consider updating the `PYTHONPATH` environment variable or using `.pth` files.




# creating setup.py
setup.py is a python file, which usually tells you that the module/package you are about to install. If you have your package tree like:
```
pip install -U
```
or 
```
pip install --user package_name
```
or
```
pip install --install-option="--prefix=$HOME/local" package_name
```
or
```
python setup.py install --user


 foo
 ├── foo
 │   ├── data_struct.py
 │   ├── __init__.py
 │   └── internals.py
 ├── README
 ├── requirements.txt
 ├── scripts
 │   ├── cool
 │   └── skype
 └── setup.py
```

Then, you do the following in your `setup.py` script so that it can be installed on some machine:

```
from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
    name='foo',
    version='1.0',
    description='A useful module',
    license="MIT",
    long_description=long_description,
    author='Man Foo',
    author_email='foomail@foo.com',
    url="http://www.foopackage.com/",
    packages=['foo'],  # same as name
    install_requires=['bar', 'greek'],  # external packages as dependencies
    scripts=[
        'scripts/cool',
        'scripts/skype',
    ]
)
```
a sample available [here](https://github.com/pytorch/vision/blob/master/setup.py) 

[code](../Tutorials/modules_packages)
