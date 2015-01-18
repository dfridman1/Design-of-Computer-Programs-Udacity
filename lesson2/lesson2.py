from __future__ import division
import itertools, time, string, re, cProfile



#CRYPTARITHMETIC PUZZLES



examples = ['ODD + ODD == EVEN', 'TWO + TWO == FOUR', 'A**2 + B**2 == C**2',
            'X / X == X', 'GLITTERS is not GOLD', 'ATOM**0.5 == A + TO + M']




def timedcall(fn, *args):
    "return the runtime of fn and its result"
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1 - t0, result



def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    for f in fill_in(formula):
        if valid(f):
            return f


def fill_in(formula):
    "Generate all possible fillings-in of letters in formula with digits."
    letters = ''.join( set( re.findall('[A-Z]', formula) ) )
    for digits in itertools.permutations('1234567890', len(letters)):
        table = string.maketrans(letters, ''.join(digits))
        yield formula.translate(table)



def valid(f):
    """Formula f is valid if and only if it has no
    numbers with leading zero, and evaluates to true."""
    try:
        return not re.search(r'\b0[0-9]', f) and eval(f)
    except ArithmeticError:
        return False





#Since for every possible permutation of digits we call
#a costly function 'eval', I will first compile a 'letters'
#formula into a lambda function

def compile_word(word):
    """Compile a word of uppercase letters as numeric digits.
    E.g., compile_word('YOU') => '(1*U+10*O+100*Y)'
    Non-uppercase words unchanged: compile_word('+') => '+'"""

    if word.isupper():
        terms = ['%s*%s' % (10 ** i, d) for i, d in enumerate(word[::-1])]
        return '(' + '+'.join(terms) + ')'
    return word




def compile_formula(formula, verbose=False):
    """Compile formula into a function. Also return letters found, as a str,
    in  same order as parms of function. For example, 'YOU == ME**2' returns
    (lambda Y, M, E, U, O : (U+10*O+100*Y) == (E+10*M)**2), 'YMEUO'  """

    letters = ''.join( set( re.findall('[A-Z]', formula) ) )
    leading_letters = set( re.findall( r'\b[A-Z]' , formula ) )
    print leading_letters
    if formula[0] in string.ascii_letters: leading_letters.add(formula[0])

    if_clauses = ' and '.join([letter + ' != 0' for letter in leading_letters])

    parms = ', '.join(letters)
    tokens = map(compile_word, re.split('([A-Z]+)', formula))
    body = ''.join(tokens)

    if if_clauses: body = '%s and %s' % (body, if_clauses)

    f = 'lambda %s : %s' % (parms, body)

    if verbose: print f
    return eval(f), letters




def faster_solve(formula):
    "solve cryptarithmetic puzzle by first compiling a formula"
    f, letters = compile_formula(formula)

    for digits in itertools.permutations((1, 2, 3, 4, 5, 6, 7, 8, 9, 0), len(letters)):
        try:
            if f(*digits) is True:
                table = string.maketrans(letters, ''.join(map(str, digits)))
                yield formula.translate(table)
        except ArithmeticError:
            pass
