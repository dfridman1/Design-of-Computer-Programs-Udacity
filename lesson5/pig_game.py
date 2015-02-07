# *** PIG GAME ***

import random
from functools import update_wrapper



other = {0 : 1, 1 : 0}
goal = 40


def hold(state):
    '''Apply the hold action to a state to yield a new state:
    Reap the pending points and it becomes the other player's turn.'''
    p, me, you, pending = state
    return other[p], you, me + pending, 0


def roll(state, d):
    '''Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points), and it is
    the other player's turn. If d > 1, add d to 'pending' points.'''

    p, me, you, pending = state
    if d == 1:
        return other[p], you, me + 1, 0
    else:
        return p, me, you, pending + d


def clueless(state):
    "Choose either 'hold' or 'roll'"
    return random.choice(['hold', 'roll'])

    

def hold_at(x):
    '''Return a strategy that holds iff pending >= x or player reaches goal.'''
    def strategy(state):
        p, me, you, pending = state
        if me + pending >= goal or pending >= x:
            return 'hold'
        else:
            return 'roll'
    strategy.__name__ = "hold at %s" % x
    return strategy


def dierolls():
    "Generate die rolls."
    while True:
        yield random.randint(1, 6)


def play_pig(A, B, dierolls=dierolls()):
    '''Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one players's score exceeds the goal, return that player'''
    strategies = [A, B]
    state = (0,) * 4
    while True:
        p, me, you, pending = state
        if me >= goal:
            return strategies[p]
        elif you >= goal:
            return strategies[other[p]]
        else:
            action = strategies[p](state)
            if action == 'hold':
                state = hold(state)
            elif action == 'roll':
                state = roll(state, next(dierolls))
            else:
                return strategies[other[p]]



def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d
            

@decorator
def memo(f):
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            return f(*args)
    return _f



def Q_pig(state, action, Pwin):
    "The expected value of choosing action in state."
    if action == 'hold':
        return 1 - Pwin(hold(state))
    elif action == 'roll':
        return (1 - Pwin(roll(state, 1))
                + sum(Pwin(roll(state, d)) for d in (2, 3, 4, 5, 6))) / 6.
    raise ValueError



def Pwin(state):
    '''The utility of a state; here just the probability that an optimal
    player whose turn it is to make can win from the current state.'''
    _, me, you, pending = state
    @memo
    def _Pwin(me, you, pending):
        if me + pending >= goal:
            return 1
        if you >= goal:
            return 0
        Proll = (1 - _Pwin(you, me + 1, 0) +
                 sum(_Pwin(me, you, pending + i) for i in (2, 3, 4, 5, 6))) / 6.
        return Proll if not pending else max(1 - _Pwin(you, me + pending, 0),
                                             Proll)
    return _Pwin(me, you, pending)


@memo
def difference(state):
    "The utility of a state; here the winning differential."
    p, me, you, pending = state
    if me + pending >= goal or you >= goal:
        return me + pending - you
    else:
        return max(Q_pig(state, action, difference) for action in pig_actions(state))

    
def pig_actions(state):
    _, _, _, pending = state
    return ['roll', 'hold'] if pending else ['roll']


def best_action(state, actions, Q, U):
    "Return the best action in a state according to a utility U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)

def max_wins(state):
    "The optimal pig strategy chooses an action with the highest probability win."
    return best_action(state, pig_actions, Q_pig, Pwin)

def max_diffs(state):
    '''A strategy that maximmizes the expected difference between my final score
    and my opponent's.'''
    return best_action(state, pig_actions, Q_pig, difference)
