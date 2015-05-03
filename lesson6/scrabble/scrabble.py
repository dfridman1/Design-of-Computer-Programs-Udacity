# *** SCRABBLE GAME ***


def prefixes(word):
    "A list of the prefixes of a word, excluding the entire word."
    return [word[:i] for i in xrange(len(word))]


def readwordlist(filename):
    '''Read the words from a file and return a set of
    the words and a set of the prefixes.'''
    wordset = set(file(filename).read().upper().split())
    prefixset = set(p for word in wordset for p in prefixes(word))
    return wordset, prefixset


FILENAME = "../4kwords.txt"
WORDS, PREFIXES = readwordlist(FILENAME)


BLANK = '_'


def find_words(letters, pre="", results=None):
    if results is None:
        results = set()
    if pre in WORDS:
        results.add(pre)
    if pre in PREFIXES:
        for letter in letters:
            find_words(letters.replace(letter, '', 1), pre+letter, results)
    return results


def removed(hand, letters):
    '''Remove the first occurrence of letter in letters from hand.'''
    for L in letters:
        hand = hand.replace(L, '', 1)
    return hand


def word_plays(hand, board_letters):
    '''Find all word plays from hand that can be made to
    abut with a letter on board.'''
    # Find prefix + L + suffix; L from board letters, rest from hand
    results = set()
    for pre in find_prefixes(hand, '', set()):
        for L in board_letters:
            add_suffixes(removed(hand, pre), pre+L, results)
    return results


prev_hand, prev_results = '', set()  # cache for find_prefixes


def find_prefixes(hand, pre='', results=None):
    '''Find all prefixes (of words) that can be made from letters in hand'''
    global prev_hand, prev_results
    if hand == prev_hand:
        return prev_results
    if results is None:
        results = set()
    if pre == '':
        prev_hand, prev_results = hand, results
    PRE = pre.upper()
    if PRE in WORDS or PRE in PREFIXES:
        results.add(pre)
    if PRE in PREFIXES:
        for letter in hand:
            if is_blank(letter):
                for C in LOWER_LETTERS:
                    find_prefixes(hand.replace(BLANK, '', 1), pre+C, results)
            else:
                find_prefixes(hand.replace(letter, '', 1), pre+letter, results)
    return results


def add_suffixes(hand, pre, start, row, results, anchored=True):
    '''Add all possible suffixes, and accumulate (start, word) pairs in
    results'''
    i = start + len(pre)
    PRE = pre.upper()
    if PRE in WORDS and anchored and not is_letter(row[i]):
        results.add((start, pre))
    if PRE in PREFIXES:
        sq = row[i]
        if is_letter(sq):
            add_suffixes(hand, pre+sq, start, row, results)
        elif is_empty(sq):
            possibilities = sq if isinstance(sq, anchor) else ANY
            for L in hand:
                if L in possibilities:
                    add_suffixes(hand.replace(L, '', 1), pre+L, start,
                                 row, results)
                elif is_blank(L):
                    for C in possibilities:
                        add_suffixes(hand.replace(BLANK, '', 1), pre+C.lower(),
                                     start, row, results)
    return results


def longest_words(hand, board_letters):
    '''Return all word plays, longest first.'''
    words = word_plays(hand, board_letters)
    return sorted(words, key=len, reverse=True)


POINTS = dict(A=1, B=3, C=3, D=2, E=1, F=4, G=2, H=4, I=1,
              J=8, K=5, L=1, M=3, N=1, O=1, P=3, Q=10, R=1,
              S=1, T=1, U=1, V=4, W=4, X=8, Y=4, Z=10, _=0)


def word_score(word):
    "The sum of individual point scores for the word."
    return sum(POINTS[letter] for letter in word)


def topn(hand, board_letters, n=10):
    '''Return a list of the top n words that hand can
    play, sorted by word score'''
    words = word_plays(hand, board_letters)
    return sorted(words, key=word_score, reverse=True)[:n]


class anchor(set):
    '''An anchor is where a new word can be placed; has a set of allowable
    letters.'''


LETTERS = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
LOWER_LETTERS = map(str.lower, LETTERS)  # representation of blank tiles
ANY = anchor(LETTERS)

for L in LOWER_LETTERS:
    POINTS[L] = 0


def row_plays(hand, row):
    "Return a set of legal plays in row. A row play is an (start, 'WORD') pair"
    results = set()
    # To each allowable prefix, add all suffixes, keeping words
    for (i, sq) in enumerate(row[1:-1], 1):
        if isinstance(sq, anchor):
            pre, maxsize = legal_prefix(i, row)
            if pre:  # Add to the letters already on the board
                start = i - len(pre)
                add_suffixes(hand, pre, start, row, results, anchored=False)
            else:  # Empty to left: go through the set of all possible prefixes
                for pre in find_prefixes(hand):
                    if len(pre) <= maxsize:
                        start = i - len(pre)
                        add_suffixes(removed(hand, pre), pre, start, row,
                                     results, anchored=False)
    return results


def legal_prefix(i, row):
    '''A legal prefix of an anchor at row[i] is either a string of letters
    already on the board, or new letters that fit into an empty space. Return
    the tuple (prefix_on_board, maxsize) to indicate this.
    E.g. legal_prefix(a_row, 9) == ('BE', 2) and for 6, ('', 2).'''
    s = i
    while is_letter(row[s-1]):
        s -= 1
    if s < i:
        return (''.join(row[s:i]), i-s)
    while is_empty(row[s-1]) and not isinstance(row[s-1], anchor):
        s -= 1
    return ('', i-s)


def is_letter(sq):
    return isinstance(sq, str) and (sq in LETTERS or sq in LOWER_LETTERS)


