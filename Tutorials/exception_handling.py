########################## Raising an Exception ##########################
#We can use raise to throw an exception 

x=1
if x>5:
	raise Exception("x should be smaller than 5")


########################## Handling Exceptions ##########################
#https://docs.python.org/3/library/exceptions.html#exception-hierarchy
#BaseException
# +-- SystemExit
# +-- KeyboardInterrupt
# +-- GeneratorExit
# +-- Exception
#      +-- StopIteration
#      +-- StopAsyncIteration
#      +-- ArithmeticError
#      |    +-- FloatingPointError
#      |    +-- OverflowError
#      |    +-- ZeroDivisionError
#      +-- AssertionError
#      +-- AttributeError
#      +-- BufferError
#      +-- EOFError
#      +-- ImportError
#      |    +-- ModuleNotFoundError
#      +-- LookupError
#      |    +-- IndexError
#      |    +-- KeyError
#      +-- MemoryError
#      +-- NameError
#      |    +-- UnboundLocalError
#      +-- OSError
#      |    +-- BlockingIOError
#      |    +-- ChildProcessError
#      |    +-- ConnectionError
#      |    |    +-- BrokenPipeError
#      |    |    +-- ConnectionAbortedError
#      |    |    +-- ConnectionRefusedError
#      |    |    +-- ConnectionResetError
#      |    +-- FileExistsError
#      |    +-- FileNotFoundError
#      |    +-- InterruptedError
#      |    +-- IsADirectoryError
#      |    +-- NotADirectoryError
#      |    +-- PermissionError
#      |    +-- ProcessLookupError
#      |    +-- TimeoutError
#      +-- ReferenceError
#      +-- RuntimeError
#      |    +-- NotImplementedError
#      |    +-- RecursionError
#      +-- SyntaxError
#      |    +-- IndentationError
#      |         +-- TabError
#      +-- SystemError
#      +-- TypeError
#      +-- ValueError
#      |    +-- UnicodeError
#      |         +-- UnicodeDecodeError
#      |         +-- UnicodeEncodeError
#      |         +-- UnicodeTranslateError
#      +-- Warning
#           +-- DeprecationWarning
#           +-- PendingDeprecationWarning
#           +-- RuntimeWarning
#           +-- SyntaxWarning
#           +-- UserWarning
#           +-- FutureWarning
#           +-- ImportWarning
#           +-- UnicodeWarning
#           +-- BytesWarning
#           +-- ResourceWarning


######################## Structure of try and except Block ########################
#The order should bealways like that, any other order will cause a syntax error
#At a time only one exception is caught, 

#try:
	#python run the code here

#except:
	#runs if the exception occures in the try block
#except <Exception 1>:
#.
#.
#.
#except <Exception N>:
	
#else:
	#The else part is executed when no exception occurs.

#finally:
	#runs always, regardless of everything


########################## Properly ignore exceptions ##########################
try:
  doSomething()
except: 
  pass


print("########################## Catching multiple: IndexError, ZeroDivisionError ##########################")
value = [1, 2, 3, 4, 5] 
try: 
    value = value[5]/0
except (IndexError, ZeroDivisionError): 
    print('IndexError or ZeroDivisionError') 
else: 
    print('no exceptions happened') 
finally: 
    print('I will be run anyhow')


print("########################## ValueError,TypeError ##########################")

r=-10
try:
	if type(r) not in [int, float]:
		raise TypeError("The value must be a real number.")	
	if r<0:
		raise ValueError("The value cannot be negative!")

except (TypeError,ValueError )as err:
	print(err)



print("########################## FileNotFoundError ##########################")


import logging

logging.basicConfig(level=logging.DEBUG, filename='data/exception_handling.log', filemode='w')
logger=logging.getLogger()


def reading_file(file_name):
	access_mode='rb'
	try:
		f=open(file_name,access_mode)
		data=f.read()
		return data
	except FileNotFoundError as err:
		print(err)
		logger.error( err)
	else:
		f.close()
	finally:
		pass
reading_file(file_name="data/some_file")

print("########################## AssertionError ##########################")
try: 
	assert(1==0)
except AssertionError as err:
	print(err)
	print("Assertion failed!")
	
else:
	print("Assertion suceed!")


print("########################## AttributeError ##########################")
class Bird:
	pass

bird=Bird()
try:
    bird.quack()
except AttributeError:
    print("AttributeError")





