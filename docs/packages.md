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



# complete example

```
   space_package/
   ├── __init__.py
   ├── Calc.py
   └── Planet.py
```

# creating setup.py


To create a `setup.py` file for a Python package, you need to define the package's metadata, dependencies, and other relevant information. Below is a simple example of a `setup.py` file for a Python package:

```python
from setuptools import setup, find_packages

# Package metadata
NAME = 'your-package-name'
VERSION = '1.0.0'
DESCRIPTION = 'Description of your package'
AUTHOR = 'Your Name'
EMAIL = 'your.email@example.com'
URL = 'https://github.com/yourusername/your-package-repo'
LICENSE = 'MIT'  # Replace with the appropriate license if needed

# Define the required packages and package directories
PACKAGES = find_packages()

# Define the dependencies of your package
INSTALL_REQUIRES = [
    # List your dependencies here, e.g.,
    # 'numpy>=1.18.0',
    # 'requests>=2.25.1',
]

# Additional classifiers that describe your project
CLASSIFIERS = [
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

# Setup function call
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license=LICENSE,
    packages=PACKAGES,
    install_requires=INSTALL_REQUIRES,
    classifiers=CLASSIFIERS,
)
```

Replace the placeholders (`your-package-name`, `Description of your package`, `Your Name`, `your.email@example.com`, etc.) with appropriate values for your package.

In this example, we are using `setuptools` to handle package distribution and dependencies. To create a distributable package, navigate to the directory containing your `setup.py` file in the command line and run the following command:

```
python setup.py sdist
```

This will create a source distribution package in the `dist` directory. You can distribute this package to others, or if you want to upload it to the Python Package Index (PyPI), you can use the `twine` package:

```
pip install twine
twine upload dist/*
```

Remember to ensure that your package's code is organized properly and contains an `__init__.py` file inside each subpackage so that `setuptools` can discover and include them correctly.

Keep in mind that this is a basic setup.py file. Depending on your package's complexity and needs, you may need to include additional configurations like data files, entry points, etc.


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

# use a package without installation 

You can use a Python package without installation by manually adding the package's source code or module files to your project's working directory or any directory included in the Python's module search path. This approach is useful for quick experimentation or when you don't want to perform a formal installation.

Here are the steps to use a Python package without installation:

1. Obtain the package source code: Download the package's source code or obtain it from a version control repository (e.g., GitHub) as a ZIP file.

2. Extract the package: Extract the ZIP file to a directory on your computer.

3. Add the package to the Python path: To use the package in your project, you need to add the package's directory to Python's module search path. This can be done using the `sys.path` variable. For example:

```python
import sys

# Replace 'path/to/package' with the actual path to the package directory
package_path = 'path/to/package'
sys.path.append(package_path)
```

4. Import the package's modules: Now, you can import modules from the package as if it were installed. For example:

```python
# Assuming 'mymodule' is a module within the package
import mymodule

# Use functions, classes, or variables from 'mymodule'
```

5. Use the package: You can now use the package's functions, classes, or variables in your Python code.

Please note that using a package without formal installation may not be suitable for production-level projects or when working with complex packages with external dependencies. Proper package installation using `pip` or `setuptools` is recommended for most scenarios.

Additionally, be aware that updates to the package won't be automatically reflected in your project unless you manually update the package files in your project directory.

[code](../Tutorials/modules_packages)
