### Python Example

In Python, you can use the `json` module to serialize a class object. You typically need to convert the class instance to a dictionary first:

```python
import json

class MyClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def to_dict(self):
        return {"name": self.name, "age": self.age}

# Create an instance of MyClass
obj = MyClass("John Doe", 30)

# Convert the object to a dictionary
obj_dict = obj.to_dict()

# Serialize the dictionary to a JSON string
json_str = json.dumps(obj_dict)

# Write the JSON string to a file
with open("data.json", "w") as file:
    file.write(json_str)
```

