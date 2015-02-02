# *** GENERALIZATION OF THE LOWEST COST SEARCH PROBLEM ***
import bridge_optimized


def lowest_cost_search(start, successors, is_goal, action_cost):
    '''Return the lowest cost path, starting from start state,
    and considering successors(state) => {state:(action, total_cost)},
    that ends in a state for which is_goal(state) is true, where
    the cost of a path is the sum of action costs, which are
    given by action_cost(action).'''

    explored = set()
    frontier = [[start]]

    while frontier:
        path = frontier.pop(0)
        s = final_state(path)
        if is_goal(s):
            return path
        explored.add(s)
        pcost = path_cost(path)

        for (state, action) in successors(s).items():
            if state not in explored:
                total_cost = pcost + action_cost(action)
                path2 = path + [(action, total_cost), state]
                add_to_frontier(path2, frontier)
        frontier.sort(key=path_cost)
    return Fail

Fail = []


def path_cost(path):
    '''Return the total cost of the parth, where path is
    described by [state, (action, total_cost), state,...]'''
    return 0 if len(path) < 3 else path[-2][-1]


def final_state(path):
    "Return the final state of the path"
    return path[-1]


def add_to_frontier(path, frontier):
    '''Add path to the frontier, replacing any costlier
    path if one exists'''
    old = None
    for i, p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) > path_cost(path):
        frontier[old] = path
    elif old is None:
        frontier.append(path)









#solution to the bridge problem using lowest_cost_search

def bridge_problem_using_lowest_cost_search():

    def bridge_is_goal(state):
        here, there, light = state
        return not here

    def _f(here, there=frozenset([]), light=0):
        state = (here, there, light)
        return lowest_cost_search(state, bridge_optimized.bsuccessors,
                                  bridge_is_goal, bridge_optimized.action_cost)
    return _f

bridge_problem = bridge_problem_using_lowest_cost_search()
