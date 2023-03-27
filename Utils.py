""" It returns the coordinates of a given direction.
    Example: FRONT -> -1,0
             LEFT  -> 0,-1
"""
from Constants import *

map_direction_coordinates = {
    0: [-1,0],
    1: [0, 1],
    2: [1, 0],
    3: [0,-1]
}

opposite_directions = {
    LEFT: RIGHT,
    RIGHT: LEFT,
    FRONT: BACK,
    BACK: FRONT
}

""" This is used to obtain the orthogonal directions for a given direction.
    Examples: FRONT -> orthogonals are [LEFT, RIGHT]
              RIGHT -> orthogonals are [FRONT, DOWN]
"""
orthogonal_directions = {
    0: [[0,-1, LEFT],[0,1, RIGHT]], # ↑: (←,→)
    1: [[-1,0, FRONT],[1,0, BACK]], # →: (↑,↓)
    2: [[0,1, RIGHT],[0,-1, LEFT]], # ↓: (←,→)
    3: [[-1,0, FRONT],[1,0, BACK]]  # ←: (↑,↓)
}

""" It returns the coordinates of a given direction.
    Example: FRONT -> -1,0
             LEFT  -> 0,-1
"""
map_direction_coordinates = {
    0: [-1,0],
    1: [0, 1],
    2: [1, 0],
    3: [0, -1]
}