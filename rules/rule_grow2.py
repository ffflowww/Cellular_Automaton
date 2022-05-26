import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    s = 0
    s_wall = False
    s_wall = (neighbors[(-1, -1)]['value'] + neighbors[(-1, 0)]['value'] + neighbors[(-1, 1)]['value'] == 3) or s_wall
    s_wall = (neighbors[(-1, -1)]['value'] + neighbors[(0, -1)]['value'] + neighbors[(1, -1)]['value'] == 3) or s_wall
    s_wall = (neighbors[(1, -1)]['value'] + neighbors[(1, 0)]['value'] + neighbors[(1, 1)]['value'] == 3) or s_wall
    s_wall = (neighbors[(-1, 1)]['value'] + neighbors[(0, 1)]['value'] + neighbors[(1, 1)]['value'] == 3) or s_wall
    s_cross = neighbors[(-1, 0)]['value'] + neighbors[(1, 0)]['value'] + neighbors[(0, -1)]['value'] + neighbors[(0, 1)]['value']

    for coord, neigh in neighbors.items():
        s += neigh['value']

    if cell['value'] == 0:
        if s == 1 and s_cross > 0:
            cell['value'] = 1
        if s == 3 and s_wall:
            cell['value'] = np.random.choice([1, 0], 1, p=[0.002, 0.998])[0]
    return cell


def initializer(game):
    game.field[:]['value'][game.sizes[0] // 2][game.sizes[1] // 2] = 1
