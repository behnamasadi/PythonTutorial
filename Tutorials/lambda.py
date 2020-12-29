#A lambda function can take any number of arguments, but can only have one expression.
#Syntax
#lambda arguments : expression

adder= lambda a,b: a+b
print(adder(10,15))


f = lambda x: x*x
x=[f(x) for x in range(10)]

for i in x:
	print(i)

z=[1 for x in range(10)]
print (z)
z=[x for x in range(10)]
print (z)


#Both list.sort() and sorted() have a key parameter to specify a function to be called on each list element prior to making comparisons.
#The value of the key parameter should be a function that takes a single argument and returns a key to use for sorting purposes.

student_tuples = [
	('john', 'A', 15),
	('jane', 'B', 12),
	('dave', 'B', 10),
	]
sorted(student_tuples, key=lambda student: student[2])  # sort by age
print(student_tuples)
