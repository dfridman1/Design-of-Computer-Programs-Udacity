# This problem deals with the one-player game foxes_and_hens. This 
# game is played with a deck of cards in which each card is labelled
# as a hen 'H', or a fox 'F'. 
# 
# A player will flip over a random card. If that card is a hen, it is
# added to the yard. If it is a fox, all of the hens currently in the
# yard are removed.
#
# Before drawing a card, the player has the choice of two actions, 
# 'gather' or 'wait'. If the player gathers, she collects all the hens
# in the yard and adds them to her score. The drawn card is discarded.
# If the player waits, she sees the next card. 
#
# Your job is to define two functions. The first is do(action, state), 
# where action is either 'gather' or 'wait' and state is a tuple of 
# (score, yard, cards). This function should return a new state with 
# one less card and the yard and score properly updated.
#
# The second function you define, strategy(state), should return an 
# action based on the state. This strategy should average at least 
# 1.5 more points than the take5 strategy.


import random



def foxes_and_hens(strategy, foxes=7, hens=45):
    "Play the game of foxes and hens."
    state = (score, yard, cards) = (0, 0, 'F' * foxes + 'H' * hens)
    while cards:
        action = strategy(state)
        state = (score, yard, cards) = do(action, state)
    return score + yard




def do(action, state):
    "Apply action to state, returning a new state."
    score, yard, cards = state
    card = random.choice(cards)
    cards = cards.replace(card, '', 1)
    
    if action == 'wait':
        return (score, yard + 1, cards) if card == 'H' else (score, 0, cards)
    elif action == 'gather':
        return (score + yard, 0, cards)
    raise ValueError


def take5(state):
    "A strategy that waits until there are 5 hens in yard, then gathers."
    (score, yard, cards) = state
    if yard < 5:
        return 'wait'
    else:
        return 'gather'

def average_score(strategy, N=1000):
    return sum(foxes_and_hens(strategy) for _ in xrange(N)) / float(N)

def superior(A, B=take5):
    "Does strategy A have higher strategy score than B, by more than 1.5 point?"
    return average_score(A) - average_score(B) > 1.5

def strategy(state):
    (score, yard, cards) = state
    if 'F' not in cards:
        return 'wait'
    elif yard < 3:
        return 'wait'
    else:
        return 'gather'
