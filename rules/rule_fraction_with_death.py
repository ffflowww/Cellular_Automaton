import numpy as np


dt = np.dtype([('power', np.int32),
               ('fraction', np.int32),
               ('age', np.int32)])


def rule(game, coord):
    max_age = 10

    cell = game.get_cell(coord)
    neighbors = game.get_neighbors(coord, radius=1)
    neigh1_power = 0
    neigh2_power = 0
    for coord, neigh in neighbors.items():
        if neigh['power'] > 0:
            if neigh['fraction'] == 1:
                neigh1_power += neigh['power']
            else:
                neigh2_power += neigh['power']

    if cell['age'] == max_age:
        cell['power'] += 1
        cell['age'] = 1
    elif cell['power'] == 0:
        if neigh1_power > neigh2_power:
            cell['power'] = 1
            cell['fraction'] = 1
            cell['age'] = 1
        elif neigh1_power < neigh2_power:
            cell['power'] = 1
            cell['fraction'] = 2
            cell['age'] = 1
    else:
        if neigh1_power > neigh2_power:
            if cell['fraction'] == 1:
                cell['age'] += 1
            else:
                cell['power'] = 0
                cell['fraction'] = 0
                cell['age'] = 0
        elif neigh1_power < neigh2_power:
            if cell['fraction'] == 2:
                cell['age'] += 1
            else:
                cell['power'] = 0
                cell['fraction'] = 0
                cell['age'] = 0
        else:
            cell['age'] += 1

    return cell


def initializer(game):
    p = 0.5
    p2 = 0.5
    game.field[:]['power'] = np.random.choice([1, 0], game.sizes, p=[p, 1 - p])
    mask = game.field[:]['power'] > 0
    game.field[:]['fraction'][mask] = np.random.choice([1, 2], game.sizes, p=[p2, 1 - p2])[mask]
    game.field[:]['age'][mask] = np.ones(game.sizes)[mask]
