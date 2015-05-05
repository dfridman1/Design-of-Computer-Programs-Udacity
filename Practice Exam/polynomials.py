"""
UNIT 3: Functions and APIs: Polynomials

A polynomial is a mathematical formula like:

    30 * x**2 + 20 * x + 10

More formally, it involves a single variable (here 'x'), and the sum of one
or more terms, where each term is a real number multiplied by the variable
raised to a non-negative integer power. (Remember that x**0 is 1 and x**1 is x,
so 'x' is short for '1 * x**1' and '10' is short for '10 * x**0'.)

We will represent a polynomial as a Python function which computes the formula
when applied to a numeric value x.  The function will be created with the call:

    p1 = poly((10, 20, 30))

where the nth element of the input tuple is the coefficient of the nth power of x.
(Note the order of coefficients has the x**n coefficient neatly in position n of 
the list, but this is the reversed order from how we usually write polynomials.)
poly returns a function, so we can now apply p1 to some value of x:

    p1(0) == 10

Our representation of a polynomial is as a callable function, but in addition,
we will store the coefficients in the .coefs attribute of the function, so we have:

    p1.coefs == (10, 20, 30)

And finally, the name of the function will be the formula given above, so you should
have something like this:

    >>> p1
    <function 30 * x**2 + 20 * x + 10 at 0x100d71c08>

    >>> p1.__name__
    '30 * x**2 + 20 * x + 10'

Make sure the formula used for function names is simplified properly.
No '0 * x**n' terms; just drop these. Simplify '1 * x**n' to 'x**n'.
Simplify '5 * x**0' to '5'.  Similarly, simplify 'x**1' to 'x'.
For negative coefficients, like -5, you can use '... + -5 * ...' or
'... - 5 * ...'; your choice. I'd recommend no spaces around '**'
and spaces around '+' and '*', but you are free to use your preferences.

Your task is to write the function poly and the following additional functions:

    is_poly, add, sub, mul, power, deriv, integral

They are described below; see the test_poly function for examples.
"""


def poly(coefs):
    """Return a function that represents the polynomial with these coefficients.
    For example, if coefs=(10, 20, 30), return the function of x that computes
    '30 * x**2 + 20 * x + 10'.  Also store the coefs on the .coefs attribute of
    the function, and the str of the formula on the .__name__ attribute.'"""

    def polynomial(x):
        return sum(c*(x**p) for (p, c) in enumerate(coefs))

    polynomial.coefs = canonical(coefs)

    polynomial.__name__ = get_poly_name(polynomial.coefs)

    return polynomial


def get_poly_name(coefs):
    '''Given coefficients of the polynomial, return string representation of
    it.'''
    name = []
    for term in enumerate(coefs):
        s = term_to_string(term)
        if s:
            name.append(s)
    name = ' + '.join(reversed(name))
    if not name:
        name = "0"
    return name


def term_to_string(term):
    '''Given an equation term in the form (power, coefficient), return an
    appropriate string represenation of the term. E.g, (3,2) => 3 * x**2'''
    power, coef = term

    def power_to_string(power):
        if power == 0:
            return ""
        else:
            s = "x"
            if power > 1:
                s += "**" + str(power)
            return s

    if coef == 0:
        return ""
    elif coef == 1:
        return power_to_string(power) if power != 0 else '1'
    else:
        power_str = power_to_string(power)
        return (str(coef) + " * " + power_str) if power_str else str(coef)


def canonical(coefs):
    "Remove trailing zeros and return as a tuple."
    if isinstance(coefs, (int, float)):
        coefs = [coefs]
    elif len(coefs) == 0:
        return (0,)
    coefs = remove_trailing_zeros(coefs)
    return tuple(coefs)


def same_name(name1, name2):
    '''I define this function rather than doing name1 == name2 to allow some
    variation in naming conventions.'''

    def canonical_name(name):
        return name.replace(' ', '').replace('+-', '-')

    return canonical_name(name1) == canonical_name(name2)


def is_poly(x):
    '''Return True if x is a poly (polynomial).'''
    return callable(x) and hasattr(x, 'coefs')


def add(p1, p2):
    "Return a new polynomial which is the sum of polynomials p1 and p2."

    def _add(coefs1, coefs2):
        if not coefs1:
            return tuple(coefs2)
        if not coefs2:
            return tuple(coefs1)
        return (coefs1[0] + coefs2[0],) + _add(coefs1[1:], coefs2[1:])

    return poly(_add(p1.coefs, p2.coefs))


def negate(p):
    "Negate the coefficients of the polynomial."
    negate = lambda x: -x
    return poly(map(negate, p.coefs))


def sub(p1, p2):
    "Return a new polynomial which is the difference of polynomials p1 and p2."
    return add(p1, negate(p2))


def mul(p1, p2):
    "Return a new polynomial which is the product of polynomials p1 and p2."
    max_power = (len(p1.coefs)-1) + (len(p2.coefs)-1)
    coefs = [0 for _ in xrange(max_power+1)]

    for (i, c) in enumerate(p1.coefs):
        for (j, d) in enumerate(p2.coefs):
            coefs[i+j] += c * d

    return poly(coefs)


def remove_trailing_zeros(L):
    t = type(L)
    L = list(L)
    while L and L[-1] == 0:
        del L[-1]
    return t(L)


