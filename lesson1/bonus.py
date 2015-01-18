import random, collections, itertools



def shuffle(iterable):
    N = len(iterable)
    for i in xrange(N - 1):
        j = random.randrange(i, N)
        swap(iterable, i, j)


def swap(iterable, i, j):
    iterable[i], iterable[j] = iterable[j], iterable[i]


def test_shuffler(shuffler, deck='abcd', n=10000):
    counts = collections.defaultdict(int)
    for _ in xrange(n):
        input = list(deck)
        shuffle(input)
        counts[''.join(input)] += 1
    e = n * 1./factorial(len(deck)) #expected count
    ok = all(0.9 <= counts[item] / e <= 1.1 for item in counts)
    name = shuffler.__name__
    print '%s(%s) %s' % (name, deck, 'ok' if ok else '*** BAD ***')
    print '  '
    for item, count in sorted(counts.items()):
        print '%s:%4.1f' % (item, count * 100./e)





allranks = '23456789TJQKA'
redcards = [r + s for r in allranks for s in 'DH']
blackcards = [r + s for r in allranks for s in 'SC']


def best_wild_hand(hand):
    "Try all values for jokers in all 5-card selections."
    hands = set(best_hand(h) for h in itertools.product(*map(replacements, hand)))
    return max(hands, key=hand_rank)


def best_hand(hand):
    return max(itertools.combinations(hand, 5), key=hand_rank)


def replacements(card):
    if card == '?R': return redcards
    if card == '?B': return blackcards
    return [card]


def hand_rank(hand):
    "Return a value indicating the ranking of a hand."
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand):
    "Return a list of the ranks, sorted with higher first."
    ranks = ['--23456789TJQKA'.index(r) for r, s in hand]
    ranks.sort(reverse = True)
    return [5, 4, 3, 2, 1] if (ranks == [14, 5, 4, 3, 2]) else ranks


def flush(hand):
    "Return True if all the cards have the same suit."
    suits = [s for r,s in hand]
    return len(set(suits)) == 1


def straight(ranks):
    """Return True if the ordered
    ranks form a 5-card straight."""
    return (max(ranks)-min(ranks) == 4) and len(set(ranks)) == 5


def kind(n, ranks):
    """Return the first rank that this hand has
    exactly n-of-a-kind of. Return None if there
    is no n-of-a-kind in the hand."""
    for r in ranks:
        if ranks.count(r) == n: return r
    return None


def two_pair(ranks):
    """If there are two pair here, return the two
    ranks of the two pairs, else None."""
    pair = kind(2, ranks)
    lowpair = kind(2, list(reversed(ranks)))
    if pair and lowpair != pair:
        return (pair, lowpair)
    else:
        return None
