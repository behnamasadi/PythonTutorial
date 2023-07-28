# module
A module is a file containing Python definitions and statements. 

### Key Concepts:

1. **Module Creation**:
   
   A module is simply a `.py` file. So, if you have a file named `my_module.py`, the file name (minus the `.py` extension) becomes the module name: `my_module`.

2. **Importing Modules**:

   You can use any Python source file as a module by executing an `import` statement in some other Python source file. 
   
   ```python
   import my_module
   ```

   Once you've imported a module, you can access its functions, classes, and variables using the dot notation:

   ```python
   my_module.some_function()
   ```

3. **`from ... import ...` Statement**:

   You can also choose to import specific attributes from a module directly:

   ```python
   from my_module import some_function
   some_function()
   ```

   This way, you don't need to prefix the function with the module name.

4. **Module Search Path**:

   When you try to import a module, Python searches for it in several locations. The search begins in the current directory. If the module isn't found, Python then searches each directory in the shell variable `PYTHONPATH`. If it still can't find it, Python checks the default path, which is generally `/usr/local/lib/python/`.

   The module search path is stored in the system module `sys` as the `sys.path` variable. You can modify this list to add new search paths.
   
	```   
	import sys
	sys.path.append('/path/to/module_file.py')
	print("sys.path:\n", sys.path)
	```

   or 

	``` 
	export PYTHONPATH=$HOME/dirWithScripts/:$PYTHONPATH
	```
	

5. **Built-in Modules**:

   Python comes with a library of standard modules. Some modules are built into the interpreter; these provide access to operations that aren't part of the core of the language but are nevertheless built in, either for efficiency or to provide access to operating system primitives such as system calls. Examples include the `math` and `sys` modules.

6. **`dir()` Function**:

   The built-in function `dir()` is used to find out which names a module defines. It returns a sorted list of strings:

   ```python
   import math
   print(dir(math))
   ```

   This would print all the functions and attributes available in the `math` module.

7. **`__name__` Attribute**:

Every module has a name, and statements in a module can find out the name of their module. This is handy for the particular purpose of figuring out whether the module is being run standalone or being imported into another module. If the module is running standalone, its `__name__` attribute is set to `"__main__"`, if it is running as module `__name__` it is equal to name of the `module_file_name`


## if `__name__==__main__`

the special variable `__name__` is used to determine if a Python file is being run as the main program or if it's being imported as a module into another program. 

### Purpose:

When a Python script is run, `__name__` is set to `"__main__"` for that script. If a module is being imported, `__name__` is set to the module's name.

Using the `if __name__ == "__main__":` check allows authors to distinguish between the two cases, so they can:
1. Write code that can be both used by other programs when imported as a module and
2. Can be run standalone by itself.

This provides a lot of flexibility, enabling the reuse of code across multiple scripts.

### Example:

Let's say we have a file named `math_operations.py`:

```python
# math_operations.py

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

if __name__ == "__main__":
    print(add(10, 5))
    print(subtract(10, 5))
```

Here's what happens:
- If you run the script directly (e.g., `python math_operations.py`), the code under `if __name__ == "__main__":` will execute, and it'll print the results of the `add` and `subtract` functions.
  
- If you import `math_operations` in another script or interactive Python session using `import math_operations`, then the code under `if __name__ == "__main__":` will NOT execute. Only the functions will be available for use.

Example of importing:

```python
# another_script.py

import math_operations

result = math_operations.add(3, 4)
print(result)  # This will print 7, but won't execute the code inside the if __name__ == "__main__": block in math_operations.py
```

This design pattern allows script writers to make their Python files reusable as modules and still be able to run them as standalone programs for testing or other purposes.



## python -m [module-name]

When you run `python -m [module-name]`, Python searches for the named module in the Python standard library, installed packages, and the local directory, then runs its main script.
The `-m` option essentially treats the specified module as a script, running its code in the context of `__main__`. This is why many Python modules include a clause like:

```python
if __name__ == "__main__":
    main()
```

This ensures that if the module is run as a standalone script (whether directly or using the `-m` option), the `main()` function will execute.

### Examples:

1. **Starting an HTTP server for the current directory**: 
   
   This can be helpful for quickly sharing files over a local network.

   ```
   python -m http.server
   ```

   By default, this starts a web server on port 8000. You can specify a different port by adding it after the command, like `python -m http.server 8080`.

2. **Launching the Python package installer (pip)**:
   The command `python -m pip` invokes the `pip` module using the Python interpreter's `-m` switch, which runs library modules as scripts.	
   Although `pip` often has its own command-line entry point, you can also run it with:
   
   ```
   python -m pip install some_package
   ```

3. **Running the interactive Python debugger**:

   ```
   python -m pdb my_script.py
   ```

4. **Executing a zip archive**:

   If you have a zip archive with a `__main__.py` inside, you can run it directly:

   ```
   python -m zipfile_name
   ```

[code](../Tutorials/modules_packages)


   