def is_empty(sq):
    return sq == '.' or sq == '*' or isinstance(sq, anchor)


def is_blank(tile):
    "Return True the tile is blank"
    return tile == BLANK


def show(board):
    '''Print the board, and the BONUS[j][i] entries where appropriate.'''
    print('\n'.join(
        ' '.join(
            [letter if (is_letter(letter) or letter == '|') else BONUS[j][i]
             for i, letter in enumerate(row)])
        for j, row in enumerate(board)))


def horizontal_plays(hand, board):
    '''Find all horizontal plays -- (score, (i, j), word) pairs --- across all
    rows. NOTE: (i, j) === (column, row).'''
    results = set()
    for (j, row) in enumerate(board[1:-1], 1):
        set_anchors(row, j, board)
        for (i, word) in row_plays(hand, row):
            score = calculate_score(board, (i, j), ACROSS, hand, word)
            results.add((score, (i, j), word))
    return results


ACROSS, DOWN = (1, 0), (0, 1)


def all_plays(hand, board):
    '''All plays in both directions. A play is a (score, pos, dir, word) tuple,
    where pos is an (i, j) pair, and dir is a (delta_i, delta_j) pair.'''
    hplays = horizontal_plays(hand, board)
    vplays = horizontal_plays(hand, transpose(board))

    return (set((score, (i, j), ACROSS, word) for (score, (i, j), word) in hplays) |
            set((score, (i, j), DOWN, word) for (score, (j, i), word) in vplays))


def set_anchors(row, j, board):
    '''Anchors are empty squares with a neighboring letter. Some are restricted
    by cross-words to be only a subset of letters.'''
    for (i, sq) in enumerate(row[1:-1], 1):
        neighborlist = (N, S, E, W) = neighbors(board, i, j)
        # Anchors are letters adjacent to a letter. Plus the '*' square
        if sq == '*' or (is_empty(sq) and any(map(is_letter, neighborlist))):
            # Find letters that fit with the cross (vertical) word
            if is_letter(N) or is_letter(S):
                (j2, w) = find_cross_word(board, i, j)
                row[i] = anchor(L for L in LETTERS if w.replace('.', L) in
                                WORDS)
            else:
                row[i] = ANY


def find_cross_word(board, i, j):
    '''Find the vertical word that crosses board[j][i]. Return (j2, w), where
    j2 is the starting row, and w is the word.'''
    sq = board[j][i]
    w = sq if is_letter(sq) else '.'
    for j2 in xrange(j, 0, -1):
        sq2 = board[j2-1][i]
        if is_letter(sq2):
            w = sq2 + w
        else:
            break
    for j3 in xrange(j+1, len(board)):
        sq3 = board[j3][i]
        if is_letter(sq3):
            w += sq3
        else:
            break
    return (j2, w)


def neighbors(board, i, j):
    '''Return a list of the contents of the four neighboring squares, in the
    order N, S, E, W.'''
    return [board[j-1][i], board[j+1][i],
            board[j][i+1], board[j][i-1]]


def transpose(matrix):
    '''Return a matrix transpose.'''
    return map(list, zip(*matrix))


def calculate_score(board, pos, direction, hand, word):
    "Return the total score for the play."
    total, crosstotal, word_mult = (0, 0, 1)
    starti, startj = pos
    di, dj = direction
    other_direction = DOWN if direction == ACROSS else ACROSS
    for (n, L) in enumerate(word):
        i, j = starti + n*di, startj + n*dj
        sq = board[j][i]
        b = BONUS[j][i]
        word_mult *= (1 if is_letter(sq) else
                      3 if b == TW else 2 if b in (DW, '*') else 1)
        letter_mult = (1 if is_letter(sq) else
                       3 if b == TL else 2 if b == DL else 1)
        total += POINTS[L] * letter_mult
        if isinstance(sq, anchor) and sq is not ANY and direction is not DOWN:
            crosstotal += cross_word_score(board, L, (i, j), other_direction)
    return crosstotal + word_mult*total


def cross_word_score(board, L, pos, direction):
    '''Return the score of a word made in the other direction from the main
    word.'''
    i, j = pos
    (j2, word) = find_cross_word(board, i, j)
    return calculate_score(board, (i, j2), DOWN, L, word.replace('.', L))


def bonus_template(quadrant):
    '''Make a board from the upper-left quadrant.'''
    return mirror(map(mirror, quadrant.split()))


def mirror(sequence):
    return sequence + sequence[-2::-1]


def make_play(play, board):
    "Put the word down on the board."
    score, (i, j), (di, dj), word = play
    for (n, letter) in enumerate(word):
        board[j + n*dj][i + n*di] = letter
    return board


NOPLAY = None


def best_play(hand, board):
    plays = all_plays(hand, board)
    get_score = lambda play: play[0]  # play = (score, (i, j), (di, dj), word)
    return max(plays, key=get_score) if plays else NOPLAY


def show_best(hand, board):
    print "Current board"
    show(board)
    play = best_play(hand, board)
    if play:
        print "\nNew word: %r score %d" % (play[-1], play[0])
        show(make_play(play, board))
    else:
        print "Sorry, no legal plays!"


CRABBLE = bonus_template("""
|||||||||
|3..:...3
|.2...;..
|..2...:.
|:..2...:
|....2...
|.;...;..
|..:...:.
|3..:...*
""")

WWF = bonus_template("""
|||||||||
|...3..;.
|..:..2..
|.:..:...
|3..;...2
|..:...:.
|.2...;..
|;...:...
|...2...*
""")

DW, TW, DL, TL = '23:;'

BONUS = WWF
