# *** OPTIMIZED SOLUTION TO THE BRIDGE PROBLEM ***




def action_cost(action):
    '''Return the cost of an action; action is described by a
    tuple (a, b, '->') or (a, b, '<-') where a and b are times
    it takes person 'a' and person 'b' to cross the bridge'''
    if len(action) == 2:
        return action[0]
    else:
        a, b, direction = action
        return max(a, b)


def path_cost(path):
    "Return the total cost of the path"
    return 0 if len(path) < 3 else path[-2][-1]


def final_state(path):
    "Return the final state of the path"
    return path[-1]


def addToFrontier(path, frontier):
    "Add path to frontier, replacing costlier path if one exists"
    old = None
    for i, p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) > path_cost(path):
        frontier[old] = path
    elif old is None:
        frontier.append(path)

    

def bsuccessors(state):
    '''Given a state (here, there, light), return a dict
    {state:action} of possible actions'''
    here, there, light = state
    if light == 0:
        return { (here - frozenset([a, b]), there | frozenset([a, b]), 1) : tuple(set([a, b])) + ('->',)
                 for a in here for b in here  }
    elif light == 1:
        return { (here | frozenset([a, b]), there - frozenset([a, b]), 0) : tuple(set([a, b])) + ('<-',)
                 for a in there for b in there }


Fail = []

def bridge_solution(here, there=frozenset([]), light=0):
    '''Return a sequence of actions required for people from 'here'
    to get to the other side of the bridge in the shortest period
    of time'''

    state = (here, there, light)
    explored = set()
    frontier = [[state]]

    while frontier:
        path = frontier.pop(0)
        here, there, light = st = final_state(path)
        if not here:
            return path
        explored.add(st)
        total_time = path_cost(path)
        for (state, action) in bsuccessors(st).items():
            if state not in explored:
                new_total_time = total_time + action_cost(action)
                path2 = path + [(action, new_total_time), state]
                addToFrontier(path2, frontier)
        frontier.sort(key=path_cost)
    return Fail
