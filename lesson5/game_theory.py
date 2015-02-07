# *** GAME THEORY EXAMPLE ***

# A player is facing a decision: to keep $1m he has in his pocket,
# or roll a fair coin for an opportunity to win $3m in total in the
# case of a head; if tail lands, he loses it all



million = 1000000

def Q(state, action, U):
    "The expected value of the action given utility function U"
    if action == 'hold':
        return U(state + 1 * million)
    if action == 'gamble':
        return U(state + 3 * million) * 0.5 + U(state) * 0.5


def actions(state): return ['hold', 'gamble']

def identity(x): return x

U = identity


def best_action(state, actions, Q, U):
    "Return the optimal action for state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)
