# *** DECORATORS EXAMPLES ***


from functools import update_wrapper
from time import clock





def decorator(d):
    '''Make function d a decorator: d wraps a function fn'''
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def countcalls(f):
    def _f(*args):
        _f.callcount += 1
        return f(*args)
    _f.callcount = 0
    return _f


@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (_f.level*indent, signature)
        _f.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % ((_f.level-1)*indent,
                                      signature, result)
        finally:
            _f.level -= 1
        return result
    _f.level = 0
    return _f


@decorator
def memo(f):
    '''Decorator that cashes the return value for each call to f(args).
    Then when called again with some args, we can just look it up.'''
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


@countcalls
@trace
@memo
def fib(n):
    '''Computes Fibonacci numbers'''
    if n == 0: return 0
    elif n == 1: return 1
    else: return fib(n - 1) + fib(n - 2)


def timed_call(f, *args):
    start = clock()
    result = f(*args)
    return result, clock() - start


@decorator
def trace(f):
    indent = '   '
    def _f(*args):
        signature = '%s(%s)' % (f.__name__, ', '.join(map(repr, args)))
        print '%s--> %s' % (indent * _f.level, signature)
        _f.level += 1
        try:
            result = f(*args)
            print '%s<-- %s == %s' % (indent * (_f.level - 1), signature, result)
        finally:
            _f.level -= 1
        return result

    _f.level = 0
    return _f
