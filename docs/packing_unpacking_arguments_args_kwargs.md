# Packing and Unpacking Arguments 
Python permits us to pack and unpack values from iterables in a single assignment.



- `*`: for tuples 
- `**`: for dictionaries.

Let say we have this function:
```
def foo(a, b, c, d):
    return
```
and this is our input:
```
l = [1, 2, 3, 4]
```
so this won't work:
```
foo(l)
```
you have to unpack it:


```
foo(*l)
```


`*args` and `**kwargs` are special syntax in Python for passing a variable number of arguments to a function. 

- `*args` is used to send a non-keyworded variable-length argument list to the function.
- `**kwargs` is used to send a keyworded variable-length argument list to the function.

Let's look at examples of both:

## *args

```python
def add_all(*args):
    total = 0
    for num in args:
        total += num
    return total

print(add_all(1, 2, 3, 4, 5))  # Output: 15
```

In the `add_all` function, `*args` allows us to pass a variable number of arguments. In this case, it takes all the passed numbers and sums them. 

## **kwargs

```python
def person_details(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

person_details(name="John", age=25, country="USA")
```

Output:
```
name: John
age: 25
country: USA
```

Here, `**kwargs` allows us to pass any number of keyword arguments (like `name="John"`, `age=25`, etc.) to the `person_details` function.

## Using *args and **kwargs together

You can use `*args` and `**kwargs` in the same function. Here's how:

```python
def func(*args, **kwargs):
    for arg in args:
        print(arg)
    
    for key, value in kwargs.items():
        print(f"{key}: {value}")

func(1, 2, 3, name="John", country="USA")
```

Output:
```
1
2
3
name: John
country: USA
```

Here, `*args` catches non-keyword arguments and `**kwargs` catches keyword arguments. Note that the order matters. `*args` must come before `**kwargs` in the function definition.
