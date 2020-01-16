# decorators.py
from time import perf_counter


def counter(fn):
    """A simple decorator to count the number of function calls for a given function"""
    count = 0

    def inner(*args, **kwargs):
        nonlocal count
        count += 1
        out = fn(*args, **kwargs)
        return out

    return inner


def timer(fn):
    """A simple decorator to record the total time spent running a given function over the lifetime __main__ call"""
    elapsed = 0

    def inner(*args, **kwargs):
        nonlocal elapsed
        start = perf_counter()
        out = fn(*args, **kwargs)
        end = perf_counter()
        elapsed += (end - start)
        return out

    return inner
