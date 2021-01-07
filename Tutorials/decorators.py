#Ref:
# https://www.youtube.com/watch?v=r7Dtus7N4pI
# https://www.geeksforgeeks.org/decorators-in-python/

# In Python, functions are objects which means, thats why when you print the function without Parenthesis you would get
#an object address i.e. in print(f1(f)) in the code below

# 1) They can be referenced to, passed to a variable and returned from other functions as well.
# 2) Functions can be defined inside another function and can also be passed as argument to another function.
# Decorators allows you to change the behaviour of a function without modifing the code
# so here we want to extend the functionality of f() with f1()
def f1(input_func):
    def wrapper(*args, **kwargs):
        print("begining of wrapper")
        input_func(*args, **kwargs)
        print("end of wrapper")
    return wrapper


def f(a,b):
    print("hello from f,params are: ",a,b)
print('########################### Function Aliasing ###########################')
f=f1(f)
f(2,3)

print('########################### Function Decorating ###########################')
@f1
def g(a,b):
    print("hello from g,params are: ",a,b)
# here instead of above code everytime we call g(), f1() will be called, because we add @f1 above the g()
g(2,3)
