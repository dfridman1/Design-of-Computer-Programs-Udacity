# *** FUNCTION INVERSE ***




# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the
# non-negative numbers. The runtime of your program should be
# proportional to the LOGARITHM of the input. You may want to
# do some research into binary search and Newton's method to
# help you out.
#
# This function should return another function which computes the
# inverse of the input function.
#
# Your inverse function should also take an optional parameter,
# delta, as input so that the computed value of the inverse will
# be within delta of the true value.





def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1


def inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def _f(y):
        low, high = get_bounds(f, y)
        return bin_search(low, high, f, y, delta)
    return _f


def get_bounds(f, x):
    low, high = 0, 1

    def in_between(x, l, h): return x >= f(l) and x <= f(h)

    while not in_between(x, low, high):
        low, high = high, 2 * high
    return (low, high)


def bin_search(low, high, f, y, delta):
    mid = (low + high) / 2.0
    lower_bound, upper_bound = y-delta, y+delta

    def good_enough(x): return x >= lower_bound and x <= upper_bound

    value = f(mid)
    while not good_enough(value):
        if value > y: high = mid
        else: low = mid
        mid = (low + high) / 2.0
        value = f(mid)

    return mid
