# Context manager
context manager is a mechanism that's commonly used to allocate and deallocate resources, such as opening and closing a file, acquiring and releasing a lock, or establishing and tearing down a network connection.

You might have already seen this in use with the `with` statement. Here's a classic example with file handling:

```python
with open("myfile.txt", "r") as file:
    data = file.read()
    # File is still open within this block and you can read or write as needed.
# Outside the block, the file is automatically closed.
```

In the above example, the `open()` function returns a context manager that ensures the file is closed when the block of code exits, regardless of whether the exit was due to successful completion or because of an exception.

### How Does a Context Manager Work?

A context manager is any Python object that implements the methods `__enter__()` and `__exit__()`. 

- The `__enter__` method is what's executed when the `with` block is entered.
- The `__exit__` method is what's executed as the block is exited.

### Creating Your Own Context Manager

Let's take an example of a simple context manager that measures the execution time of a code block.

```python
import time

class TimerContextManager:
    def __enter__(self):
        self.start_time = time.time()
        return self  # this is optional

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        print(f"Elapsed time: {self.end_time - self.start_time} seconds")

# Usage
with TimerContextManager():
    # Some long running operations
    time.sleep(2)
```

When the code within the `with` block finishes running (in this case, a sleep for 2 seconds), the context manager will print out the time it took.

### Using contextlib

Python also provides a module named `contextlib` that has utilities to create context managers without the need to create a class. The most commonly used utility is `contextmanager` as a decorator.

Here's how you'd implement the above TimerContextManager using `contextlib`:

```python
from contextlib import contextmanager
import time

@contextmanager
def timer_context():
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"Elapsed time: {end_time - start_time} seconds")

# Usage
with timer_context():
    time.sleep(2)
```

In this case, the code before the `yield` is what would be in `__enter__`, and the code after the `yield` is what would be in `__exit__`.

Context managers are a powerful tool in Python and can help in making code cleaner and ensuring that resources are used optimally.

[code](Tutorials/with_statement_contex_manager_contextlib.py)
