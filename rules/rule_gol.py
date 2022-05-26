import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)

    neighbors_alive = 0
    for coord, neigh in neighbors.items():
        neighbors_alive += neigh['value']

    if (neighbors_alive == 3) or (neighbors_alive == 2 and cell['value'] == 1):
        cell['value'] = 1
    else:
        cell['value'] = 0
    return cell


def initializer(game):
    p = 0.5
    game.field[:]['value'] = np.random.choice([1, 0], game.sizes, p=[p, 1 - p])
