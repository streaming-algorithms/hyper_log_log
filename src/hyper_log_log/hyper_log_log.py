import logging

import numpy as np


class HyperLogLog:
    def __init__(self, nb_buckets):
        self.logger = logging.getLogger(__name__)
        self.bucket_bits = int(np.ceil(np.log(nb_buckets) / np.log(2)))
        self.nb_buckets = 2 ** self.bucket_bits
        self.buckets = [0 for _ in range(self.nb_buckets)]
        self.alpha = 0.7213 / (1 + 1.079 / self.nb_buckets)
        self.logger.info(f'HyperLogLog with {self.nb_buckets} buckets')

    def add_item(self, item):
        binary_item = bin(hash(str(item)) & 0xffffffff)[2:].zfill(32)
        bucket_address = int(binary_item[-self.bucket_bits:], 2)
        nb_leading_zeros = len(binary_item.split('1')[0]) + 1
        self.buckets[bucket_address] = max(
            self.buckets[bucket_address],
            nb_leading_zeros
        )

    def estimate_cardinality(self):
        indicator_function = sum([2 ** -bucket for bucket in self.buckets])
        cardinality = self.alpha * (self.nb_buckets ** 2) / indicator_function
        if cardinality <= 5 * self.nb_buckets / 2:
            self.logger.info('Small range')
            nb_empty_buckets = sum([bucket == 0 for bucket in self.buckets])
            if nb_empty_buckets > 0:
                return self.nb_buckets * np.log(cardinality / nb_empty_buckets)
            return cardinality
        elif cardinality <= 2 ** 32 / 30:
            self.logger.info('Intermediate range')
            return cardinality
        self.logger.info('Large range')
        return -2 ** 32 * np.log(1 - cardinality / (2 ** 32))
