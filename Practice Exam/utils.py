from functools import update_wrapper
from time import clock



def decorator(f):
    return lambda g: update_wrapper(f(g), g)


def memo(f):
    "Memoization decorator."

    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return f(*args)

    return _f


def timedcall(f, *args):
    '''Return the result of invoking a function f with arguments args, along
    with the time computation takes.'''
    start = clock()
    result = f(*args)
    return result, clock()-start
