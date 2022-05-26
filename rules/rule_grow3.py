import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    s = 0
    s_cross = neighbors[(-1, 0)]['value'] + neighbors[(1, 0)]['value'] + neighbors[(0, -1)]['value'] + neighbors[(0, 1)]['value']

    for coord, neigh in neighbors.items():
        s += neigh['value']

    p = 0.1
    if cell['value'] == 0:
        if s == 1 and s_cross > 0:
            cell['value'] = np.random.choice([1, 0], 1, p=[0.8, 0.2])[0]
        elif s == 2:
            if neighbors[(-1, 0)]['value'] == 1 and (neighbors[(-1, -1)]['value'] == 1 or neighbors[(-1, 1)]['value'] == 1):
                cell['value'] = np.random.choice([1, 0], 1, p=[p, 1 - p])[0]
            elif neighbors[(1, 0)]['value'] == 1 and (neighbors[(1, -1)]['value'] == 1 or neighbors[(1, 1)]['value'] == 1):
                cell['value'] = np.random.choice([1, 0], 1, p=[p, 1 - p])[0]
            elif neighbors[(0, -1)]['value'] == 1 and (neighbors[(-1, -1)]['value'] == 1 or neighbors[(1, -1)]['value'] == 1):
                cell['value'] = np.random.choice([1, 0], 1, p=[p, 1 - p])[0]
            elif neighbors[(0, 1)]['value'] == 1 and (neighbors[(-1, 1)]['value'] == 1 or neighbors[(1, 1)]['value'] == 1):
                cell['value'] = np.random.choice([1, 0], 1, p=[p, 1 - p])[0]

    return cell


def initializer(game):
    game.field[:]['value'][game.sizes[0] // 2][game.sizes[1] // 2] = 1
