import time


def memo(f):
    '''Memoization decorator'''
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
    '''Returns the result of invoking a function
    and the time it takes'''
    start = time.clock()
    result = f(*args)
    return result, time.clock() - start
