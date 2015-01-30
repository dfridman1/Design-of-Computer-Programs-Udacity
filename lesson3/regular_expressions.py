# *** REGULAR EXPRESSIONS ***


#here we consider 5 special characters: '?.^$*'



def search(pattern, text):
    "Return True if pattern appears anywhere in the text"
    if pattern.startswith('^'):
        return match(pattern[1:], text)
    else:
        return match('.*' + pattern, text)


def match(pattern, text):
    "Return True if pattern appears at the start of the text"
    if not pattern: return True
    elif pattern == '$': return text == ''
    elif len(pattern) > 1 and pattern[1] in '?*':
        p, op, pat = pattern[0], pattern[1], pattern[2:]
        if op == '?':
            if match1(p, text) and match(pat, text[1:]):
                return True
            else:
                return match(pat, text)
        elif op == '*':
            return star_match(p, pat, text)
    else:
        return match1(pattern[0], text) and match(pattern[1:], text[1:])


def match1(p, text):
    "Return True if first char of text matches char p"
    if not text: return False
    return p == '.' or p == text[0]


def star_match(p, pattern, text):
    return (match1(p, text) and star_match(p, pattern, text[1:])) or match(pattern, text)
