# *** SUBPALINDROME PROBLEM ***



# Write a function, longest_subpalindrome_slice(text) that takes
# a string as input and returns the i and j indices that
# correspond to the beginning and end indices of the longest
# palindrome in the string.




def longest_subpalindrome_slice(text):
    "Returns (i, j) such that text[i:j] is the longest palindrome in text."
    text = text.lower()
    text_length = len(text)
    longest_pal = (0, 0)

    def solve(i, j):
        if i < 0 or j >= text_length or text[i] != text[j]:
            return (i+1, j)
        else:
            return solve(i-1, j+1)

    get_length = lambda x: x[1] - x[0]

    for i in xrange(text_length):
        longest_pal = max([longest_pal, solve(i, i+1)], key=get_length)
        longest_pal = max([longest_pal, solve(i-1, i+1)], key=get_length)

    return longest_pal



def test():
    L = longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8, 21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    return 'tests pass'

print test()
