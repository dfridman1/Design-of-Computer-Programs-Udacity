import random
from collections import defaultdict


##Poker Program



def poker(hands):
    '''return best hands from hands: [hand, ...] => [hand, ...]'''
    return allmax(hands, key=hand_rank)


def allmax(iterable, key=None):
    key = key or (lambda x : x)
    return filter(lambda x : key(x) == key(max(iterable, key=key)), iterable)


def hand_rank(hand):
    "Return a value indicating how high the hand ranks."
    groups = group(['--23456789TJQKA'.find(r) for r, s in hand])
    counts, ranks = unzip(groups)
    if ranks == (14, 5, 4, 3, 2):
        ranks = (5, 4, 3, 2, 1)
    straight = len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4
    flush = len(set([s for r, s in hand])) == 1
    return max(count_rankings[counts], 4 * straight + 5 * flush), ranks


count_rankings = {(5, ) : 10, (4, 1) : 7, (3, 2) : 6, (3, 1, 1) : 3, (2, 2, 1) : 2, (2, 1, 1, 1) : 1, (1, 1, 1, 1, 1) : 0}


def group(items):
    "Return a list of [(count, x), ...], highest count first, then highest x first"
    return sorted([(items.count(x), x) for x in set(items)], reverse=True)


def unzip(pairs):
    return zip(*pairs)


def card_ranks(cards):
    "Return a list of the ranks, sorted with higher first"
    ranks = ['--23456789TJQKA'.find(r) for r, s in cards]
    ranks.sort(reverse=True)
    return [5, 4, 3, 2, 1] if ranks == [14, 5, 4, 3, 2] else ranks




mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']

def deal(numhands, n=5, deck=mydeck):
    random.shuffle(deck)
    return [deck[n*i : n*(i + 1)] for i in xrange(numhands)]


def test():
    "Test cases for the functions in poker program"
    sf = "6C 7C 8C 9C TC".split() # Straight Flush
    fk = "9D 9H 9S 9C 7D".split() # Four of a Kind
    fh = "TD TC TH 7C 7D".split() # Full House

    assert poker([sf, fk, fh]) == [sf]
    assert poker([fk, fh]) == [fk]
    assert poker([fh, fh]) == [fh, fh]
    assert poker([sf]) == [sf]
    assert poker([sf] + 99*[fh]) == [sf]

    print 'Test cases passed'


test()








