# *** SUBWAY PLANNING (HOMEWORK 4) ***


# Write a function, subway, that takes lines as input (read more about
# the **lines notation in the instructor comments box below) and returns
# a dictionary of the form {station:{neighbor:line, ...}, ... }
#
# For example, when calling subway(boston), one of the entries in the
# resulting dictionary should be 'foresthills': {'backbay': 'orange'}.
# This means that foresthills only has one neighbor ('backbay') and
# that neighbor is on the orange line. Other stations have more neighbors:
# 'state', for example, has 4 neighbors.
#
# Once you've defined your subway function, you can define a ride and
# longest_ride function. ride(here, there, system) takes as input
# a starting station (here), a destination station (there), and a subway
# system and returns the shortest path.
#
# longest_ride(system) returns the longest possible ride in a given
# subway system.

import search_generalization




def split_dict_lines(D):
    '''Given a dict with string values, split values on space'''
    for key in D:
        D[key] = D[key].split()


def get_all_stops(D):
    all_stops = set()
    for key in D:
        all_stops = all_stops | set(D[key])
    return all_stops


def getNeighbours(station, map_dict):
    '''Given the name of the station and the map_dict {line1 : [station11, station12,...],
    line2 : [station21, station22,...], ...}, return dict {some_station:some_line,...}
    where some_station is one stop away from the given station, and some_line is the line
    connecting them'''
    neighbours = {}
    for key in map_dict:
        index = find(map_dict[key], station)
        if index != -1:
            if index != 0:
                neighbours[map_dict[key][index - 1]] = key
            try:
                neighbours[map_dict[key][index + 1]] = key
            except IndexError:
                pass
    return neighbours


def find(iterable, value):
    "If value in iterable, return its index, else return -1"
    try:
        return iterable.index(value)
    except ValueError:
        return -1
        



def subway(**lines):
    """Define a subway map. Input is subway(linename='station1 station2...'...).
    Convert that and return a dict of the form: {station:{neighbor:line,...},...}"""
    split_dict_lines(lines)
    all_stations = get_all_stops(lines)
    subway_map = { station : getNeighbours(station, lines) for station in all_stations }
    return subway_map


boston = subway(
    blue='bowdoin government state aquarium maverick airport suffolk revere wonderland',
    orange='oakgrove sullivan haymarket state downtown chinatown tufts backbay foresthills',
    green='lechmere science north haymarket government park copley kenmore newton riverside',
    red='alewife davis porter harvard central mit charles park downtown south umass mattapan')



def successors(state):
    return boston[state]



def ride(here, there, system=boston):
    "Return a path on the subway system from here to there."
    def goal_function(there): return lambda state: state == there
    return search_generalization.generalized_bfs(goal_function(there), successors)(here)


def longest_ride(system):
    """"Return the longest possible 'shortest path' 
    ride between any two stops in the system."""
    all_stops = system.keys()
    return max([ride(a, b) for a in all_stops for b in all_stops if a != b], key=len)


def path_states(path):
    "Return a list of states in the path"
    return path[0::2]


def path_actions(path):
    "Return a list of actions in the path"
    return path[1::2]
