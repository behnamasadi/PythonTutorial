In Python, properties and setters are part of a mechanism to control the access and modification of class attributes. They allow you to define custom behavior when getting and setting attribute values. Properties are used to define a "getter" for an attribute, while setters are used to define a "setter" for an attribute. Let me explain each concept in more detail:

1. Class Attribute:
A class attribute is a variable that belongs to the class.

Example:

```python
class MyClass:
    class_attribute = 10

    def __init__(self, instance_attribute):
        self.instance_attribute = instance_attribute

# Accessing the class attribute using the class name
print(MyClass.class_attribute)  # Output: 10

# Creating instances and accessing instance attributes
obj1 = MyClass(20)
print(obj1.instance_attribute)  # Output: 20
```

2. Property:
Properties allow you to define a custom method to get the value of an attribute. They are useful when you want to perform additional operations or computations before returning the attribute value.

To create a property, you use the `@property` decorator above the getter method.

Example:

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def diameter(self):
        return 2 * self.radius

circle = Circle(5)
print(circle.diameter)  # Output: 10
```

In this example, `diameter` is a property of the `Circle` class, which calculates the diameter based on the `radius` attribute. You can access the property just like a regular attribute.

3. Setter:
Setters allow you to define a custom method to set the value of an attribute. This is useful when you want to perform some validation or transformation before assigning the new value to the attribute.

To create a setter, you use the `@attribute_name.setter` decorator above the setter method.

Example:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius
        
    def getRadius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative.")
        self._radius = value

circle = Circle(5)
circle.radius = 10
print(circle.radius)  # Output: 10
print(circle.getRadius())  # Output: 10 # Getting radius via class method
circle.radius = -5  # Raises ValueError: Radius cannot be negative.
```

In this example, `radius` is a property with both a getter and a setter. The setter ensures that the radius cannot be set to a negative value.

By using properties and setters, you can encapsulate the behavior of attribute access and modification, providing a cleaner and more robust interface to your classes.



[code](../Tutorials/class)
