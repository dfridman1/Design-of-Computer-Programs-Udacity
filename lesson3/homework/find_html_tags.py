# *** FINDING HTML TAGS ***

import re




def findtags(text):
    regex = r'<[ ]*[a-zA-Z]+[ ]*(?:[a-zA-Z]+[ ]*=[ ]*".+[ ]*")*/?>'
    pat = re.compile(regex)
    return re.findall(pat, text)


testtext1 = """
My favorite website in the world is probably
<a href="www.udacity.com">Udacity</a>. If you want
that link to open in a <b>new tab</b> by default, you should
write <a href="www.udacity.com"target="_blank">Udacity</a>
instead!
"""

testtext2 = """
Okay, so you passed the first test case. <let's see> how you
handle this one. Did you know that 2 < 3 should return True?
So should 3 > 2. But 2 > 3 is always False.
"""

testtext3 = """
It's not common, but we can put a LOT of whitespace into
our HTML tags. For example, we can make something bold by
doing <         b           > this <   /b    >, Though I
don't know why you would ever want to.
"""


def test():
    assert findtags(testtext1) == ['<a href="www.udacity.com">',
                                   '<b>',
                                   '<a href="www.udacity.com"target="_blank">']
    assert findtags(testtext2) == []
    assert findtags(testtext3) == ['<         b           >']
    return 'tests pass'

print test()
