# -----------------
# User Instructions
#
# This homework deals with anagrams. An anagram is a rearrangement
# of the letters in a word to form one or more new words.
#
# Your job is to write a function anagrams(), which takes as input
# a phrase and an optional argument, shortest, which is an integer
# that specifies the shortest acceptable word. Your function should
# return a set of all the possible combinations of anagrams.
#
# Your function should not return every permutation of a multi word
# anagram: only the permutation where the words are in alphabetical
# order. For example, for the input string 'ANAGRAMS' the set that
# your function returns should include 'AN ARM SAG', but should NOT
# include 'ARM SAG AN', or 'SAG AN ARM', etc...


def anagrams(phrase, shortest=2):
    '''Return a set of phrases with words from WORDS that form anagram
    of phrase. Spaces can be anywhere in phrase or anagram. All words
    have length >= shortest. Phrases in answer must have words in
    lexicographic order (not all permutations).'''
    letters = phrase.replace(' ', '')  # remove whitespaces
    return find_anagrams(letters, shortest=shortest)
    # return find_anagrams2(letters, "", shortest)  -- Peter Norvig's solution


def find_anagrams(letters, so_far=[], last="", shortest=2, results=None):
    if results is None:
        results = set()
    if last in WORDS and len(last) >= shortest:
        if not letters:
            string = ' '.join(sorted(so_far + [last]))
            results.add(string)
            return
        else:
            find_anagrams(letters, so_far + [last], "", shortest, results)
    if last in PREFIXES:
        for L in letters:
            find_anagrams(letters.replace(L, '', 1), so_far, last+L, shortest,
                          results)
    return results


def find_anagrams2(letters, previous_word="", shortest=2):
    results = set()
    for w in find_words(letters):
        if len(w) >= shortest and previous_word <= w:
            remainder = removed(letters, w)
            if remainder:
                for rest in find_anagrams2(remainder, w, shortest):
                    results.add(w + ' ' + rest)
            else:
                results.add(w)
    return results


def find_words(letters, pre="", results=None):
    if results is None:
        results = set()
    if pre in WORDS:
        results.add(pre)
    if pre in PREFIXES:
        for L in letters:
            find_words(letters.replace(L, '', 1), pre+L, results)
    return results


def readwordlist(filename):
    words = set(file(filename).read().upper().split())
    prefx = set(p for w in words for p in prefixes(w))
    return words, prefx


def prefixes(word):
    '''Return a set of prefixes if a word, excluding the word itself.'''
    return set(word[:i] for i in xrange(len(word)))


def removed(letters, remove):
    for L in remove:
        letters = letters.replace(L, '', 1)
    return letters


FILENAME = "../4kwords.txt"
WORDS, PREFIXES = readwordlist(FILENAME)
