import numpy as np


dt = np.dtype([('value', np.int32),
               ('fraction', np.int32)])


def rule(game, coord):
    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    neigh_fraction1 = 0
    neigh_fraction2 = 0
    for coord, neigh in neighbors.items():
        if neigh['value'] > 0:
            if neigh['fraction'] == 1:
                neigh_fraction1 += 1
            else:
                neigh_fraction2 += 1

    if (neigh_fraction1 == neigh_fraction2 == 3) or (neigh_fraction1 == neigh_fraction2 == 2):
        pass
    elif neigh_fraction1 == 3:
        if cell['fraction'] == 1:
            cell['value'] += 1
        else:
            cell['value'] = 1
            cell['fraction'] = 1
    elif neigh_fraction2 == 3:
        if cell['fraction'] == 2:
            cell['value'] += 1
        else:
            cell['value'] = 1
            cell['fraction'] = 2
    elif (neigh_fraction1 == 2 and cell['fraction'] == 1) or (neigh_fraction2 == 2 and cell['fraction'] == 2):
        pass
    else:
        if cell['value'] > 1:
            cell['value'] -= 1
        else:
            cell['value'] = 0
            cell['fraction'] = 0

    return cell


def initializer(game):
    p = 0.5
    p2 = 0.5
    game.field[:]['value'] = np.random.choice([1, 0], game.sizes, p=[p, 1 - p])
    mask = game.field[:]['value'] > 0
    game.field[:]['fraction'][mask] = np.random.choice([1, 2], game.sizes, p=[p2, 1 - p2])[mask]
