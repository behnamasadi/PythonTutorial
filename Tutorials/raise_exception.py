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


#you can simpy call any of the exceptions like this:
#raise MemoryError("some Memory Error")
#raise SystemError("some error")
#raise ValueError("some Value Error")
#raise Exception("some Exception")

try:
	switch:
	#some code
	#here we manually raise some exception but usually they shoudl raised automatically via errors that are happening:
	#raise SystemError("some System error")
	raise MemoryError("some Memory Error")
	#raise ValueError("some Value Error")
	#raise Exception("some Exception")
except MemoryError as err:
	print (err.args)

	
except SystemError as err:
	print(err.args)
	 




