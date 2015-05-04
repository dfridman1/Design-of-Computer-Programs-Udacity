# -----------------
# User Instructions
#
# In this problem, you will define a function, boggle_words(),
# that takes a board as input and returns a set of words that
# can be made from the board according to the rules of Boggle.


def prefixes(word):
    "Return a set of prefixes of the word, excluding the word itself."
    return set(word[:i] for i in xrange(len(word)))


def readwordlist(filename):
    words = file(filename).read().upper().split()
    prefx = set(p for w in words for p in prefixes(w))
    return words, prefx


FILENAME = "../4kwords.txt"
WORDS, PREFIXES = readwordlist(FILENAME)


LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
BORDER = '|'


def boggle_words(board, minlength=3):
    "Find all words on this Boggle board; return as a set of words."
    results = set()
    N = size(board)

    def valid(word):
        return len(word) >= minlength and word in WORDS

    def extend_path(prefix, path):
        if valid(prefix):
            results.add(prefix)
        if prefix in PREFIXES:
            for i in neighbors(path[-1], N):
                if i not in path and is_letter(board[i]):
                    extend_path(prefix+board[i], path+[i])

    for (i, sq) in enumerate(board):
        if is_letter(sq):
            extend_path(sq, [i])

    return results


def Board(text):
    '''Input is a string of space-separated rows of N letters each;
    result is a string of size (N+2)**2 with borders all around.'''
    rows = text.split()
    N = len(rows)
    rows = [BORDER*N] + rows + [BORDER*N]
    return ''.join(BORDER + row + BORDER for row in rows)


def size(board):
    return int(len(board) ** 0.5)


def neighbors(i, N):
    '''Return indices of the neighboring squares.'''
    return (i-N-1, i-N, i-N+1, i-1, i+1, i+N-1, i+N, i+N+1)


def is_letter(sq):
    return isinstance(sq, str) and sq in LETTERS
