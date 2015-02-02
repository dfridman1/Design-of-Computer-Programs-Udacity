# *** WATER POURING PROBLEM ***

def water_pouring(X, Y, goal, start=(0,0)):
    '''Given 2 glasses with capacities X and Y and the starting
    levels of water in each of them (described by a tuple start),
    return the shortest sequence of steps to reach level goal in
    at least one of the glasses. The valid steps for manipulating
    water in glasses are: empty, fill, transfer from one to another'''

    assert start[0] <= X and start[1] <= Y
    if goal in start:
        return [start]

    explored = set([start])
    frontier = [[start]]

    while frontier:
        path = frontier.pop(0)
        (x, y) = path[-1]
        if goal in (x, y):
            return path
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                frontier.append(path2)
    return Fail

Fail = []


def successors(x, y, X, Y):
    '''Return a dict of {state:action} pairs describing what can be
    reached from the (x, y) state, and how.'''
    return { (X, y): "fill X", (x, Y): "fill Y",
             (0, y): "empty X", (x, 0): "empty Y",
             ((0, x + y) if x + y <= Y else (x - Y + y, Y)): "X -> Y",
             ((x + y, 0) if x + y <= X else (X, y - X + x)): "Y -> X"
           }
