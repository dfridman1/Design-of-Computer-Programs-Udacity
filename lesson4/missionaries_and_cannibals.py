# *** MISSIONARIES AND CANNIBALS PUZZLE ***



def csuccessors(state):
    '''Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors.'''
    M1, C1, M2, C2, B = state
    if C1 > M1 > 0 or C2 > M2 > 0: return {}

    if B == 0:
        return { (M1 - a, C1 - b, M2 + a, C2 + b, 1) : (a * 'M' + b * 'C', '->')
                 for a in xrange(3) for b in xrange(3) if M1 - a >= 0 and C1 - b >= 0
                 and a + b > 0 and a + b <= 2 }
    elif B == 1:
        return { (M1 + a, C1 + b, M2 - a, C2 - b, 0) : (a * 'M' + b * 'C', '<-')
                 for a in xrange(3) for b in xrange(3) if M2 - a >= 0 and C2 - b >= 0
                 and a + b > 0 and a + b <= 2 }



Fail = []
    
def missionaries_cannibals(M, C):
    state = (M, C, 0, 0, 0)
    explored = set()
    frontier = [[state]]

    while frontier:
        path = frontier.pop(0)
        m1, c1, m2, c2, b = st = final_state(path)
        if m1 == 0 and c1 == 0:
            return path
        explored.add(st)
        
        for (state, action) in csuccessors(st).items():
            if state not in explored:
                path2 = path + [action, state]
                frontier.append(path2)
    return Fail


def final_state(path):
    return path[-1]
