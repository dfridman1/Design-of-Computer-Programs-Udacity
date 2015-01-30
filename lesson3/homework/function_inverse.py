# *** FUNCTION INVERSE ***



def inverse(f, delta):
    '''Return an inverse function for a given function f.
    NOTE: f is monotonically increasing and f: R+ -> R+'''
    def _f(y):
        low, high = find_bounds(f, y)
        return binary_search(f, y, low, high, delta)
    return _f


def find_bounds(f, y, low=0, high=1):
    while f(high) < y:
        low, high = high, high * 2
    return low, high


def binary_search(f, y, low, high, delta):
    mid = (low + high) / 2.0
    diff = f(mid) - y
    while abs(diff) > delta:
        if diff > 0:
            high = mid
        elif diff < 0:
            low = mid
        else:
            return mid
        mid = (low + high) / 2.0
        diff = f(mid) - y
    return mid
