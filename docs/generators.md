# generators
A generator is a special type of iterator in Python that allows you to iterate over its items only once and does not store all of its items in memory. It is defined using a function, just like a regular function, but instead of returning values using the `return` statement, it uses the `yield` keyword to produce a series of values.

Here's a simple example of a generator:

### Example: Generator to Yield Fibonacci Sequence

```python
def fibonacci_generator(n):
    """Generate the first n numbers in the Fibonacci sequence."""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Using the generator:
fib = fibonacci_generator(5)
for number in fib:
    print(number)

# Output:
# 0
# 1
# 1
# 2
# 3
```

In the above example, the `fibonacci_generator` function is a generator that yields the Fibonacci sequence up to the `n`-th term. When the generator function is called, it returns a generator object (`fib` in this case) without even starting the execution of the function. Only when the generator object is iterated over (e.g., using a `for` loop), the function starts executing until it hits the `yield` keyword. After yielding its value, the function's state is saved, and it can be resumed from where it left off the next time the generator is iterated.

### Benefits of Generators:

1. **Memory Efficiency**: Since generators don't store all their items in memory (they generate them on-the-fly), they can be more memory-efficient than lists or arrays, especially for large data sets.
  
2. **Laziness**: Items are generated one-by-one and only when requested. This can be useful when dealing with infinite sequences or large data streams.

3. **Cleaner Code**: Generators can help simplify code when working with iterative processes, as they provide a clean way to abstract away the iteration logic.
