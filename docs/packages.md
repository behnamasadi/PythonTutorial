# Packages
In Python, while modules are individual `.py` files, packages are a way of organizing related modules into a single directory hierarchy. Essentially, a package is a directory that contains multiple module files and a special `__init__.py` file.



### 1. **Package Creation**:

   A package is simply a directory containing an `__init__.py` file. This file can be empty, or it can contain valid Python code. Its presence indicates that the directory should be treated as a package.

   For instance, consider you have a directory structure as follows:
   ```
   my_package/
   ├── __init__.py
   ├── module1.py
   └── module2.py
   ```

   Here, `my_package` is a package that contains two modules: `module1` and `module2`.

### 2. **Importing from Packages**:

   To import a module from a package, you use the package name and the module name separated by a dot. 

   ```python
   from my_package import module1
   ```

   Or to import a specific function or class from a module within a package:

   ```python
   from my_package.module1 import my_function
   ```

### 3. **Subpackages**:

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

### 4. **`__init__.py` Role**:

   While this file can be empty, it's also the place where package-level variables and functions can be defined. It runs when the package is imported, allowing for package initialization code. For instance, if you want to initialize some package-level data or import submodules by default, you'd do that in `__init__.py`.

### 5. **`__all__` List in `__init__.py`**:

   You can provide a list named `__all__` in your `__init__.py` file to specify which modules should be imported when `from package import *` is used.

   ```python
   __all__ = ["module1", "module2"]
   ```

## Package and module path 
In Python, when you import a module or package, the Python interpreter searches for the module or package in a list of directories defined in a system variable named `sys.path`. This variable determines the import search path.

The `sys.path` variable contains the following locations:

1. **The directory of the script being run or the current directory if the interactive shell is used.** This is why scripts can always import other scripts located in the same directory.

2. **The site-packages directory** - where third-party packages are usually installed.

3. **PYTHONPATH directories** - if you set the `PYTHONPATH` environment variable, its content will be added to the Python import path.

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






## python import package path 
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



# Complete example


```
├── LICENSE
├── README.md
├── setup.py
└── space_package
    ├── Calc.py
    ├── __init__.py
    └── Planet.py
```


content of `Calc.py`:

```python
def plannet_mass(gravity,radius):
    mass=(gravity*radius**2/6.67*10**-11)
    return mass


def plannet_volume(radius):
    vol=(4*3.14*radius**2)/2
    return vol
```

content of `Planet.py`:

```python
class planet:
    shape="round"

    def printInfo(self,x=10):
        print(self.shape,x)

    def __init__(self,radius=1,name="earth",gravity=9.8,system="solar"):
        self.radius=radius
        self.name=name
        self.gravity=gravity
        self.system=system

    @classmethod
    def comment(cls):
        return f'All {cls.shape} becuase of gravity'

    @staticmethod
    def spin(speed='2000 miles per hour'):
        return f'The planet spins at {speed}'
```


## Creating setup.py

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

## Creating distribution package
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

You can also create wheel package:


```
python setup.py sdist bdist_wheel
```


## Installation of newly created package

you can install packages as followings:

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

```
Now you can install `space_package-1.0.0` in a separate environment 

```
pip install -U space_package-1.0.0.tar.gz 
```
[code](../Tutorials/modules_packages)


