import numpy as np


dt = np.dtype([('value', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    cell['value'] = (neighbors[(-1, 0)]['value'] + neighbors[(1, 0)]['value'] + neighbors[(0, -1)]['value'] + neighbors[(0, 1)]['value']) % 2
    return cell


def initializer(game):
    game.field[:]['value'][game.sizes[0] // 2][game.sizes[1] // 2] = 1
