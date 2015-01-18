import itertools, collections



# Hopper, Kay, Liskov, Perlis, and Ritchie live on
# different floors of a five-floor apartment building.
#
# Hopper does not live on the top floor.
# Kay does not live on the bottom floor.
# Liskov does not live on either the top or the bottom floor.
# Perlis lives on a higher floor than does Kay.
# Ritchie does not live on a floor adjacent to Liskov's.
# Liskov does not live on a floor adjacent to Kay's.
#
# Where does everyone live?



floors = [1, 2, 3, 4, 5]
orderings = list(itertools.permutations(floors))


def are_neighbours(h1, h2):
    return abs(h1 - h2) == 1



def c(L):
    """keeps track of the number of times the function is called
    and the number of permutations we yield"""
    c.starts += 1
    for item in L:
        c.items += 1
        yield item

c.starts = 0
c.items = 0


def floor_puzzle():
    return list(next( (Hopper, Kay, Liskov, Perlis, Ritchie) for (Hopper, Kay, Liskov, Perlis, Ritchie) in c(orderings)
                  if Hopper != 5 and Kay != 1 and Liskov != 1 and Liskov != 5 and Perlis > Kay
                  and not are_neighbours(Ritchie, Liskov) and not are_neighbours(Liskov, Kay)))
