
In Python, "mutable" refers to objects whose value or state can be altered after they are created, while "immutable" refers to objects whose value or state cannot be changed once they are created. 

### Mutable Examples:
Common mutable objects in Python include:
1. Lists
2. Dictionaries
3. Sets

#### List (Mutable) Example:
```python
# Create a list
list_example = [1, 2, 3, 4]

# Modify the list
list_example[2] = 99

print(list_example)  # Outputs: [1, 2, 99, 4]
```

Here, we changed the third element of the list from 3 to 99, so the list's state was mutable.

### Immutable Examples:
Common immutable objects in Python include:
1. Integers
2. Floats
3. Strings
4. Tuples

#### String (Immutable) Example:
```python
string_example = "hello"

# Try to modify the string
try:
    string_example[0] = "H"
except TypeError as e:
    print(f"Error: {e}")

# Outputs: Error: 'str' object does not support item assignment
```

Here, we tried to change the first letter of the string from 'h' to 'H'. However, strings are immutable in Python, so this operation raises a `TypeError`.

### Why does this distinction matter?

1. **Performance**: Some operations are more efficient on immutable objects. For instance, because strings are immutable, Python can optimize memory use and performance for string operations.
 
2. **Safety**: Immutable objects are inherently safe from unintended side effects. If you pass an immutable object to a function, you can be sure it won't be changed within that function, which can help prevent bugs.

3. **Dictionary Keys**: Only immutable objects can be used as dictionary keys. This is because a mutable object might change its value, making it hard or impossible to find later in the dictionary.
