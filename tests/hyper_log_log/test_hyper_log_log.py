import numpy as np

from streaming_algorithms.hyper_log_log.hyper_log_log import HyperLogLog


class TestHyperLogLog:
    def test_nb_buckets(self):
        hyper_log_log = HyperLogLog(nb_buckets=32)
        assert hyper_log_log.nb_buckets == 32
        assert hyper_log_log.bucket_bits == np.log(32) / np.log(2)
        assert len(hyper_log_log.buckets) == 32

        hyper_log_log = HyperLogLog(nb_buckets=63)
        assert hyper_log_log.nb_buckets == 32
        assert hyper_log_log.bucket_bits == np.log(32) / np.log(2)
        assert len(hyper_log_log.buckets) == 32

    def test_add_item(self):
        custom_nb_buckets = 8
        custom_item = "hyper_log_log"
        hyper_log_log = HyperLogLog(nb_buckets=custom_nb_buckets)
        binary_item = bin(hash(str(custom_item)) & 0xffffffff)[2:].zfill(32)
        bucket_address = int(binary_item[-int(np.log(custom_nb_buckets) / np.log(2)):],
                             2)
        nb_leading_zeros = len(binary_item.split('1')[0]) + 1
        assert hyper_log_log.buckets[bucket_address] == 0
        hyper_log_log.add_item(item=custom_item)
        assert hyper_log_log.buckets[bucket_address] == nb_leading_zeros

    def test_estimate_cardinality_small_range_correction(self):
        custom_nb_buckets = 8
        hyper_log_log = HyperLogLog(nb_buckets=custom_nb_buckets)
        hyper_log_log.buckets = [1, 2, 3, 4, 0, 0, 0, 0]
        indicator_function = 0
        for bucket in hyper_log_log.buckets:
            indicator_function += 2 ** -bucket
        cardinality = hyper_log_log.alpha * hyper_log_log.nb_buckets ** 2 \
                      / indicator_function
        nb_empty_buckets = 4
        assert hyper_log_log.estimate_cardinality() == hyper_log_log.nb_buckets \
               * np.log(cardinality / nb_empty_buckets)

    def test_estimate_cardinality_small_range_no_correction(self):
        custom_nb_buckets = 8
        hyper_log_log = HyperLogLog(nb_buckets=custom_nb_buckets)
        hyper_log_log.buckets = [1, 2, 3, 4, 2, 1, 1, 1]
        indicator_function = 0
        for bucket in hyper_log_log.buckets:
            indicator_function += 2 ** -bucket
        cardinality = hyper_log_log.alpha * hyper_log_log.nb_buckets ** 2 \
                      / indicator_function
        assert hyper_log_log.estimate_cardinality() == cardinality

    def test_estimate_cardinality_intermediate_range_no_correction(self):
        custom_nb_buckets = 8
        hyper_log_log = HyperLogLog(nb_buckets=custom_nb_buckets)
        hyper_log_log.buckets = [16, 8, 12, 4, 13, 10, 19, 16]
        indicator_function = 0
        for bucket in hyper_log_log.buckets:
            indicator_function += 2 ** -bucket
        cardinality = hyper_log_log.alpha * hyper_log_log.nb_buckets ** 2 \
                      / indicator_function
        assert hyper_log_log.estimate_cardinality() == cardinality

    def test_estimate_cardinality_large_range_correction(self):
        custom_nb_buckets = 8
        hyper_log_log = HyperLogLog(nb_buckets=custom_nb_buckets)
        hyper_log_log.buckets = [42, 32, 24, 32, 34, 39, 29, 24]
        indicator_function = 0
        for bucket in hyper_log_log.buckets:
            indicator_function += 2 ** -bucket
        cardinality = hyper_log_log.alpha * hyper_log_log.nb_buckets ** 2 \
                      / indicator_function
        assert hyper_log_log.estimate_cardinality() == -2 ** 32 \
               * np.log(1 - cardinality / (2 ** 32))
