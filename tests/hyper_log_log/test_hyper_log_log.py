import numpy as np
import pytest

from hyper_log_log.hyper_log_log import HyperLogLog


class TestHyperLogLog:
    @pytest.mark.parametrize("nb_buckets, expected", [
        (32, 32),
        (61, 64),
        (15, 16)
    ])
    def test_nb_buckets(self, nb_buckets, expected):
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        assert hyper_log_log.nb_buckets == expected
        assert hyper_log_log.bucket_bits == np.log(expected) / np.log(2)
        assert len(hyper_log_log.buckets) == expected

    @pytest.mark.parametrize("nb_buckets, items_list", [
        (8, ["test", "stream", "telecom"]),
        (16, ["DATA", "Veepee"])
    ])
    def test_add_item(self, nb_buckets, items_list):
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        for item in items_list:
            binary_item = bin(hash(str(item)) & 0xffffffff)[2:].zfill(32)
            bucket_address = int(binary_item[-hyper_log_log.bucket_bits:], 2)
            nb_leading_zeros = len(binary_item.split('1')[0]) + 1
            bucket_value = hyper_log_log.buckets[bucket_address]
            hyper_log_log.add_item(item=item)
            assert hyper_log_log.buckets[bucket_address] == max(
                bucket_value,
                nb_leading_zeros
            )

    @pytest.mark.parametrize("nb_buckets, buckets", [
        (8, [1, 2, 3, 4, 0, 0, 0, 0]),
        (4, [1, 0, 2, 0])
    ])
    def test_estimate_cardinality_small_range_correction(self, nb_buckets, buckets):
        assert 0 in buckets, f'As least one bucket should be empty, got {buckets}'
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        hyper_log_log.buckets = buckets
        indicator_function = sum([2 ** -bucket for bucket in buckets])
        cardinality = hyper_log_log.alpha * nb_buckets ** 2 / indicator_function
        max_cardinality = 5 * nb_buckets / 2
        assert cardinality <= max_cardinality, f'Required cardinality <= ' \
            f'{max_cardinality}, got {cardinality}'
        nb_empty_buckets = sum([bucket == 0 for bucket in buckets])
        assert hyper_log_log.estimate_cardinality() == nb_buckets * np.log(
            cardinality / nb_empty_buckets)

    @pytest.mark.parametrize("nb_buckets, buckets", [
        (8, [1, 2, 3, 4, 2, 1, 1, 1]),
    ])
    def test_estimate_cardinality_small_range_no_correction(self, nb_buckets, buckets):
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        hyper_log_log.buckets = buckets
        indicator_function = sum([2 ** -bucket for bucket in buckets])
        cardinality = hyper_log_log.alpha * nb_buckets ** 2 / indicator_function
        max_cardinality = 5 * nb_buckets / 2
        assert cardinality <= max_cardinality, f'Required cardinality <= ' \
            f'{max_cardinality}, got {cardinality}'
        assert hyper_log_log.estimate_cardinality() == cardinality

    @pytest.mark.parametrize("nb_buckets, buckets", [
        (8, [16, 8, 12, 4, 13, 10, 19, 16]),
    ])
    def test_estimate_cardinality_intermediate_range_no_correction(
            self,
            nb_buckets,
            buckets):
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        hyper_log_log.buckets = buckets
        indicator_function = sum([2 ** -bucket for bucket in buckets])
        cardinality = hyper_log_log.alpha * nb_buckets ** 2 / indicator_function
        min_cardinality, max_cardinality = 5 * nb_buckets / 2, 2 ** 32 / 30
        assert min_cardinality < cardinality <= max_cardinality, f'Required ' \
            f'{min_cardinality} < cardinality <= {max_cardinality}, got {cardinality}'
        assert hyper_log_log.estimate_cardinality() == cardinality

    @pytest.mark.parametrize("nb_buckets, buckets", [
        (8, [42, 32, 24, 32, 34, 39, 29, 24]),
    ])
    def test_estimate_cardinality_large_range_correction(self, nb_buckets, buckets):
        hyper_log_log = HyperLogLog(nb_buckets=nb_buckets)
        hyper_log_log.buckets = buckets
        indicator_function = sum([2 ** -bucket for bucket in buckets])
        cardinality = hyper_log_log.alpha * nb_buckets ** 2 / indicator_function
        min_cardinality = 2 ** 32 / 30
        assert min_cardinality < cardinality, f'Required ' \
            f'{min_cardinality} < cardinality, got {cardinality}'
        assert hyper_log_log.estimate_cardinality() == -2 ** 32 * np.log(
            1 - cardinality / 2 ** 32)
