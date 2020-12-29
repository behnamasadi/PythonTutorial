#a mutable object can be changed after it is created, and an immutable object can’t
#Objects of built-in types like (int, float, bool, str, tuple, unicode) are immutable. 
#Objects of built-in types like (list, set, dict) are mutable.


############################ id, type() and "is" ############################

#The built-in function id() returns the identity of an object as an integer. This integer usually corresponds to the object’s location in memory, although this is specific to the Python implementation and the platform being used. The is operator compares the identity of two objects.

#The built-in function type() returns the type of an object. 

#The is operator compares the identity of two objects.

a = "Holberton"
b = "Holberton"
print("id(a): ",id(a))
print("id(b): ",id(b))

print("a is b",a is b)# '''comparing the types'''

x=10
y=10
print("id(x) == id(y)",id(x) == id(y))
x = y


print("id(y) == id(10)",id(y) == id(10))

x = x + 1

print("id(x) == id(y)",id(x) == id(y))
print("id(y) == id(10)",id(y) == id(10))


m = list([1, 2, 3])
n = m

print("id(m) == id(n)",id(m) == id(n))
m.pop()
print(m)
print(n)
print("id(m) == id(n)",id(m) == id(n))




























