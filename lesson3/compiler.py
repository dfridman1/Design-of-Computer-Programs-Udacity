# *** BUILDING A COMPILER TO MATCH PATTERNS IN TEXT ***



def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None"
    for i in xrange(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m


def match(pattern, text):
    "Match pattern against start of the text; return longest match found or None"
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text) - len(shortest)]


def lit(x): return lambda text: set([text[len(x):]]) if text.startswith(x) else null
def seq(x, y): return lambda text: set().union(*map(y, x(text)))
def alt(x, y): return lambda text: set().union(x(text), y(text))
def oneof(chars): return lambda text: set([text[1:]]) if (text and text[0] in chars) else null
dot = lambda text: set([text[1:]]) if text else null
eol = lambda text: set([""]) if text == "" else null
def plus(x): return seq(x, star(x))
def opt(x): return alt(lit(""), x)
def star(x): return lambda text: set([text]) | set(t2 for t1 in x(text) if t1 != text
                                                      for t2 in star(x)(t1))

null = frozenset()


def test_search():
    a, b, c = lit('a'), lit('b'), lit('c')
    abcstars = seq(star(a), seq(star(b), star(c)))
    dotstar = star(dot)
    assert search(lit('def'), 'abcdefg') == 'def'
    assert search(seq(lit('def'), eol), 'abcdef') == 'def'
    assert search(seq(lit('def'), eol), 'abcdefg') == None
    assert search(a, 'not the start') == 'a'
    assert match(a, 'not the start') == None
    assert match(abcstars, 'aaabbbccccccccdef') == 'aaabbbcccccccc'
    assert match(abcstars, 'junk') == ''
    assert all(match(seq(abcstars, eol), s) == s
                    for s in 'abc aaabbccc aaaabcccc'.split())
    assert all(match(seq(abcstars, eol), s) == None
                    for s in 'cab aaabbcccd aaaa-b-cccc'.split())
    r = seq(lit('ab'), seq(dotstar, seq(lit('aca'), seq(dotstar, seq(a, eol)))))
    assert all(search(r, s) is not None
                for s in 'abracadabra abacaa about-acacia-flora'.split())
    assert all(match(seq(c, seq(dotstar, b)), s) is not None
                for s in 'cab cob carob cb carbuncle'.split())
    assert not any(match(seq(c, seq(dot, b)), s)
                for s in 'crab cb across scab'.split())
    print 'test_search passes'

test_search()
