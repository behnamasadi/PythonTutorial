'''algebra module'''


def mean(x, y):
    return (x+y)/2


def sum_numbers(*numbers):
    sum = 0
    for n in numbers:
        sum = sum+n
    return sum


if __name__ == "__main__":
    x = 2, 3, 5
    print(sum(1, 2, 3, 8))
    print(sum(*x))
