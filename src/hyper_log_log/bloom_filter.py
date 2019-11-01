import logging

import numpy as np
from bitarray import bitarray
from streaming_algorithms.bloom_filter.tools import minimal_memory_footprint, \
    false_positive_rate


class BloomFilter:
    def __init__(self, bit_array_size, nb_salt):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f'Bloom filter parameters:'
                         f' bit-array size: {bit_array_size}'
                         f' number of hash functions: {nb_salt}')
        self.bit_array_size = bit_array_size
        self.nb_salt = nb_salt
        self.bit_array = bitarray(bit_array_size)
        self.bit_array.setall(False)

    def add_item(self, item):
        for salt in range(self.nb_salt):
            address = hash(''.join([str(salt), str(item)])) % self.bit_array_size
            self.bit_array[address] = True

    def retrieve_item(self, item):
        for salt in range(self.nb_salt):
            address = hash(''.join([str(salt), str(item)])) % self.bit_array_size
            if not self.bit_array[address]:
                return False
        return True

    @classmethod
    def minimal_false_positive_rate_bloom_filter(cls, bit_array_size, input_cardinal):
        logger = logging.getLogger(__name__)
        floor_nb_salt = int(bit_array_size * np.log(2) / input_cardinal)
        ceil_nb_salt = floor_nb_salt + 1
        floor_false_positive_rate = false_positive_rate(bit_array_size=bit_array_size,
                                                        nb_salt=floor_nb_salt,
                                                        input_cardinal=input_cardinal)
        ceil_false_positive_rate = false_positive_rate(bit_array_size=bit_array_size,
                                                       nb_salt=ceil_nb_salt,
                                                       input_cardinal=input_cardinal)
        if ceil_false_positive_rate < floor_false_positive_rate:
            optimal_nb_salt = ceil_nb_salt
            optimal_false_positive_rate = ceil_false_positive_rate
        else:
            optimal_nb_salt = floor_nb_salt
            optimal_false_positive_rate = floor_false_positive_rate

        logger.info(f'False positive rate: {optimal_false_positive_rate * 100}%')
        return cls(bit_array_size=bit_array_size, nb_salt=optimal_nb_salt)

    @classmethod
    def minimal_memory_bloom_filter(cls, input_cardinal, error_rate):
        minimal_bit_array_size = minimal_memory_footprint(input_cardinal=input_cardinal,
                                                          error_rate=error_rate)
        return cls.minimal_false_positive_rate_bloom_filter(
            bit_array_size=minimal_bit_array_size,
            input_cardinal=input_cardinal)
