#  *** BUILDING A LANGUAGE GENERATOR ***

from functools import update_wrapper




def decorator(d):
    '''Make function d a decorator: d wraps a function fn'''
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def n_ary(f):
    '''Given a binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y, z)), etc. Also allow f(x) = x.'''
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f




null = frozenset()


def lit(s):
    set_s = {s}
    return lambda Ns: set_s if len(s) in Ns else null


def alt(x, y):    return lambda Ns: x(Ns) | y(Ns)


def star(x):      return lambda Ns: opt(plus(x))(Ns)


def plus(x):      return lambda Ns: genseq(x, star(x), Ns, startx=1)


def oneof(chars):
    chars_set = set(chars)
    return lambda Ns: chars_set if 1 in Ns else null


@n_ary
def seq(x, y):    return lambda Ns: genseq(x, y, Ns)


def opt(x):       return alt(epsilon, x)


dot = oneof('?')


epsilon = lit('')


def genseq(x, y, Ns, startx=0):
    if not Ns:
        return null
    xmatches = x(set(range(startx, max(Ns) + 1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n - m for n in Ns for m in Ns_x if n >= m)
    ymatches = y(Ns_y)
    return set(m1 + m2 for m1 in xmatches for m2 in ymatches
               if len(m1) + len(m2) in Ns)




def test():
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null

    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])

    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null

    print 'tests pass'
test()
