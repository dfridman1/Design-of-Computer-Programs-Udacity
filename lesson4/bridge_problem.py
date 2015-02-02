# *** BRIDGE PROBLEM ***

from itertools import combinations

def bridge_problem(here, there=frozenset([]), light=0):
    start = (frozenset(here), there, light, 0)
    explored = set(start)
    frontier = [[start]]

    while frontier:
        path = frontier.pop(0)
        state = path[-1]
        if not state[0]:
            return path
        for (state, action) in bsuccessors(state).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
        frontier.sort(key=elapsed_time)
    return Fail

Fail = []



def bsuccessors(state):
    '''Return a dict {state:action} pairs. A state is a (here,there,light,t)
    tuple where here and there are frozensets of people (indicated by
    there times) and light is 0 if light is here, 1 if it is there; t
    indicates the total elapsed time. Action is represented as a tuple
    (person1, person2, arrow), where arrow is '->' for here to there and
    '<-' for there to here'''
    here, there, light, t = state
    if light == 0:
        return { (here - frozenset([a, b]), there | frozenset([a, b]), 1, t + max([a, b])) : (a, b, '->')
                 for a in here for b in here }
    elif light == 1:
        return { (here | frozenset([a, b]), there - frozenset([a, b]), 0, t + max([a, b])) : (a, b, '<-')
                 for a in there for b in there }


def elapsed_time(path):
    return path[-1][-1]
