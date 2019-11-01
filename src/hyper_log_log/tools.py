import numpy as np


def false_positive_rate(bit_array_size, nb_salt, input_cardinal):
    return (1 - (1 - 1 / bit_array_size) ** (nb_salt * input_cardinal)) ** nb_salt


def minimal_memory_footprint(input_cardinal, error_rate):
    return int(
        input_cardinal * np.log(error_rate) / np.log(1 / 2 ** np.log(2))) + 1