def power(p, n):
    "Return a new polynomial which is p to the nth power (n - nonnegative)"
    if n == 0:
        return poly(1)
    elif even(n):
        return square(power(p, n >> 1))
    else:
        return mul(p, power(p, n-1))


def even(x):
    return x % 2 == 0


def square(x):
    return mul(x, x)


def deriv(p):
    "Return derivative of a function p (with respect to its argument)."
    coefs = list(p.coefs)
    if len(coefs) == 1:
        return poly((0,))  # derivative of a constant function
    for (p, coeff) in enumerate(coefs[1:], 1):
        coefs[p-1] = p*coeff
    coefs.pop()
    return poly(tuple(coefs))


def integral(p, C=0):
    "Return the integral of a function p (with respect to its argument."
    coefs = [C]
    for (p, c) in enumerate(p.coefs):
        coefs.append(float(c) / (p+1))
    return poly(tuple(coefs))


"""
Now for an extra credit challenge: arrange to describe polynomials with an
expression like '3 * x**2 + 5 * x + 9' rather than (9, 5, 3).  You can do this
in one (or both) of two ways:

(1) By defining poly as a class rather than a function, and overloading the
__add__, __sub__, __mul__, and __pow__ operators, etc.  If you choose this,

(2) Using the grammar parsing techniques we learned in Unit 5. For this
approach, define a new function, Poly, which takes one argument, a string,
as in Poly('30 * x**2 + 20 * x + 10').  Call test_poly2().
"""


class Poly(object):
    def __init__(self, coefs):
        self.coefs = canonical(coefs)
        self.fn = poly(self.coefs)
        self.__name__ = get_poly_name(self.coefs)

    def __call__(self, x):
        return self.fn(x)

    def __eq__(self, other):
        return isinstance(other, Poly) and self.coefs == other.coefs

    def __add__(self, other):
        coefs = add(self, Poly._coerce_poly(other)).coefs
        return Poly(coefs)

    def __sub__(self, other):
        coefs = sub(self, Poly._coerce_poly(other)).coefs
        return Poly(coefs)

    def __pos__(self):
        return self

    def __neg__(self):
        coefs = negate(self).coefs
        return Poly(coefs)

    def __mul__(self, other):
        coefs = mul(self, Poly._coerce_poly(other)).coefs
        return Poly(coefs)

    def __pow__(self, n):
        coefs = power(self, n).coefs
        return Poly(coefs)

    def __radd__(self, other):
        coefs = add(self, Poly._coerce_poly(other)).coefs
        return Poly(coefs)

    def __rmul__(self, other):
        coefs = mul(self, Poly._coerce_poly(other)).coefs
        return Poly(coefs)

    @staticmethod
    def _coerce_poly(p):
        return p if isinstance(p, Poly) else Poly(p)


def test_poly():
    global p1, p2, p3, p4, p5, p9

    p1 = poly((10, 20, 30))
    assert p1(0) == 10
    for x in (1, 2, 3, 4, 5, 1234.5):
        assert p1(x) == 30 * x**2 + 20 * x + 10
    assert same_name(p1.__name__, '30 * x**2 + 20 * x + 10')

    assert is_poly(p1)
    assert not is_poly(abs) and not is_poly(42) and not is_poly('cracker')

    p3 = poly((0, 0, 0, 1))
    assert p3.__name__ == 'x**3'
    p9 = mul(p3, mul(p3, p3))
    assert p9(2) == 512
    p4 = add(p1, p3)
    assert same_name(p4.__name__, 'x**3 + 30 * x**2 + 20 * x + 10')

    assert same_name(poly((1, 1)).__name__, 'x + 1')
    assert same_name(power(poly((1, 1)), 10).__name__,
            'x**10 + 10 * x**9 + 45 * x**8 + 120 * x**7 + 210 * x**6 + 252 * x**5 + 210' +
            ' * x**4 + 120 * x**3 + 45 * x**2 + 10 * x + 1')

    assert add(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (11,22,33)
    assert sub(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (9,18,27)
    assert mul(poly((10, 20, 30)), poly((1, 2, 3))).coefs == (10, 40, 100, 120, 90)
    assert power(poly((1, 1)), 2).coefs == (1, 2, 1)
    assert power(poly((1, 1)), 10).coefs == (1, 10, 45, 120, 210, 252, 210, 120, 45, 10, 1)

    assert deriv(p1).coefs == (20, 60)
    assert integral(poly((20, 60))).coefs == (0, 20, 30)
    p5 = poly((0, 1, 2, 3, 4, 5))
    assert same_name(p5.__name__, '5 * x**5 + 4 * x**4 + 3 * x**3 + 2 * x**2 + x')
    assert p5(1) == 15
    assert p5(2) == 258
    assert same_name(deriv(p5).__name__,  '25 * x**4 + 16 * x**3 + 9 * x**2 + 4 * x + 1')
    assert deriv(p5)(1) == 55
    assert deriv(p5)(2) == 573

    print "test_poly passed"


def test_poly1():
    # I define x as the polynomial 1*x + 0.
    x = Poly((0, 1))
    # From here on I can create polynomials by + and * operations on x.
    newp1 = 30 * x**2 + 20 * x + 10  # This is a poly object, not a number!
    assert p1(100) == newp1(100)  # The new poly objects are still callable.
    assert same_name(p1.__name__,newp1.__name__)
    assert (x + 1) * (x - 1) == x**2 - 1 == Poly((-1, 0, 1))
    print "test_poly1 passed"


test_poly()
test_poly1()
