import numpy as np
import os
from time import localtime, strftime
from PIL import Image
import matplotlib.pyplot as plt
import multiprocessing as mp
import itertools
import time
import psutil

# from rules.rule_gol import dt, rule, initializer
# from rules.rule_gol_sustainable import dt, rule, initializer
# from rules.rule_gol_sustainable_fraction import dt, rule, initializer
# from rules.rule_repentance import dt, rule, initializer
# from rules.rule_majority_with_twist import dt, rule, initializer
# from rules.rule_grow import dt, rule, initializer
# from rules.rule_grow2 import dt, rule, initializer
# from rules.rule_grow3 import dt, rule, initializer
# from rules.rule_fraction_age import dt, rule, initializer
from rules.rule_fraction_with_death import dt, rule, initializer


class CustomError(Exception):
    """Exception raised for errors in the input salary.

    Attributes:
        value -- error value
        message -- explanation of the error
    """

    def __init__(self, value, message):
        self.value = value
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.value} -> {self.message}'


class Game:
    def __init__(self, sizes: tuple, is_border_cyclic: bool, unit_dt, rule_function, initializer_func):
        min_field_size = 10
        if sizes[0] < min_field_size:
            raise CustomError(sizes[0], f"Field size should be greater than {min_field_size}")
        if sizes[1] < min_field_size:
            raise CustomError(sizes[1], f"Field size should be greater than {min_field_size}")

        for name in unit_dt.names:
            if not (unit_dt[name] == np.int32 or unit_dt[name] == np.float32):
                raise CustomError(unit_dt[name], "You should use only np.int32 or np.float32 as types")

        if not os.path.exists("../data"):
            os.mkdir("../data")
        loc_time = strftime("run_%Y-%m-%d_%H-%M-%S", localtime())
        self.path = os.path.join(os.getcwd(), "../data", loc_time)
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        if not os.path.exists(os.path.join(self.path, "gifs")):
            os.mkdir(os.path.join(self.path, "gifs"))

        self.sizes = sizes
        self.rule_function = rule_function
        self.is_border_cyclic = is_border_cyclic
        self.initializer_func = initializer_func
        self.unit_dt = unit_dt

        self.field = np.zeros(sizes, dtype=self.unit_dt)
        self.zero_cell = np.zeros(1, dtype=self.unit_dt)
        # self.shared_memory = mp.RawArray(np.ctypeslib.as_ctypes_type(self.unit_dt), self.field.flatten())

        self.initializer_func(self)

        # parallel stuff
        self.cpu_available = psutil.cpu_count(logical=False)
        list_all_coords = [coord for coord in itertools.product(range(self.sizes[0]), range(self.sizes[1]))]
        chunk_sizes, extra = divmod(len(list_all_coords), self.cpu_available)
        if extra > 0:
            chunk_sizes += 1
        self.coords_chunked = [list_all_coords[i * chunk_sizes:(i + 1) * chunk_sizes] for i in range(self.cpu_available)]

    def _update_field(self):
        with mp.Pool(processes=self.cpu_available) as p:
            res = p.map(self._task_calc, self.coords_chunked)

        for coords_chunk, res_chunk in zip(self.coords_chunked, res):
            for c, r in zip(coords_chunk, res_chunk):
                self.field[c] = r

        # with mp.Pool(processes=self.cpu_available) as p:
        #     res = p.starmap(self._task_calc, zip(self.coords_chunked, itertools.repeat()))

    def _task_calc(self, chunk):
        return [self.rule_function(self, coord) for coord in chunk]

    def get_cell(self, coord):
        if self.is_border_cyclic:
            if coord[0] < 0:
                coord[0] += self.sizes[0]
            elif coord[0] >= self.sizes[0]:
                coord[0] -= self.sizes[0]

            if coord[1] < 0:
                coord[1] += self.sizes[1]
            elif coord[1] >= self.sizes[1]:
                coord[1] -= self.sizes[1]

            return self.field[coord].copy()
        else:
            if coord[0] < 0 or coord[0] >= self.sizes[0] or coord[1] < 0 or coord[1] >= self.sizes[1]:
                return self.zero_cell[0].copy()
            return self.field[coord].copy()

    def get_neighbors(self, coord, radius):
        if radius < 1:
            raise CustomError(radius, "Radius for getting neighbors should be greater than 1")
        neighbors = dict()
        for i in range(-radius, radius + 1, 1):
            for j in range(-radius, radius + 1, 1):
                if i == j == 0:
                    continue
                neighbors[(i, j)] = self.get_cell((coord[0] + i, coord[1] + j))
        return neighbors

    def _save_txt_png(self, n_epoch):
        for field_name in self.unit_dt.names:
            if self.unit_dt[field_name] == np.int32:
                np.savetxt(os.path.join(self.path, f"epoch{n_epoch}_{field_name}.txt"), self.field[:][field_name], "%d")
            else:
                np.savetxt(os.path.join(self.path, f"epoch{n_epoch}_{field_name}.txt"), self.field[:][field_name], "%f")

            plt.imsave(os.path.join(self.path, f"epoch{n_epoch}_{field_name}_seq.png"), self.field[:][field_name], cmap='magma_r')
            plt.imsave(os.path.join(self.path, f"epoch{n_epoch}_{field_name}_bin.png"), self.field[:][field_name] > 0, cmap='Greys')
            plt.imsave(os.path.join(self.path, f"epoch{n_epoch}_{field_name}_cat.png"), self.field[:][field_name], cmap='gist_ncar_r')

    def _save_meta(self, n_epochs):
        with open(os.path.join(self.path, "meta.txt"), "w") as f:
            f.write(f"{self.sizes[0]} {self.sizes[1]}\n")
            f.write(f"{n_epochs}\n")
            f.write(f"{len(self.unit_dt.names)}\n")
            for field_name in self.unit_dt.names:
                f.write(f"{field_name} {self.unit_dt[field_name]}\n")

    def _save_gifs(self, n_epochs):
        img_big = None
        big_name = ""
        for field_name in self.unit_dt.names:
            big_name += f"{field_name}_"
            images_bin = []
            images_seq = []
            images_cat = []
            images_all = []
            for i in range(n_epochs + 1):
                images_bin.append(Image.open(os.path.join(self.path, f"epoch{i}_{field_name}_bin.png")))
                images_seq.append(Image.open(os.path.join(self.path, f"epoch{i}_{field_name}_seq.png")))
                images_cat.append(Image.open(os.path.join(self.path, f"epoch{i}_{field_name}_cat.png")))
                images_all.append(Image.fromarray(np.vstack((images_bin[-1], images_seq[-1], images_cat[-1]))))
                if img_big is not None:
                    img_big[i] = Image.fromarray(np.hstack((img_big[i], images_all[-1])))
            images_bin[0].save(os.path.join(self.path, "gifs", f"gif_{field_name}_bin.gif"), save_all=True, append_images=images_bin[1:], duration=50, loop=0, optimize=False)
            images_seq[0].save(os.path.join(self.path, "gifs", f"gif_{field_name}_seq.gif"), save_all=True, append_images=images_seq[1:], duration=50, loop=0, optimize=False)
            images_cat[0].save(os.path.join(self.path, "gifs", f"gif_{field_name}_cat.gif"), save_all=True, append_images=images_cat[1:], duration=50, loop=0, optimize=False)
            images_all[0].save(os.path.join(self.path, "gifs", f"gif_{field_name}.gif"), save_all=True, append_images=images_all[1:], duration=50, loop=0, optimize=False)
            if img_big is None:
                img_big = images_all
        big_name = big_name[:-1]
        img_big[0].save(os.path.join(self.path, "gifs", f"gif_{big_name}.gif"), save_all=True, append_images=img_big[1:], duration=50, loop=0, optimize=False)

    def run(self, a_epochs):
        self._save_meta(n_epochs=a_epochs)
        self._save_txt_png(n_epoch=0)
        for i in range(1, a_epochs + 1):
            self._update_field()
            self._save_txt_png(n_epoch=i)
        self._save_gifs(n_epochs=a_epochs)


if __name__ == "__main__":
    field_size = (256, 256)
    epochs = 512
    g = Game(sizes=field_size, is_border_cyclic=False, unit_dt=dt, rule_function=rule, initializer_func=initializer)
    g.run(epochs)

