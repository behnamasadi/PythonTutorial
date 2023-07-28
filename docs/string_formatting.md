# Strings
`'foo'` is the same as `"foo"`.


Multi-line strings: 
```
a = """Lorem ipsum dolor sit amet,
consectetur adipiscing elit,
sed do eiusmod tempor incididunt
ut labore et dolore magna aliqua."""
```

# 1. String Formatting (% Operator)
Old Style:

```
name = "behnam"
str = "my name is %s" % name
print(str)
```



# 2. String Formatting (str.format)
```
first_name = "behnam"
last_name = "asadi"
str = "my name is {f} and my last name is {l}".format(
    f=first_name, l=last_name)
print(str)
```
with index:


```
print('The {2} {1} {0}'.format('car','yellow','fast')) 
```


# 3. String Interpolation / f-Strings
you can embed arbitrary Python expressions, you can even do inline arithmetic with it.
```
first_name = "behnam"
last_name = "asadi"
age = 20
str = f"my name is {first_name} and my last name is {last_name}, I'm {age*2}"
print(str)
```

# 4. Template Strings 
It uses Template class from string module. It has a syntax somewhat similar to .format() when done with keywords, but instead of curly braces to define the placeholder, it utilises a dollar sign ($). ${} is also valid and should be in place when a valid string comes after the placeholder.
```
str = Template(
    "my name is $first_name and my last name is $last_name, I'm $age")
var = str.substitute(first_name="behnam", last_name="asadi", age=20)
print(var)
```

