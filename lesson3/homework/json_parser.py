# *** BUILDING A JSON PARSER ***

from functools import update_wrapper
import re




def decorator(d):
    '''Make function d a decorator: d wraps a function fn.'''
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    '''Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up.'''
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f




def grammar(description, whitespace=r'\s*'):
    '''Convert language description to a grammar.'''
    G = {' ': whitespace}
    description = description.replace('\t', ' ')
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G


def split(text, sep=None, maxsplit=-1):
    '''Like str.split applied to text, but strips whitespace from each piece'''
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]




Fail = (None, None)

def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])

    # Body of parse:
    return parse_atom(start_symbol, text)



json_description = '''
object   => [{] members [}]
members  => pair [,] members | pair
pair     => string [:] value
value    => object | array | number | string
array    => [[] elements []]
elements => value [,] elements | value
number   => int frac exp | int frac | int exp | int
int      => [-+]?[0-9]+
frac     => [.][0-9]+
exp      => e[+-][0-9]+
string   => "([^"\\\\]|\\["\\/bfnrtu])*"
'''


JSON = grammar(json_description, whitespace='\s*')


def json_parse(text):
    return parse('value', text, JSON)


def test():
    assert json_parse('["testing", 1, 2, 3]') == (
                       ['value', ['array', '[', ['elements', ['value',
                       ['string', '"testing"']], ',', ['elements', ['value', ['number',
                       ['int', '1']]], ',', ['elements', ['value', ['number',
                       ['int', '2']]], ',', ['elements', ['value', ['number',
                       ['int', '3']]]]]]], ']']], '')

    assert json_parse('-123.456e+789') == (
                       ['value', ['number', ['int', '-123'], ['frac', '.456'], ['exp', 'e+789']]], '')

    assert json_parse('{"age": 21, "state":"CO","occupation":"rides the rodeo"}') == (
                      ['value', ['object', '{', ['members', ['pair', ['string', '"age"'],
                       ':', ['value', ['number', ['int', '21']]]], ',', ['members',
                      ['pair', ['string', '"state"'], ':', ['value', ['string', '"CO"']]],
                      ',', ['members', ['pair', ['string', '"occupation"'], ':',
                      ['value', ['string', '"rides the rodeo"']]]]]], '}']], '')
    return 'tests pass'
