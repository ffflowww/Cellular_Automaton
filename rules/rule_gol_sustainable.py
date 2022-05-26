import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)

    neighbors_alive = 0
    for coord, neigh in neighbors.items():
        if neigh['value'] > 0:
            neighbors_alive += 1

    if neighbors_alive == 3:
        cell['value'] += 1
    elif neighbors_alive == 2 and cell['value'] >= 1:
        cell['value'] += 1
    else:
        if cell['value'] >= 1:
            cell['value'] -= 1
    return cell


def initializer(game):
    p = 0.5
    game.field[:]['value'] = np.random.choice([1, 0], game.sizes, p=[p, 1 - p])
