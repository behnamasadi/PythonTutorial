
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


### Integers (int)

When you perform operations on an integer in Python, a new integer object is created. Let's see this in action with an example:

```python
a = 3
print(id(a))  # id() function returns the unique identifier of an object

a += 2
print(id(a))  # The id is different, meaning a new object has been created
```

In this example, `a` initially points to an integer object with the value `3`. When we add `2` to `a`, instead of changing the value of the existing object, Python creates a new integer object with the value `5` and updates `a` to reference this new object.

### Floating-Point Numbers (float)

Floating-point numbers (`float`) in Python work similarly to integers in terms of immutability. When a floating-point number is changed, a new object is created.

```python
b = 2.5
print(id(b))

b *= 2
print(id(b))  # Different id, hence a new float object
```

In this example, `b` initially references a `float` object with the value `2.5`. After multiplying `b` by `2`, Python creates a new `float` object with the value `5.0` and `b` is updated to reference this new object.

