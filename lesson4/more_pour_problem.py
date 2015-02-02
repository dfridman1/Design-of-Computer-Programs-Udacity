# *** MORE POUR PROBLEM ***

# In this problem, you will solve the pouring problem for an arbitrary
# number of glasses. Write a function, more_pour_problem, that takes 
# as input capacities, goal, and (optionally) start. This function should 
# return a path of states and actions.
#
# Capacities is a tuple of numbers, where each number represents the 
# volume of a glass. 
#
# Goal is the desired volume and start is a tuple of the starting levels
# in each glass. Start defaults to None (all glasses empty).
#
# The returned path should look like [state, action, state, action, ... ]
# where state is a tuple of volumes and action is one of ('fill', i), 
# ('empty', i), ('pour', i, j) where i and j are indices indicating the 
# glass number.


import search_generalization



def more_pour_problem(capacities, goal, start=None):
    '''The first argument is a tuple of capacities (numbers) of glasses; the
    goal is a number which we must achieve in some glass.  start is a tuple
    of starting levels for each glass; if None, that means 0 for all.
    Start at start state and follow successors until we reach the goal.
    Keep track of frontier and previously explored; fail when no frontier.
    On success return a path: a [state, action, state2, ...] list, where an
    action is one of ('fill', i), ('empty', i), ('pour', i, j), where
    i and j are indices indicating the glass number.'''

    if start is None:
        start = (0, ) * len(capacities)
    goal_function = is_goal(goal)
    successors_function = successors(capacities)
    return search_generalization.generalized_bfs(goal_function, successors_function)(start)


def is_goal(goal):
    "Return True if one of the glasses contains the goal level of water"
    def _is_goal(state):
        return goal in state
    return _is_goal


def successors(capacities):
    def _f(state):
       return dict_union(fill(capacities, state), empty(state), transfer(capacities, state))
    return _f


def fill(capacities, state):
    '''Return a dict {state:action} where action is filling
    up one of the cups'''
    return { replace(state, i, capacities[i]) : ('fill', i) for i in xrange(len(state)) }



def empty(state):
    '''Return a dict {state:action} where action is emptying 
    one of the cups'''
    return { replace(state, i, 0) : ('empty', i) for i in xrange(len(state)) }




def transfer(capacities, state):
    '''Return a dict {state:action} where action is transferring
    from one cup to another'''
    D = {}
    N = len(state)
    for i in xrange(N):
        for j in xrange(N):
            if i == j: continue
            amount = min(capacities[j] - state[j], state[i])
            replaced_i = replace(state, i, state[i] - amount)
            replaced = replace(replaced_i, j, state[j] + amount)
            D[replaced] = ('pour', i, j)
    return D



def replace(iterable, i, value):
    '''Replace item at index i with value'''
    l = list(iterable)
    l[i] = value
    return type(iterable)(l)


def dict_union(*dicts):
    D = {}
    for d in dicts:
        D.update(d)
    return D
