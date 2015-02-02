# *** GENERALIZING BFS TO A TYPICAL SEARCH PROBLEM ***
import missionaries_and_cannibals



def generalized_bfs(goal_achieved, successors):
    '''Given an initial state, the function determining whether the goal 
    has been achieved (goal_achieved), and a successors function, return
    shortest path leading to the goal'''
    def _f(initial_state):
        explored = set()
        frontier = [[initial_state]]

        while frontier:
            path = frontier.pop(0)
            state = final_state(path)
            if goal_achieved(state):
                return path
            explored.add(state)

            for (state, action) in successors(state).items():
                if state not in explored:
                    path2 = path + [action, state]
                    frontier.append(path2)
        return Fail
    return _f

    
Fail = []

def final_state(path):
    return path[-1]






# missionaries and cannibals puzzle using generalized bfs
def goal_achieved_missionary(state):
    M1, C1, M2, C2, B = state
    return M1 == 0 and C1 == 0

missionaries_and_cannibals = generalized_bfs(goal_achieved_missionary, missionaries_and_cannibals.csuccessors)




# water pouring puzzle using generalized bfs
def water_pouring_gen(X, Y, target_level, start=(0,0)):
    return generalized_bfs(goal_achieved_water_pouring(target_level), water_successors(X, Y))(start)


def goal_achieved_water_pouring(goal):
    def _f(state):
        x, y = state
        return x == goal or y == goal
    return _f


def water_successors(X, Y):
    def _water_successors(state):
        '''Return a dict {state:action} where state is a tuple
        (x, y, X, Y); x = current level in glass 1; y2 = current
        level in glass 2; X and Y are capacities of glass 1 and
        glass 2, respectively.'''
        x, y, = state
        return { (X, y) : 'fill X', (x, Y) : 'fill y',
                 (0, y) : 'empty X', (x, 0) : 'empty Y',
                 ((0, x+y) if x + y <= Y else (x - Y + y, Y)) : 'X -> Y',
                 ((x+y, 0) if x + y <= X else (X, y - X + x)) : 'Y -> X'
               }
    return _water_successors
