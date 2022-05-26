import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    s = cell['value']
    for coord, neigh in neighbors.items():
        s += neigh['value']
    if s < 4 or s == 5:
        cell['value'] = 0
    else:
        cell['value'] = 1
    return cell


def initializer(game):
    p = 0.5
    game.field[:]['value'] = np.random.choice([1, 0], game.sizes, p=[p, 1 - p])
