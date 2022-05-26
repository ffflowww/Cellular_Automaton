import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    s = 0
    s_cross = neighbors[(-1, 0)]['value'] + neighbors[(1, 0)]['value'] + neighbors[(0, -1)]['value'] + neighbors[(0, 1)]['value']
    for coord, neigh in neighbors.items():
        s += neigh['value']

    p = [0.3, 0.25]

    if cell['value'] == 0 and s_cross > 0:
        if s == 1:
            cell['value'] = np.random.choice([1, 0], 1, p=[p[0], 1 - p[0]])[0]
        elif s == 2:
            cell['value'] = np.random.choice([1, 0], 1, p=[p[1], 1 - p[1]])[0]
    return cell


def initializer(game):
    game.field[:]['value'][game.sizes[0] // 2][game.sizes[1] // 2] = 1
