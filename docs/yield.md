# yield
The yield statement suspends function’s execution and sends a value back to caller, but retains enough state to enable function to resume where it is left off.
We should use yield when we want to iterate over a sequence, but don’t want to store the entire sequence in memory.

```
def simpleYieldFunction():
	yield 1
	yield 2
	yield 3

numbers=simpleYieldFunction()
for i in numbers:
	print(i)

numbers=simpleYieldFunction()
print(numbers.__next__())
print(numbers.__next__()) 
print(numbers.__next__())

```
Yield are used in Python generators. A generator function is defined like a normal function, but whenever it needs to generate a value, it does so with the yield keyword rather than return. If the body of a def contains yield, the function automatically becomes a generator function.

```
def infinitSquare():
	i=1
	while True:
		yield i*i
		i += 1  # Next execution resumes from this point   
numbers=infinitSquare()
for i in numbers:
	print(i)
	if i>100:
		break
```
