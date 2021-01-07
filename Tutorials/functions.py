################################# *args and **kwargs in Python #################################

#What *args allows you to do is take in more arguments than the number of formal arguments that you previously defined. With *args, any number of extra arguments can be tacked on to your current formal parameters (including zero extra arguments).


def adder(*arg):
	sum=0
	for numbers in arg:
		sum+=numbers
	return sum

list_of_numbers=[1,2,3]
print(adder( *list_of_numbers ) )

	
#The special syntax **kwargs in function definitions in python is used to pass a keyworded, variable-length argument list. We use the name kwargs with the double star. The reason is because the double star allows us to pass through keyword arguments (and any number of them).

	
def parseFunctionsParameter(**kwarg):
	for key,value in kwarg.items():
		print( "given parameter is {} and value is {}".format(key, value))




parseFunctionsParameter(color='blue', size='10', font='arial')


################################# call by value/ call by reference #################################

#one easy solution:

def increaser(x):
    x[0] = x[0]+1

x = [1]
increaser(x)
print (x)


#https://www.youtube.com/watch?v=-Zy18QEFm6s
#https://www.youtube.com/watch?v=z_55F4zSjoA
a=5
def increase_number(n):
	n+=1
	return

def clear_it(l):
	l=[]
	return

def append_it(l):
	l.append(1)
	return


	












